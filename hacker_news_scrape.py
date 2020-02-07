# to search through more than one page **MINE** -> this works.
# new url :
# https://news.ycombinator.com/news?p=num

import requests
from bs4 import BeautifulSoup
import datetime

# create   request (url to grab data)
# var


tday = (datetime.date.today())
td_str = tday.strftime("%m-%d-%Y")
# print(td_str)

print('starting to parse through pages...')
res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.storylink')
subtext = soup.select('.subtext')

## STRATEGY CHANGE TO DEAL WITH NO VOTES
# first grab the relevent stuff
responses = []
soups = []
# links = []
# subtext = []
for i in range(10):
    print(f'parsing page {i}...')
    response = requests.get(f'https://news.ycombinator.com/news?p={i}')
    responses.append(response)
    # url = '~/news/Hacker_News.html'
    # page = open(url)
    soup_object = BeautifulSoup(response.text, 'html.parser')
    soup.append(soup_object)

print(f'grabbing bulk relevent information from soup ...')
links = soup.select('.storylink')
subtext = soup.select('.subtext')


def my_hacker_news(links, subtext):
    # create hn list
    hn = []
    # loop thru w/ enumerate to give index also
    for indx, item in enumerate(links):
        title = links[indx].getText()
        # hn.append(title)
        link = links[indx].get('href', None)
        # hn.append((title, link))
        cont_len = len(subtext[indx].contents)
        # cont = subtext[indx].contents
        votes = None
        for i in range(cont_len):
            # to find in need to convert object to string
            if 'score' in str(subtext[indx].contents[i]):
                votes = int(subtext[indx].contents[i].getText().replace(' points', ''))
                break
        # votes = subtext[indx].contents.name
        # if votes:
        #    votes = votes.getText()
        if votes:
            hn.append((title, link, votes))
    return hn


# *********
# now lets call this fucntion
# print(my_hacker_news(links, votes))
# *********
print('running function to summarize soup info...')
hacks = my_hacker_news(links, subtext)


# get the key to sort it by
def getKey(item):
    return item[2]


# sort it
print('sorting info by votes...')
hacks = (sorted(hacks, key=getKey, reverse=True))

# awkward function to remove duplicates
hax = []


def remove_dups(hax):
    hax2 = []
    for i in hax:
        test = str(i[0])
        flag = True
        for elem in hax2:
            if elem[0] == test:
                flag = False
        if flag:
            hax2.append(i)
    return hax2


print('Total links found over 100 votes: ', len(hacks))
# call awkward remove dups
print('removing duplicate entries...')
hacks1 = remove_dups(hacks)

# this is just a check to see if remove_dups worked

print('Total NON-DUPLICATE links found over 100 votes: ', len(hacks1))

# now format it and print
for i in hacks1:
    if i[2] > 100:
        print()
        print(f'Votes:{i[2]}\n{i[0]}')
        print(i[1])

print()

with open(f'/home/Dhash_ad_1/news/{td_str}_Hacker_news.html', mode='a+') as my_file:
    # first fill with basic html header;
    my_file.write(
        f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Hacker News {td_str}</title>\n<meta name="description" content="The HTML5 Herald">\n<meta name="author" content="SitePoint">\n<link rel="stylesheet" href="css/styles.css">\n</head>\n<body>\n<script src="js/scripts.js"></script>')
    my_file.write(f'<h1> Hacker News {td_str}</h1>')
    my_file.write('<ol>')
    for i in hacks1:
        if i[2] > 100:
            my_file.write(f'<li><strong>Votes:{i[2]}</strong>')
            my_file.write(f'<ul class="container"><li class="item"><a href="{i[1]}">{i[0]}</a></li></ul></li><br />')

    my_file.write('</ol>')
    my_file.write('</body >')
    my_file.write('</html>')

