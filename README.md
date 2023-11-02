# project-discovery-dashboard
 iGEM project discovery over time exploration

# Installation
Use mamba/conda to install the environments:
```bash
mamba create -f env.yaml
```

# Usage
## Scrape team data using the old igem portal
```python
python script_name.py --start_year 2008 --end_year 2023 --outfile data/raw/team_list_2008_2023.csv
```

# Development
## Using pre-commits
Activate pre-commit by:
```bash
pre-commit
```
