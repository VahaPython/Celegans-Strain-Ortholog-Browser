import argparse
import csv
from typing import Iterable, Set


def load_gene_list(path: str) -> Set[str]:
    """Load gene names from a text file."""
    genes: Set[str] = set()
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                genes.add(line)
    return genes


def filter_table(ts_path: str, genes: Iterable[str], output: str) -> None:
    """Write rows from ts_path whose 'Gene' field is in genes to output."""
    with open(ts_path, newline="") as inp, open(output, "w", newline="") as out:
        reader = csv.DictReader(inp, delimiter="\t")
        writer = csv.DictWriter(out, fieldnames=reader.fieldnames, delimiter="\t")
        writer.writeheader()
        genes_set = set(genes)
        for row in reader:
            if row.get("Gene") in genes_set:
                writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Filter the temperature sensitive strain table by a list of genes"
    )
    parser.add_argument("input", help="Path to temperature_sensitive_table.tsv")
    parser.add_argument("gene_list", help="Text file containing gene names")
    parser.add_argument("output", help="Output TSV file")
    args = parser.parse_args()

    genes = load_gene_list(args.gene_list)
    filter_table(args.input, genes, args.output)


if __name__ == "__main__":
    main()