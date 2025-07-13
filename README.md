# Celegans-Strain-Ortholog-Browser

This repository contains a small dataset of temperature sensitive *C. elegans* strains and a mapping of their human orthologs.  A static website located in the `docs/` directory allows searching these tables by gene or strain name.

## Usage

Open `docs/index.html` in a web browser or enable GitHub Pages for this repository.  Use the search box to filter by human gene symbol, worm gene, or strain name.  Links lead directly to the appropriate pages on [WormBase](https://wormbase.org/).

All source data are located in the `data/` directory and may also be downloaded from the **Downloads** section of the website.

The script `scripts/build_data_json.py` can be used to regenerate `docs/data.json` from the TSV tables.