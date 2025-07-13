import csv, json, os

# Paths relative to repository root
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ORTHOLOG_FILE = os.path.join(DATA_DIR, 'ortholog_table.tsv')
TS_FILE = os.path.join(DATA_DIR, 'temperature_sensitive_table.tsv')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'docs', 'data.json')

# Load ortholog mapping
orthologs = []
stable_to_symbol = {}
with open(ORTHOLOG_FILE, newline='') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        ce_gene = row['C. elegans Gene']
        stable = row['Human Gene Stable ID']
        symbol = row['Human Gene Name']
        orthologs.append({
            'ce_gene': ce_gene,
            'human_stable_id': stable,
            'human_gene': symbol
        })
        stable_to_symbol[stable] = symbol

# Load temperature sensitive strain info
strains = []
with open(TS_FILE, newline='') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        stable = row['Human Ortholog']
        strains.append({
            'strain_name': row['Strain Name'],
            'ts_mutation': row['TS Mutation/Allele'],
            'ce_gene': row['Gene'],
            'phenotype': row['Phenotype'],
            'human_stable_id': stable,
            'human_gene': stable_to_symbol.get(stable, '')
        })

data = {'orthologs': orthologs, 'strains': strains}

with open(OUTPUT_FILE, 'w') as out:
    json.dump(data, out, indent=2)