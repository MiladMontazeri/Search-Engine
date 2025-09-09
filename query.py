
import argparse
import sys
from data_loader import parse_fasta
from search_engine import bmh_search

def run(pattern, fasta_files, ignore_case=True):
    pattern_norm = pattern.upper() if ignore_case else pattern
    hit_count = 0
    for path in fasta_files:
        for rec in parse_fasta(path):
            seq = rec.seq.upper() if ignore_case else rec.seq
            hits = bmh_search(seq, pattern_norm)
            for pos in hits:
                print(f"{rec.id}\t{pos}\t{seq[pos:pos+len(pattern_norm)]}")
                hit_count += 1
    return hit_count

def main(argv=None):
    parser = argparse.ArgumentParser(description="Protein sequence search using Boyer–Moore–Horspool")
    parser.add_argument("-p", "--pattern", help="Pattern to search (amino-acid letters)")
    parser.add_argument("fasta", nargs="*", help="Input FASTA file(s)")
    parser.add_argument("--case-sensitive", action="store_true", help="Case-sensitive search (default: case-insensitive)")
    args = parser.parse_args(argv)

    # If script is run without args (common in VS Code 'Run Python File'), prompt interactively
    if not args.pattern:
        try:
            args.pattern = input("Enter pattern: ").strip()
        except EOFError:
            print("ERROR: No pattern provided.", file=sys.stderr)
            sys.exit(2)
    if not args.fasta:
        try:
            paths = input("Enter FASTA file path(s), separated by spaces: ").strip()
            args.fasta = [p for p in paths.split() if p]
        except EOFError:
            print("ERROR: No FASTA files provided.", file=sys.stderr)
            sys.exit(2)

    if not args.pattern:
        print("ERROR: Pattern is empty.", file=sys.stderr)
        sys.exit(2)
    if not args.fasta:
        print("ERROR: No FASTA files given.", file=sys.stderr)
        sys.exit(2)

    ignore_case = not args.case_sensitive
    run(args.pattern, args.fasta, ignore_case=ignore_case)

if __name__ == "__main__":
    main()


