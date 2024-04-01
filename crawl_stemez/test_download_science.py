from bs4 import BeautifulSoup
import urllib.request
import tqdm
import re
import argparse
import os

parser = argparse.ArgumentParser(
                    prog='stemez',
                    description='What the program does',
                    epilog='Text at the bottom of help')
parser.add_argument('--subject', "-s", type=str, default="chemistry")
args = parser.parse_args()

subject_dict = {
    'physics': ('Physics', 'DPhysics'),
    'chemistry': ('Chemistry', 'EChemistry'),
    'biology': ('Biology', 'FBiology'),
    'cs': ('ComputerScience', 'GComputerScience'),
}

subject, field = subject_dict[args.subject]

# Read the HTML file
# with open(f'index.html', 'r', encoding = 'windows-1252') as file:
#     html = file.read()

base = f'https://stemez.com/subjects/science/{field}/{field}/{field}/'
html = urllib.request.urlopen(base + "E00-0Find.htm")
# Create a BeautifulSoup object
soup = BeautifulSoup(html, 'html.parser')
a_tags = soup.find_all('a')
hrefs = [a.get('href') for a in a_tags]

all_hrefs=  []
# Print all the href links
for href in tqdm.tqdm(hrefs):
    if href and '-Ch' in href:
        html = urllib.request.urlopen(base + href)
        soup = BeautifulSoup(html, 'html.parser')
        a_tags = soup.find_all('a')

        # Extract href attributes
        for a in a_tags:
            if a.get('href') and 'Ch' in a.get('href'):
                page_url = base + a.get('href')
                print(page_url)
                html = urllib.request.urlopen(page_url)

                # Create a BeautifulSoup object
                soup = BeautifulSoup(html, 'html.parser')

                # Find all the <a> tags
                a_tags_more = soup.find_all('a')
                for a_more in a_tags_more:
                    if a_more.get('href'):
                        url = a_more.get('href')
                        if re.search('.[0-9]+-[0-9]+.htm', url):
                            all_hrefs.append(base + url)

for url in tqdm.tqdm(all_hrefs):
    if not os.path.exists(f'{subject}/{url.split("/")[-1]}'):
        urllib.request.urlretrieve(url, f'{subject}/{url.split("/")[-1]}')
