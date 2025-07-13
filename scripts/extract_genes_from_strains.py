import argparse
import csv
import json
from typing import List, Set


def extract_genes(ts_path: str) -> List[str]:
    """Return sorted list of unique gene names from a strain table."""
    genes: Set[str] = set()
    with open(ts_path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            gene = row.get("Gene")
            if gene:
                genes.add(gene.strip())
    return sorted(genes)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract unique gene names from a temperature sensitive strain table"
    )
    parser.add_argument("input", help="Path to temperature_sensitive_table.tsv")
    parser.add_argument(
        "-o",
        "--output",
        help="Output file (writes JSON if extension is .json; otherwise plain text)",
    )
    args = parser.parse_args()

    genes = extract_genes(args.input)

    if args.output:
        if args.output.lower().endswith(".json"):
            with open(args.output, "w") as fh:
                json.dump(genes, fh, indent=2)
        else:
            with open(args.output, "w") as fh:
                fh.write("\n".join(genes))
    else:
        for gene in genes:
            print(gene)


if __name__ == "__main__":
    main()