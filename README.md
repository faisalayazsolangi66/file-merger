# File Merger

Merge split chunks back into the original file. Works for any file
type — text, images, archives, PDFs — and joins chunks in the order
given, or in natural numeric order with `--sort` (so `part1`,
`part2`, `part10` merge correctly).

## Requirements

- Python 3 (standard library only, no extra packages)

## Usage

```bash
python3 main.py chunk1 chunk2 chunk3 -o merged.bin
python3 main.py --pattern "backup.zip.part*" -o backup.zip
python3 main.py part1 part2 part10 -o out.bin --sort --overwrite
```

## Example

```bash
$ echo -n "Hello " > a.part1
$ echo -n "world!" > a.part2
$ python3 main.py a.part1 a.part2 -o a.txt
Merging 2 chunk(s) into a.txt ...
  added a.part1 (6 bytes)
  added a.part2 (6 bytes)
Done: a.txt (12 bytes from 2 chunks)

$ cat a.txt
Hello world!
```

## License

MIT — see [LICENSE](LICENSE).
