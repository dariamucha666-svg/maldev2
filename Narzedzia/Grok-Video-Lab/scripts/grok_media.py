#!/usr/bin/env python3
"""
grok_media.py — klient xAI Grok Imagine: obrazy, edycja, wideo (asynchronicznie).

Bez zewnętrznych zależności (tylko biblioteka standardowa). Endpointy:
  POST /v1/images/generations    tekst -> obraz
  POST /v1/images/edits          edycja / kompozycja obrazów
  POST /v1/videos/generations    tekst/obraz/referencje -> wideo
  GET  /v1/videos/{request_id}   odpytywanie statusu

Klucz API (pierwszy trafiony wygrywa):
  1) --api-key
  2) zmienna środowiskowa XAI_API_KEY
  3) plik .env (szukany w górę od bieżącego katalogu)

Przykłady:
  python3 grok_media.py image  --prompt "kot w kosmosie" --out work/
  python3 grok_media.py edit   --images a.png b.png --prompt "połącz oba" --out work/
  python3 grok_media.py video  --image a.png --prompt "powolny zoom" --out work/
  python3 grok_media.py status REQUEST_ID --out work/
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://api.x.ai/v1"
DEFAULT_IMAGE_MODEL = "grok-imagine-image"
DEFAULT_VIDEO_MODEL = "grok-imagine-video"

_EXPLICIT_KEY = None


def set_api_key(key):
    global _EXPLICIT_KEY
    _EXPLICIT_KEY = key


# ---------------------------------------------------------------------------
# klucz API
# ---------------------------------------------------------------------------

def _find_env_file(start):
    d = os.path.abspath(start)
    for _ in range(6):
        p = os.path.join(d, ".env")
        if os.path.isfile(p):
            return p
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


def _read_env_file(path):
    out = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def _grok_cached_token():
    """Token z zalogowanej sesji Grok CLI (~/.grok/auth.json), jeśli nie wygasł."""
    import datetime
    p = os.path.join(os.path.expanduser("~"), ".grok", "auth.json")
    try:
        data = json.load(open(p, encoding="utf-8"))
    except Exception:
        return None
    now = datetime.datetime.now(datetime.timezone.utc)
    for k, entry in data.items():
        if not isinstance(k, str) or "auth.x.ai" not in k:
            continue
        if not isinstance(entry, dict) or not entry.get("key"):
            continue
        exp = entry.get("expires_at")
        if exp:
            try:
                exp_dt = datetime.datetime.fromisoformat(str(exp).replace("Z", "+00:00"))
                if exp_dt.tzinfo is None:
                    exp_dt = exp_dt.replace(tzinfo=datetime.timezone.utc)
                if exp_dt < now:
                    continue
            except Exception:
                pass
        return entry["key"]
    return None


def load_api_key():
    if _EXPLICIT_KEY:
        return _EXPLICIT_KEY
    if os.environ.get("XAI_API_KEY"):
        return os.environ["XAI_API_KEY"]
    env = _find_env_file(os.getcwd())
    if env:
        val = _read_env_file(env).get("XAI_API_KEY")
        if val:
            return val
    cached = _grok_cached_token()
    if cached:
        return cached
    raise SystemExit(
        "Brak klucza XAI_API_KEY. Ustaw zmienną XAI_API_KEY lub wklej klucz do pliku .env "
        "(skopiuj .env.example)."
    )


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def http_json(method, path, body=None, base_url=None):
    base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
    url = base_url + path
    headers = {
        "Authorization": "Bearer " + load_api_key(),
        "Content-Type": "application/json",
        "User-Agent": "grok-video-lab/1.0",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read()
            return json.loads(raw.decode("utf-8")) if raw else None
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise SystemExit("HTTP %s %s %s | %s" % (e.code, method, path, detail[:2000]))
    except urllib.error.URLError as e:
        raise SystemExit("Błąd sieci: %s" % (e.reason,))


# ---------------------------------------------------------------------------
# pliki -> data URL
# ---------------------------------------------------------------------------

_EXT_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".mp4": "video/mp4",
}


def _mime_for(path):
    ext = os.path.splitext(path)[1].lower()
    return _EXT_MIME.get(ext) or (mimetypes.guess_type(path)[0] or "image/png")


def data_uri(path):
    if not os.path.isfile(path):
        raise SystemExit("Plik nie istnieje: %s" % path)
    mime = _mime_for(path)
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return "data:%s;base64,%s" % (mime, b64)


def resolve_image_ref(x):
    """Lokalna ścieżka -> data URL, http(s)/data -> url."""
    if x.startswith(("http://", "https://", "data:")):
        return {"url": x}
    return {"url": data_uri(x)}


# ---------------------------------------------------------------------------
# pobieranie
# ---------------------------------------------------------------------------

def download(url, dest):
    if url.startswith("data:"):
        return _save_data_uri(url, dest)
    if os.path.isdir(dest):
        name = url.split("/")[-1].split("?")[0] or "media.mp4"
        dest = os.path.join(dest, name)
    dest_dir = os.path.dirname(os.path.abspath(dest)) or "."
    os.makedirs(dest_dir, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "grok-video-lab/1.0"})
    with urllib.request.urlopen(req, timeout=600) as resp, open(dest, "wb") as f:
        f.write(resp.read())
    return dest


def _save_data_uri(uri, dest):
    header, _, b64 = uri.partition(",")
    mime = "image/png"
    if ":" in header:
        mime = header.split(":")[1].split(";")[0]
    ext = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp",
           "video/mp4": ".mp4", "audio/mpeg": ".mp3", "audio/wav": ".wav"}.get(mime, ".bin")
    if os.path.isdir(dest):
        dest = os.path.join(dest, "media" + ext)
    elif not dest.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mp3", ".wav")):
        dest += ext
    os.makedirs(os.path.dirname(os.path.abspath(dest)) or ".", exist_ok=True)
    with open(dest, "wb") as f:
        f.write(base64.b64decode(b64))
    return dest


# ---------------------------------------------------------------------------
# operacje API
# ---------------------------------------------------------------------------

def generate_image(prompt, model=DEFAULT_IMAGE_MODEL, n=1, aspect_ratio=None, resolution=None):
    body = {"model": model, "prompt": prompt, "n": n}
    if aspect_ratio:
        body["aspect_ratio"] = aspect_ratio
    if resolution:
        body["resolution"] = resolution
    return http_json("POST", "/images/generations", body)


def edit_image(prompt, images, model=DEFAULT_IMAGE_MODEL):
    body = {"model": model, "prompt": prompt}
    refs = [resolve_image_ref(x) for x in images]
    if len(refs) == 1:
        body["image"] = refs[0]
    else:
        body["images"] = refs
    return http_json("POST", "/images/edits", body)


def generate_video(prompt, image=None, references=None, audios=None,
                   model=DEFAULT_VIDEO_MODEL, duration=None, aspect_ratio=None,
                   resolution=None):
    body = {"model": model, "prompt": prompt}
    if image:
        body["image"] = resolve_image_ref(image)
    if references:
        body["reference_images"] = [resolve_image_ref(r) for r in references]
    if audios:
        body["reference_audios"] = [resolve_image_ref(a) for a in audios]
    if duration:
        body["duration"] = int(duration)
    if aspect_ratio:
        body["aspect_ratio"] = aspect_ratio
    if resolution:
        body["resolution"] = resolution
    return http_json("POST", "/videos/generations", body)


def poll_video(request_id, poll_interval=10, max_wait=900, quiet=False):
    deadline = time.time() + max_wait
    while True:
        res = http_json("GET", "/videos/%s" % request_id)
        status = res.get("status")
        if status == "done":
            return res
        if status in ("failed", "expired", "canceled", "cancelled"):
            raise SystemExit("Generowanie zakończone jako '%s': %s"
                             % (status, json.dumps(res.get("error") or res)[:1000]))
        if not quiet:
            print("  [%s] postęp=%s%%" % (status, res.get("progress")))
        if time.time() >= deadline:
            raise SystemExit(
                "Timeout po %ss. Sprawdź później: python3 grok_media.py status %s"
                % (max_wait, request_id))
        time.sleep(poll_interval)


def video_url(final):
    return (final.get("video") or {}).get("url")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _save_image_results(res, out):
    data = res.get("data") or []
    if not data and isinstance(res, dict):
        data = [res]
    os.makedirs(out, exist_ok=True)
    saved = []
    for i, item in enumerate(data):
        url = item.get("url")
        b64 = item.get("b64_json") or item.get("base64")
        if url:
            saved.append(download(url, os.path.join(out, "img_%02d.png" % (i + 1))))
        elif b64:
            dest = os.path.join(out, "img_%02d.png" % (i + 1))
            with open(dest, "wb") as f:
                f.write(base64.b64decode(b64))
            saved.append(dest)
    return saved


def _cmd_image(args):
    res = generate_image(args.prompt, args.model, args.n, args.aspect_ratio, args.resolution)
    print(json.dumps(res, indent=2)[:4000])
    for p in _save_image_results(res, args.out):
        print("Zapisano:", p)


def _cmd_edit(args):
    if not args.images:
        raise SystemExit("Podaj co najmniej jeden --image")
    res = edit_image(args.prompt, args.images, args.model)
    print(json.dumps(res, indent=2)[:4000])
    for p in _save_image_results(res, args.out):
        print("Zapisano:", p)


def _cmd_video(args):
    res = generate_video(args.prompt, args.image, args.references, args.audios,
                         args.model, args.duration, args.aspect_ratio, args.resolution)
    rid = res.get("request_id")
    print("request_id:", rid)
    if args.no_wait:
        print("Nie czekam. Odpytuj przez: python3 grok_media.py status %s" % rid)
        return
    final = poll_video(rid, args.poll_interval, args.max_wait)
    print(json.dumps(final, indent=2)[:4000])
    url = video_url(final)
    if url:
        dest = download(url, args.out)
        print("Wideo zapisane:", dest)
    else:
        print("Brak URL wideo w odpowiedzi.")


def _cmd_status(args):
    final = poll_video(args.request_id, args.poll_interval, args.max_wait)
    print(json.dumps(final, indent=2)[:4000])
    url = video_url(final)
    if url:
        dest = download(url, args.out)
        print("Wideo zapisane:", dest)


def _cmd_models(args):
    res = http_json("GET", "/models")
    for m in res.get("data", []):
        mid = m.get("id", "")
        if any(k in mid for k in ("image", "video", "imagine")):
            print(mid)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Klient xAI Grok Imagine (obrazy + wideo)")
    ap.add_argument("--api-key", help="Klucz xAI (domyślnie XAI_API_KEY / .env)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("image", help="tekst -> obraz")
    p.add_argument("--prompt", required=True)
    p.add_argument("--model", default=DEFAULT_IMAGE_MODEL)
    p.add_argument("--n", type=int, default=1)
    p.add_argument("--aspect-ratio", help="np. 1:1, 16:9, 9:16")
    p.add_argument("--resolution", help="np. 1k, 2k")
    p.add_argument("--out", default="work")
    p.set_defaults(func=_cmd_image)

    p = sub.add_parser("edit", help="edycja / kompozycja obrazów")
    p.add_argument("--prompt", required=True)
    p.add_argument("--image", action="append", dest="images", required=True,
                   help="obraz (ścieżka lub URL); powtórz dla wielu")
    p.add_argument("--model", default=DEFAULT_IMAGE_MODEL)
    p.add_argument("--out", default="work")
    p.set_defaults(func=_cmd_edit)

    p = sub.add_parser("video", help="generuj wideo")
    p.add_argument("--prompt", required=True)
    p.add_argument("--image", help="obraz startowy (image-to-video)")
    p.add_argument("--reference", action="append", dest="references",
                   help="obraz referencyjny (powtórz, max 3)")
    p.add_argument("--audio", action="append", dest="audios",
                   help="audio referencyjne (powtórz, max 3)")
    p.add_argument("--model", default=DEFAULT_VIDEO_MODEL)
    p.add_argument("--duration", type=int, help="sekundy (1-15, domyślnie 8)")
    p.add_argument("--aspect-ratio", choices=["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"])
    p.add_argument("--resolution", choices=["480p", "720p"])
    p.add_argument("--out", default="work")
    p.add_argument("--no-wait", action="store_true", help="tylko zwróć request_id")
    p.add_argument("--poll-interval", type=int, default=10)
    p.add_argument("--max-wait", type=int, default=900)
    p.set_defaults(func=_cmd_video)

    p = sub.add_parser("status", help="status / pobranie wideo")
    p.add_argument("request_id")
    p.add_argument("--out", default="work")
    p.add_argument("--poll-interval", type=int, default=10)
    p.add_argument("--max-wait", type=int, default=900)
    p.set_defaults(func=_cmd_status)

    p = sub.add_parser("models", help="wypisz modele media xAI")
    p.set_defaults(func=_cmd_models)

    args = ap.parse_args(argv)
    set_api_key(args.api_key)
    args.func(args)


if __name__ == "__main__":
    main()
