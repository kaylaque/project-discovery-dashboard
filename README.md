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

## Exploring Parts Registry
- mysqldump of the parts registry was downloaded from http://parts.igem.org/partsdb/download.cgi?type=parts
- the sqldump are then converted to sqlite using [mysql2sqlite](https://github.com/techouse/mysql-to-sqlite3)
- the converted sqlite are now available in zenodo: [https://zenodo.org/records/10067040](https://zenodo.org/records/10067040)
- download the zenodo sqlite:
```bash
mkdir -p "data/raw"
wget -P data/raw https://zenodo.org/records/10067040/files/igem_parts_registry.sqlite
```

## Using metabase to explore sqlite3
TO DO

# Development
## Using pre-commits
Activate pre-commit by:
```bash
pre-commit
```

Google Colaboratory notes (data viz): https://colab.research.google.com/drive/1O6zHdq1NvdNuM-UcIzns9Kid71uYKZQZ?usp=sharing 