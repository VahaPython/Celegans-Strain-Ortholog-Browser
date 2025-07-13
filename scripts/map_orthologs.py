import argparse
import csv
import json
from typing import Dict, List


def load_orthologs(path: str) -> Dict[str, List[dict]]:
    """Load worm to human ortholog mappings from a TSV file."""
    mapping: Dict[str, List[dict]] = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            worm = row.get("C. elegans Gene")
            human_id = row.get("Human Gene Stable ID")
            human_name = row.get("Human Gene Name")
            if not worm:
                continue
            mapping.setdefault(worm, []).append({
                "stable_id": human_id,
                "name": human_name,
            })
    return mapping


def main() -> None:
    parser = argparse.ArgumentParser(description="Map worm genes to human orthologs")
    parser.add_argument("ortholog_table", help="Path to ortholog_table.tsv")
    parser.add_argument("-g", "--genes", help="File containing worm genes to map", default=None)
    parser.add_argument("-o", "--output", help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    mapping = load_orthologs(args.ortholog_table)

    if args.genes:
        with open(args.genes) as fh:
            genes = [line.strip() for line in fh if line.strip()]
        result = {g: mapping.get(g, []) for g in genes}
    else:
        result = mapping

    if args.output:
        with open(args.output, "w") as out:
            json.dump(result, out, indent=2)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()