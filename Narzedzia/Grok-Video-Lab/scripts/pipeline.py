#!/usr/bin/env python3
"""
pipeline.py — obrazki + przepis -> gotowy film (Grok Imagine + ffmpeg).

Tryb prosty (folder obrazków + jeden opis ruchu):
  python3 pipeline.py --input-dir input --prompt "powolny zoom, delikatny ruch" --output output/film.mp4

Tryb przepis (rekomendowany — scena po scenie, tu uczysz mnie swojego stylu):
  python3 pipeline.py --recipe przepisy/demo.md --output output/film.mp4

Format przepisu: zobacz przepisy/demo.md oraz README.
"""

import argparse
import os

import assemble
import grok_media as gm

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")


def list_images(d):
    if not os.path.isdir(d):
        raise SystemExit("Folder nie istnieje: %s" % d)
    out = []
    for name in sorted(os.listdir(d)):
        if name.lower().endswith(IMAGE_EXTS):
            out.append(os.path.join(d, name))
    return out


def parse_recipe(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    meta = {}
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            line = lines[i].strip()
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip().strip('"').strip("'")
            i += 1
        i += 1  # pomiń zamykające ---

    scenes = []
    cur = None
    for line in lines[i:]:
        s = line.strip()
        if s.startswith("## "):
            title = s[3:].strip()
            if title.lower().startswith("scena"):
                cur = {"title": title}
                scenes.append(cur)
            else:
                cur = None
        elif cur is not None and ":" in s:
            k, v = s.split(":", 1)
            kl = k.strip().lower()
            if kl in ("obraz", "image", "zdjecie"):
                cur["image"] = v.strip()
            elif kl in ("prompt", "opis"):
                cur["prompt"] = v.strip()
            elif kl in ("czas", "duration", "dlugosc"):
                cur["duration"] = v.strip()
            elif kl == "audio":
                cur["audio"] = v.strip()
    return meta, scenes


def resolve_image(recipe_path, val):
    if val.startswith(("http://", "https://", "data:")):
        return val
    if os.path.isabs(val):
        p = val
    else:
        base = os.path.dirname(os.path.abspath(recipe_path)) if recipe_path else os.getcwd()
        p = os.path.join(base, val)
    if not os.path.isfile(p):
        raise SystemExit("Nie znaleziono obrazu: %s" % p)
    return p


def aspect_for(orientation):
    return "9:16" if orientation == "pion" else "16:9"


def make_clip(args, scene, work, idx, aspect_ratio):
    prompt = scene.get("prompt") or args.prompt or ""
    duration = scene.get("duration") or args.duration
    res = gm.generate_video(prompt, image=scene.get("image"), model=args.model,
                            duration=int(duration) if duration else None,
                            aspect_ratio=aspect_ratio, resolution=args.resolution)
    rid = res.get("request_id")
    print("[scena %d] request_id=%s" % (idx, rid))
    if args.dry_run:
        return None
    final = gm.poll_video(rid, args.poll_interval, args.max_wait)
    url = gm.video_url(final)
    if not url:
        raise SystemExit("Scena %d: brak URL wideo" % idx)
    dest = os.path.join(work, "scene_%02d.mp4" % idx)
    gm.download(url, dest)
    print("[scena %d] -> %s" % (idx, dest))
    return dest


def main(argv=None):
    ap = argparse.ArgumentParser(description="Obrazy + przepis -> film")
    ap.add_argument("--recipe", help="plik przepisu markdown")
    ap.add_argument("--input-dir", help="folder z obrazkami (tryb prosty)")
    ap.add_argument("--prompt", help="opis ruchu/sceny (tryb prosty)")
    ap.add_argument("--output", required=True)
    ap.add_argument("--work", default="work", help="katalog roboczy na klipy")
    ap.add_argument("--orientation", choices=["pion", "poziom"], default="pion")
    ap.add_argument("--resolution", choices=["480p", "720p"], default="720p")
    ap.add_argument("--canvas", type=int, choices=[720, 1080], default=720,
                    help="rozdzielczość montażu (720p/1080p)")
    ap.add_argument("--model", default=gm.DEFAULT_VIDEO_MODEL)
    ap.add_argument("--duration", type=int, default=8)
    ap.add_argument("--transition", default="fade")
    ap.add_argument("--audio")
    ap.add_argument("--poll-interval", type=int, default=10)
    ap.add_argument("--max-wait", type=int, default=900)
    ap.add_argument("--dry-run", action="store_true", help="tylko plan, bez API")
    ap.add_argument("--api-key")
    args = ap.parse_args(argv)
    gm.set_api_key(args.api_key)

    os.makedirs(args.work, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    aspect = aspect_for(args.orientation)
    scenes = []
    recipe_path = None

    if args.recipe:
        recipe_path = os.path.abspath(args.recipe)
        meta, parsed = parse_recipe(recipe_path)
        if meta.get("orientacja") in ("pion", "poziom"):
            args.orientation = meta["orientacja"]
            aspect = aspect_for(args.orientation)
        if meta.get("rozdzielczosc"):
            args.resolution = meta["rozdzielczosc"]
        if meta.get("canvas"):
            args.canvas = int(meta["canvas"])
        if meta.get("model"):
            args.model = meta["model"]
        if meta.get("przejscie"):
            args.transition = meta["przejscie"]
        audio = meta.get("audio") or args.audio
        if audio and not os.path.isabs(audio):
            audio = os.path.join(os.path.dirname(recipe_path), audio)
        args.audio = audio
        for s in parsed:
            if not s.get("image"):
                raise SystemExit("Scena '%s' bez pola obraz:" % s.get("title"))
            if not s.get("prompt"):
                raise SystemExit("Scena '%s' bez pola prompt:" % s.get("title"))
            s["image"] = resolve_image(recipe_path, s["image"])
            scenes.append(s)
    elif args.input_dir:
        if not args.prompt:
            raise SystemExit("W trybie prostym podaj --prompt")
        for img in list_images(args.input_dir):
            scenes.append({"title": os.path.basename(img), "image": img, "prompt": args.prompt})
    else:
        raise SystemExit("Podaj --recipe albo --input-dir")

    if not scenes:
        raise SystemExit("Brak scen do wygenerowania")

    print("Sceny: %d | orientacja: %s | rozdzielczość: %s | model: %s"
          % (len(scenes), args.orientation, args.resolution, args.model))

    clips = []
    for i, s in enumerate(scenes, 1):
        print("- scena %d: %s" % (i, s["title"]))
        print("    obraz: %s" % s["image"])
        print("    prompt: %s" % s["prompt"])
        print("    czas: %ss" % (s.get("duration") or args.duration))
        if args.dry_run:
            clips.append(None)
            continue
        c = make_clip(args, s, args.work, i, aspect)
        clips.append(c)

    if args.dry_run:
        print("DRY-RUN: nie wywołano API. Aby generować, usuń --dry-run.")
        return

    print("Montaż %d klipów..." % len(clips))
    out = assemble.assemble(clips, args.output, args.orientation,
                            resolution=args.canvas,
                            transition=args.transition, audio=args.audio)
    print("Gotowy film:", out)


if __name__ == "__main__":
    main()
