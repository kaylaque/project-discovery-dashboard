import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

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
    return(wiki)

def extract_each_row(row, year):
    # Create a BeautifulSoup object
    soup = BeautifulSoup(row, 'html.parser')

    # Extract the team name
    team_name = soup.find('a', class_='team_name').get_text()
    link_team = soup.find('a', class_='team_name').get('href')
    # wiki_url = soup.find('a', href=True).get('href')
    wiki_url = get_wiki_url(str(row), year, soup)

    # extract other information
    infos = []
    for a in row.split('<td data-order='):
        infos.append(a.split('>')[-1])
    region = infos[2]
    country = infos[3]
    track = infos[4]
    kind = infos[5]
    section = infos[6]
    application = infos[7]
    return(team_name, link_team, wiki_url, region, country, track, kind, section, application)

def get_title_abstract(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    content = soup.findAll(id = 'table_abstract')[0].tr.td.get_text().split('\n')
    title = content[0]
    abstract = " ".join(content[1:])
    return(title, abstract)

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
year_range = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]


for year in year_range:
    url = 'https://old.igem.org/Team_List?year=' + str(year)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    all = re.split(r"<tr>", str(soup.table.tbody.tr))[1:]
    print(year)
    for i in range(len(all)):
        team_name, link_team, wiki_url, region, country, track, kind, section, application = extract_each_row(all[i], year)
        teams.append(team_name)
        links.append(link_team)
        title, abs = get_title_abstract(link_team)
        titles.append(title)
        abstracts.append(abs)
        wikis.append(wiki_url)
        regions.append(region)
        countries.append(country)
        tracks.append(track)
        kinds.append(kind)
        sections.append(section)
        apps.append(application)
        years.append(year)

# Create a DataFrame
df = pd.DataFrame({
    'Team name': teams,
    'Profile team': links,
    'Wiki URL': wikis,
    'Region': regions,
    'Country': countries,
    'Track': tracks,
    'Kind': kinds,
    'Section': sections,
    'Application': apps,
    'Year' : years,
    'Title': titles,
    'Abstract': abstracts
})

# Print the selected rows
print(f'Null rows in scraped result: {len(df[df.isnull().any(axis=1)])}')

df.to_csv('team_lists_all_years.csv', index=False)