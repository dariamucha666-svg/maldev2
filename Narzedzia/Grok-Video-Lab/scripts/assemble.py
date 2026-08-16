#!/usr/bin/env python3
"""
assemble.py — montaż klipów przez ffmpeg (bez watermarku, bez GPU).

Normalizuje klipy do wspólnego canvasa (pion/poziom), łączy je przejściem xfade,
opcjonalnie podkłada audio w pętli. Zgodne z ustaleniami w [[Studio_Klip]].

Przykłady:
  python3 assemble.py --inputs work/a.mp4 work/b.mp4 --output output/film.mp4
  python3 assemble.py --inputs work/a.mp4 work/b.mp4 --output out.mp4 --orientation pion --transition fade --audio audio/muzyka.mp3
"""

import argparse
import json
import subprocess

CANVAS = {
    ("pion", 720): (720, 1280),
    ("pion", 1080): (1080, 1920),
    ("poziom", 720): (1280, 720),
    ("poziom", 1080): (1920, 1080),
}


def probe_duration(path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "json", path],
            capture_output=True, text=True, timeout=30)
        if out.returncode == 0:
            return float(json.loads(out.stdout)["format"]["duration"])
    except Exception:
        pass
    return 5.0


def run(cmd):
    print("+ " + " ".join(cmd))
    r = subprocess.run(cmd)
    if r.returncode != 0:
        raise SystemExit("ffmpeg zwrócił kod %s" % r.returncode)


def assemble(inputs, output, orientation="pion", resolution=720, transition="fade",
             transition_duration=0.5, audio=None, fps=30):
    inputs = list(inputs)
    if not inputs:
        raise SystemExit("Brak klipów wejściowych")
    try:
        w, h = CANVAS[(orientation, resolution)]
    except KeyError:
        raise SystemExit("Nieznany canvas: %s %sp" % (orientation, resolution))

    durations = [probe_duration(x) for x in inputs]
    d = float(transition_duration)

    fc = []
    for i in range(len(inputs)):
        fc.append(
            "[%d:v]scale=%d:%d:force_original_aspect_ratio=decrease,"
            "pad=%d:%d:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=%d,format=yuv420p[v%d]"
            % (i, w, h, w, h, fps, i)
        )

    n = len(inputs)
    if n == 1:
        fc.append("[v0]null[vout]")
    else:
        prev = "v0"
        offset = durations[0] - d
        for i in range(1, n):
            label = "x%d" % i
            out_label = "vout" if i == n - 1 else label
            fc.append(
                "[%s][v%d]xfade=transition=%s:duration=%.3f:offset=%.3f[%s]"
                % (prev, i, transition, d, offset, out_label)
            )
            prev = label if i < n - 1 else out_label
            offset += durations[i] - d

    total = sum(durations) - (n - 1) * d
    if total <= 0:
        raise SystemExit("Łączny czas po przejściach <= 0; za krótkie klipy lub za długie przejście")

    cmd = ["ffmpeg", "-y"]
    for x in inputs:
        cmd += ["-i", x]

    maps = ["-map", "[vout]"]
    if audio:
        audio_index = n
        cmd += ["-stream_loop", "-1", "-i", audio]
        fc.append(
            "[%d:a]atrim=0:%.3f,asetpts=PTS-STARTPTS,afade=t=out:st=%.3f:d=1[aout]"
            % (audio_index, total, max(0.0, total - 1.0))
        )
        maps += ["-map", "[aout]"]

    cmd += ["-filter_complex", ";".join(fc)]
    cmd += maps
    cmd += ["-t", "%.3f" % total]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", output]
    run(cmd)
    return output


def main(argv=None):
    ap = argparse.ArgumentParser(description="Montaż klipów ffmpeg")
    ap.add_argument("--inputs", nargs="+", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--orientation", choices=["pion", "poziom"], default="pion")
    ap.add_argument("--resolution", type=int, choices=[720, 1080], default=720)
    ap.add_argument("--transition", default="fade")
    ap.add_argument("--transition-duration", type=float, default=0.5)
    ap.add_argument("--audio")
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args(argv)
    out = assemble(args.inputs, args.output, args.orientation, args.resolution,
                   args.transition, args.transition_duration, args.audio, args.fps)
    print("Gotowe:", out)


if __name__ == "__main__":
    main()
