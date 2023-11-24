#!/usr/bin/python3

""" module docstring """
import os
import sys
import argparse
import feedparser
import questionary
import requests

from striptags import strip_tags

parser = argparse.ArgumentParser(prog='dlp', description='Podcast Downloader')
parser.add_argument('-f','--feed', nargs='?', help='URL of podcast\' RSS feed')
parser.add_argument('-p','--podcasts', nargs='?',\
        help='Select from list of podcasts in file [-p FILENAME]',\
        default=True)
# parser.add_argument('-e','--episodes', nargs='?',\
        # help='Select episodes from podcast', default=False)
parser.add_argument('-q','--quiet', nargs='?',\
        help='Do not list podcast episode details', default=False)
parser.add_argument('-d','--download', nargs='?',\
        help='Download selected podcast episodes', default=False)
args = parser.parse_args()

""" default podcast filename: dlp.list """
PODCAST_LIST_FILENAME = 'dlp.list'
if PODCAST_LIST_FILENAME not in os.listdir('.'):
    sys.exit('dlp.py must me run in same directory as "dpl.list"')

def get_podcast_list(filename):
    """ function docstring """
    podcast_list = []
    with open(filename, encoding="utf-8") as f_i:
        for l_i in f_i:
            podcast_list.append(l_i.strip())

    return podcast_list

def get_episodes(podcast_url):
    """ function docstring """
    episode_list = []
    parsed_rss = feedparser.parse(podcast_url)
    for podcast_entry in parsed_rss.entries:
        episode_list.append(podcast_entry)
    return episode_list

def select_from_file(filename):
    """ function docstring """
    podcast_list = get_podcast_list(filename)

    podcast_selected = questionary.select("Select your podcast...", choices=podcast_list).ask()

    return podcast_selected

def select_episodes(episodes_selected):
    """ function docstring """
    episode_details = []
    for e_i in range(len(episodes_selected)):
        episode_details.append(str(e_i) + ' - ' + episodes[e_i]['title']\
                + '|' + episodes[e_i]['published'])

    selected_strings = questionary.checkbox("Select your episodes...",\
            choices=episode_details).ask()

    selected_episode_list = []
    for e_i in selected_strings:
        i_i = int(e_i.split()[0])
        selected_episode_list.append(episodes[i_i])

    return selected_episode_list

def list_episodes(episode_list):
    """ function docstring """
    for podcast_entry in episode_list:
        print('[title]:       ', podcast_entry['title'])
        print('[published]:   ', podcast_entry['published'])
        print('[summary]:     ', strip_tags(podcast_entry['summary']))
        print('[description]: ', strip_tags(podcast_entry['description']))
#       print('[content[0]]:  ', strip_tags(podcast_entry['content'][0]['value']))
#       print('[content[1]]:  ', strip_tags(podcast_entry['content'][1]['value']))
        print('[href]:        ', podcast_entry['enclosures'][0].href)

def rename_filename(filename):
    """ function docstring """
    forbiden_characters = '<>:"/|\\?*&'
    for replace_character in forbiden_characters:
        filename = filename.replace(replace_character, '_')
    return filename

def download_episode(podcast_entry):
    """ function_docstring """
    filename = str(podcast_entry['enclosures'][0].href).rsplit('/', maxsplit=1)[-1]
    filename = rename_filename(filename)
    print(filename)
    dlreq = requests.get(podcast_entry['enclosures'][0].href)
    with open(filename, 'wb') as d_l:
        d_l.write(dlreq.content)

print('| feed=' + str(args.feed),
 '| podcasts=' + str(args.podcasts),
  '| quiet=' + str(args.quiet),
   '| download=' + str(args.download))

if not args.feed:
    if args.podcasts or args.podcasts is None:
        PODCAST_LIST_FILENAME = 'dlp.list'
    else:
        PODCAST_LIST_FILENAME = args.podcasts

    selected_podcast = select_from_file(PODCAST_LIST_FILENAME)
    rss_url = selected_podcast.split()[0]

else:
    rss_url = args.feed
print(rss_url)

episodes = get_episodes(rss_url)
selected_episodes = select_episodes(episodes)

if not args.quiet:
    list_episodes(selected_episodes)

if args.download:
    for entry in selected_episodes:
        print('downloading: ', entry['title'], '\nURL: ', entry['enclosures'][0].href)
        download_episode(entry)
