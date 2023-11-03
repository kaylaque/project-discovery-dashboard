"""
Scrape iGEM team data from old.igem.org.

This script extracts team data from the iGEM website for a range of years.
The extracted data includes team names, profile links, wiki URLs, regions, countries, tracks, kinds, sections, applications, years, titles, and abstracts.
The data is then saved to a CSV file named 'team_lists_all_years.csv'.

Usage:
    python script_name.py --start_year 2008 --end_year 2023 --outfile data/raw/team_list_all_years.csv
"""

import argparse
import logging
import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

log_format = "%(levelname)-8s %(asctime)s   %(message)s"
date_format = "%d/%m %H:%M:%S"
logging.basicConfig(format=log_format, datefmt=date_format, level=logging.INFO)


def get_wiki_url(html, year, soup):
    # Create a regular expression to match the target URLs.
    url_regex = rf'"http:\/\/{year}(.*)\.igem\.org\/(.*)"'
    # Find all matching URLs in the HTML.
    urls = re.findall(url_regex, html)
    if len(urls) == 0:
        # Create a regular expression to match the target URLs.
        url_regex = rf'"https:\/\/{year}(.*)\.igem\.org\/(.*)"'
        # Find all matching URLs in the HTML.
        urls = re.findall(url_regex, html)
        if len(urls) > 0:
            wiki = f"https://{year}{urls[0][0]}.igem.org/{urls[0][1]}"
            wiki = wiki.split('">Wiki<')[0]
        elif len(urls) == 0:
            # Create a regular expression to match the target URLs.
            url_regex = rf'"https:\/\/{year}\.igem\.wiki\/(.*)"'
            # Find all matching URLs in the HTML.
            urls = re.findall(url_regex, html)
            if len(urls) > 0:
                wiki = f"https://{year}.igem.wiki/{urls[0]}"
                wiki = wiki.split('">Wiki<')[0]
            else:
                wiki = None
    else:
        wiki = f"https://{year}{urls[0][0]}.igem.org/{urls[0][1]}"
        wiki = wiki.split('">Wiki<')[0]
    # if soup.find('a', href=re.compile('wiki')) is not None:
    #     wiki = soup.find('a', href=re.compile('wiki')).get('href')
    # elif soup.find('a', href=re.compile('org')) is not None:
    #     wiki = soup.find('a', href=re.compile('igem')).get('href')
    # else:
    #     wiki = None
    logging.info(f"Found wiki url: {wiki}")
    return wiki


def extract_each_row(row, year):
    logging.info("Extracting each rows...")
    # Create a BeautifulSoup object
    soup = BeautifulSoup(row, "html.parser")

    # Extract the team name
    team_name = soup.find("a", class_="team_name").get_text()
    link_team = soup.find("a", class_="team_name").get("href")
    # wiki_url = soup.find('a', href=True).get('href')
    wiki_url = get_wiki_url(str(row), year, soup)

    # extract other information
    infos = []
    for a in row.split("<td data-order="):
        infos.append(a.split(">")[-1])
    region = infos[2]
    country = infos[3]
    track = infos[4]
    kind = infos[5]
    section = infos[6]
    application = infos[7]
    return (
        team_name,
        link_team,
        wiki_url,
        region,
        country,
        track,
        kind,
        section,
        application,
    )

def get_members(url):
    # url = 'https://old.igem.org/Team.cgi?team_id=4769' #2023
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    team = []
    for i in range(len(soup.findAll('table', id = 'table_roster'))):
        roster = str(soup.findAll('table', id = 'table_roster')[i]).split('<b>')
        for i in roster:
            soup2 = BeautifulSoup(i.replace('\n', ''), 'html.parser')
            if soup2.td.td is not None:
                sub_roster = str(soup2.td).split('<!-- Non-editable Member')
                if len(sub_roster) > 1:
                    for i in sub_roster:
                        soup3 = BeautifulSoup(i.replace('\n', ''), 'html.parser')
                        if soup3.td.td.get_text() is not None and str(soup3.td.td.get_text()) != '':
                            # print(soup3.td.td.get_text())
                            team.append(soup3.td.td.get_text())
                else:
                    # print(soup2.td.td.get_text())
                    team.append(soup2.td.td.get_text())
    return(team)

def get_title_abstract(url):
    logging.info("Getting title abstract...")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    content = soup.findAll(id="table_abstract")[0].tr.td.get_text().split("\n")
    title = content[0]
    abstract = " ".join(content[1:])
    return (title, abstract)


def main(start_year, end_year, outfile):
    teams = []
    links = []
    wikis = []
    regions = []
    countries = []
    tracks = []
    kinds = []
    sections = []
    apps = []
    years = []
    titles = []
    abstracts = []
    team_members = []
    year_range = list(range(start_year, end_year + 1))

    for year in year_range:
        url = "https://old.igem.org/Team_List?year=" + str(year)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        all = re.split(r"<tr>", str(soup.table.tbody.tr))[1:]
        logging.info(f"Scraping data from year: {year}")
        total_teams = len(all)
        for num, i in enumerate(range(len(all))):
            logging.info(f"Processing data: {num+1}/{total_teams}")
            (
                team_name,
                link_team,
                wiki_url,
                region,
                country,
                track,
                kind,
                section,
                application,
            ) = extract_each_row(all[i], year)
            teams.append(team_name)
            links.append(link_team)
            title, abstract = get_title_abstract(link_team)
            members = get_members(link_team)
            titles.append(title)
            abstracts.append(abstract)
            team_members.append(members)
            wikis.append(wiki_url)
            regions.append(region)
            countries.append(country)
            tracks.append(track)
            kinds.append(kind)
            sections.append(section)
            apps.append(application)
            years.append(year)

    # Create a DataFrame
    df = pd.DataFrame(
        {
            "Team name": teams,
            "Profile team": links,
            "Wiki URL": wikis,
            "Region": regions,
            "Country": countries,
            "Track": tracks,
            "Kind": kinds,
            "Section": sections,
            "Application": apps,
            "Year": years,
            "Title": titles,
            "Abstract": abstracts,
        }
    )

    # Print the selected rows
    logging.debug(f"Null rows in scraped result: {len(df[df.isnull().any(axis=1)])}")

    outfile = Path(outfile)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(outfile, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape iGEM team data from old.igem.org."
    )
    parser.add_argument(
        "--start_year",
        type=int,
        required=True,
        help="Starting year for data extraction.",
    )
    parser.add_argument(
        "--end_year", type=int, required=True, help="Ending year for data extraction."
    )
    parser.add_argument("--outfile", type=str, required=True, help="Output file (csv).")
    args = parser.parse_args()

    main(args.start_year, args.end_year, args.outfile)
