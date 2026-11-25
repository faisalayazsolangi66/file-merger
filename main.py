#!/usr/bin/env python3
"""Merge split chunks back into the original file.

Chunks are joined in the order given on the command line (or, with
--sort, in natural numeric order, so part1, part2, part10 merge
correctly). Works for any file type: text, images, archives, PDFs.
Use with the companion file-splitter tool, or any ``name.partNNN``
style chunks.
"""
import argparse
import glob
import os
import re
import sys


def natural_key(path):
    """Sort key that orders embedded numbers numerically."""
    name = os.path.basename(path)
    return [int(t) if t.isdigit() else t.lower()
            for t in re.split(r"(\d+)", name)]


def expand_inputs(inputs, pattern):
    """Expand a glob pattern, or return the explicit file list."""
    if pattern:
        files = sorted(glob.glob(pattern), key=natural_key)
        if not files:
            print(f"error: no files match pattern: {pattern}", file=sys.stderr)
            sys.exit(1)
        return files
    return list(inputs)


def merge_chunks(chunks, output, overwrite=False, chunk_size=1024 * 1024):
    """Concatenate *chunks* (in order) into *output*; return total bytes."""
    if os.path.exists(output) and not overwrite:
        print(f"error: output already exists: {output} (use --overwrite)",
              file=sys.stderr)
        sys.exit(1)
    if os.path.abspath(output) in {os.path.abspath(c) for c in chunks}:
        print("error: output file must not be one of the chunks",
              file=sys.stderr)
        sys.exit(1)
    total = 0
    with open(output, "wb") as out:
        for chunk in chunks:
            if not os.path.isfile(chunk):
                print(f"error: chunk not found: {chunk}", file=sys.stderr)
                sys.exit(1)
            with open(chunk, "rb") as src:
                while True:
                    data = src.read(chunk_size)
                    if not data:
                        break
                    out.write(data)
                    total += len(data)
            print(f"  added {chunk} ({os.path.getsize(chunk)} bytes)")
    return total


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Merge split chunks back into the original file.")
    parser.add_argument("chunks", nargs="*", metavar="CHUNK",
                        help="chunk files in merge order")
    parser.add_argument("-o", "--output", required=True,
                        help="path of the merged output file")
    parser.add_argument("--pattern",
                        help="glob pattern for chunks, e.g. 'backup.zip.part*'")
    parser.add_argument("--sort", action="store_true",
                        help="sort chunks in natural numeric order")
    parser.add_argument("--overwrite", action="store_true",
                        help="overwrite the output file if it exists")
    args = parser.parse_args(argv)

    if not args.chunks and not args.pattern:
        parser.error("give chunk files, or use --pattern")
    chunks = expand_inputs(args.chunks, args.pattern)
    if args.sort:
        chunks = sorted(chunks, key=natural_key)
    if len(chunks) < 2:
        print("warning: only one chunk given; copying it as-is")

    print(f"Merging {len(chunks)} chunk(s) into {args.output} ...")
    total = merge_chunks(chunks, args.output, overwrite=args.overwrite)
    print(f"Done: {args.output} ({total} bytes from {len(chunks)} chunks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
