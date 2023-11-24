#!/usr/bin/env python3
""" module docstring """
from __future__ import print_function
import os
import shutil
import datetime
import sys
import urllib
import argparse
import colorama
# import cPickle as pickle
import feedparser
from mutagen.id3 import ID3, TALB, TIT2, TDRC, TCON, COMM, ID3NoHeaderError
from progressbar import ProgressBar, Percentage, Bar,\
        RotatingMarker, ETA, FileTransferSpeed
#from MLStripper import strip_tags

# pod.py
__version__ = 2.0
__updated__ = 20161125

PCODES = {
    "BOLD" : "colorama.Style.BRIGHT",
    "DIM" : "colorama.Style.DIM",
    "ERROR"   : "colorama.Style.BRIGHT + colorama.Fore.RED",
    "DESC" : "colorama.Style.BRIGHT + colorama.Fore.MAGENTA",
    "DOTPOD"  : "colorama.Style.BRIGHT + colorama.Fore.BLUE",
    "PUBDATE" : "colorama.Style.BRIGHT + colorama.Fore.GREEN",
    "EPISODE" : "colorama.Style.BRIGHT + colorama.Fore.CYAN",
    "FILE" : "colorama.Style.BRIGHT + colorama.Fore.YELLOW",
    "URL" : "colorama.Style.BRIGHT + colorama.Fore.WHITE",
    "END" : "colorama.Style.RESET_ALL + colorama.Fore.RESET",
    }

def pod_error(pod):
    title = 'error in {}{}{}.'.format(PCODES['DOTPOD'], pod['title'], PCODES['END'])
    for error in pod['error']:
        e, message = error
        message = PCODES['ERROR'] + message + PCODES['END']
        print('{} | {}\n  {}'.format(title, str(e), message))

def get_selected_pod_list(podcast_home, pod_list):
    pods = []
    for pod_dir in pod_list:
        pod = {}
        pod['dir'] = os.path.join(podcast_home, pod_dir)
        pod['db'] = os.path.join(podcast_home, pod_dir, 'db')
        pod['epis'] = os.path.join(podcast_home, pod_dir, 'epis')
        pod['log'] = os.path.join(podcast_home, pod_dir, 'log')
        pod['rss'] = os.path.join(podcast_home, pod_dir, 'rss')
        pod['title'] = pod_dir[:-4]
        pod['url'] = os.path.join(podcast_home, pod_dir, 'url')
        # pod['pickle'] = os.path.join(podcast_home, pod_dir, 'pickle')
        pod['error'] = []

        for i in ['db', 'epis', 'log', 'rss', 'url']:
            if not os.path.isfile(pod[i]):
                exit('error: .pod {}{}{} does not include {}{}{}'.format(
                        PCODES['DOTPOD'], pod_dir,
                        PCODES['END'], PCODES['FILE'], pod[i], PCODES['END']))

        pods.append(pod)
    return pods

def get_pod_list(podcast_home):
    pods = []
    for pod_dir in os.listdir(podcast_home):
        if pod_dir.endswith('.pod'):
            pod = {}
            pod['dir'] = os.path.join(podcast_home, pod_dir)
            pod['db'] = os.path.join(podcast_home, pod_dir, 'db')
            pod['epis'] = os.path.join(podcast_home, pod_dir, 'epis')
            pod['log'] = os.path.join(podcast_home, pod_dir, 'log')
            pod['rss'] = os.path.join(podcast_home, pod_dir, 'rss')
            pod['title'] = pod_dir[:-4]
            pod['url'] = os.path.join(podcast_home, pod_dir, 'url')
            #pod['error'] = []

            for i in ['db', 'epis', 'log', 'rss', 'url']:
                if not os.path.isfile(pod[i]):
                    pod['error'].append((
                        IOError, 'file not found: "{}".'.format(
                            os.path.basename(pod[i]))))
                    pod_error(pod)

            pods.append(pod)
    return pods

def get_updated(pod):
    # pubDate_str = 'Mon, 31 Dec 2099 ...'
    # updated_str = 'updated: 20991231'
    with open(pod['log'], 'r') as log:
        lines = log.readlines()

    count = len(lines) - 1
    if count < 1:
        update_line = 'rss updated: {}\n'.format('unknown')
    else:
        while count:
            update_line = lines[count]
            if 'rss updated: ' in update_line:
                break
            count -= 1

    count = len(lines) - 1
    if count < 1:
        download_line = 'download: {}\n'.format('unknown')
    else:
        while count:
            download_line = lines[count]
            if 'download: ' in update_line:
                break
            count -= 1

    if 'rss updated: ' not in update_line: update_line = ' unknown'
    if 'download: ' not in download_line: download_line = ' unknown'

    # return date in format YYYYMMDD:
    return update_line.split()[-1].rstrip(), download_line.split()[-1].rstrip()

def get_new_episodes(pod):
    updated, downloaded = get_updated(pod)
    # print(' rss last updated: {}{}{} last download: {}{}{}'.format(
    #       PCODES['PUBDATE'], updated, PCODES['END'],
    #       PCODES['PUBDATE'], updated, PCODES['END']))

    # load db
    try:
        if pod['title'] == 'starshipsofa':
            db = open(pod['db'], 'r').read().replace(
                'media.mp3', '').splitlines()
        else:
            db = open(pod['db'], 'r').read().splitlines()
    except Exception as e:
        print('{}error{} in {}{}{}\n  failed to read db file. {}\n  {}{}{}'.format(PCODES['ERROR'], PCODES['END'], PCODES['DOTPOD'], pod['title'],
                      PCODES['END'], url.rstrip(), PCODES['DESC'],
                      str(e), PCODES['END']))
        return []
    # load url
    with open(pod['url'], 'r') as f:
        url = f.read()
    # download new rss
    try:
        rss_file, headers = urllib.urlretrieve(url, pod['rss'])
    except Exception as e:
        print('{}error{} in {}{}{}\n  failed to download rss. {}\n  {}{}{}'.format(PCODES['ERROR'], PCODES['END'], PCODES['DOTPOD'], pod['title'],
                      PCODES['END'], url.rstrip(), PCODES['DESC'],
                      str(e), PCODES['END']))
        return []
    # read rss
    with open(pod['rss'], 'r') as f:
        rss = f.read()

    parsed_rss = feedparser.parse(rss)
    episodes = []
    for entry in parsed_rss.entries:
        try:
            if entry.enclosures and entry.enclosures[0].href:
                episodes.append(entry)
        except Exception as e:
            print('{}error{} in episode rss\n  {}'.format(
                PCODES['ERROR'], PCODES['END'], str(e)))

    new_episodes = []
    for episode in episodes:
        url      = episode.enclosures[0].href
        url_file = url.split('/')[-1]
        title = episode.title.replace(' ', '_').format(
            'ascii', 'ignore')
        title = title.replace('/', '-')
        title = title.replace(':', '-')

        if 'id' in episode.keys():
            id_string = episode.id
        else:
            id_string = title

        if url_file not in db:
            if title not in db:
                if id_string not in db:
                    new_episodes.append(episode)

    # update log
    with open(pod['log'], 'a') as log:
        log.write('rss updated: {}\n'.format(
            datetime.date.today().strftime('%Y%m%d')))

    return new_episodes

def download_episode(pod, episode, progress= False):
    def progress_bar_retrieve(url, file_path):
        widgets = [' ', Percentage(), ' ', Bar(marker= RotatingMarker()), ' ',
                   ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets= widgets)
        (f, h) = (None, None)


        def dlProgress(count, block_size, total_size):
            if pbar.maxval is None:
                pbar.maxval = total_size
                pbar.start()

            pbar.update(min(count * block_size, total_size))
        try:
            (f, h) = urllib.urlretrieve(url, file_path, reporthook= dlProgress)
            pbar.finish()
        except Exception as e:
            #traceback.print_exc(file=sys.stdout)
                print(u'{}error{} downloading {}{}{}\n  {}{}{}'.format(
                    PCODES['ERROR'], PCODES['END'], PCODES['FILE'], file_path,
                    PCODES['END'], PCODES['DESC'], str(e), PCODES['END']))
                file_path = None

        return (f, h)

    def no_progress_bar_retrieve(url, file_path):
        (f, h) = (None, None)
        try:
            (f, h) = urllib.urlretrieve(url, file_path)
        except Exception as e:
                print(u'{}error{} downloading {}{}{}\n  {}{}{}'.format(PCODES['ERROR'], PCODES['END'], PCODES['FILE'], file_path, PCODES['END'], PCODES['DESC'], str(e), PCODES['END']))
                file_path = None

        return (f, h)

    url = episode.enclosures[0].href
    url_file = os.path.basename(url)
    file_path = os.path.join(pod['dir'], url_file)
    #progress = True # pod.py
    if progress:
        (f, h) = progress_bar_retrieve(url, file_path)
    else:
        (f, h) = no_progress_bar_retrieve(url, file_path)

    if not h:
        print('Trying wget...')
        import subprocess
        subprocess.check_output(['wget', '--output-document={}'.format(file_path), url])


    return file_path

def tag_and_rename(pod, episode, file_path):

    # pubDate='Sun, 31 Dec 2099 23:59:59 -0800'

    published_pieces = episode.published.split()[1:4]
    date_obj = datetime.datetime.strptime(
        '{} {} {}'.format(*published_pieces), '%d %b %Y')
    published = date_obj.strftime('%Y%m%d')

    title = episode.title.replace(' ', '_')
    title = title.replace('/', '').encode('ascii', 'ignore')
    title = title.replace(':', '-')
    title = title.replace('"', '')
    title = title.replace('?', '')

    desc = u'"{}"'.format(episode.description)

    url = episode.enclosures[0].href

    filename = os.path.basename(file_path)

    # new_filename -> published-title.mp3
    new_filename = u'{}-{}.mp3'.format(published, title)

    # tag episode
    try:
        eid3 = ID3(file_path)
    except ID3NoHeaderError as e:
        eid3 = ID3()

    eid3.add(TALB(encoding= 3, text= pod['title']))
    eid3.add(TIT2(encoding= 3, text= title))
    eid3.add(TDRC(encoding= 3, text= published[:4]))
    eid3.add(TCON(encoding= 3, text= u'Podcast'))
    eid3.add(COMM(encoding= 3, lang= 'ENG', desc= u'desc', text= desc))
    eid3.add(COMM(encoding= 3, desc= u'file', text= filename))

    eid3.save(file_path, v1=2)

    # rename downloaded file
    shutil.move(file_path, os.path.join(pod['dir'], new_filename))

    return new_filename

def log_episode(pod, episode, filename):
    '''
    /db
    /log
    /episode
    /pickle
    '''
    published_pieces = episode.published.split()[1:4]
    date_obj = datetime.datetime.strptime(
        '{} {} {}'.format(*published_pieces), '%d %b %Y')
    published = date_obj.strftime('%Y%m%d')

    if 'id' in episode.keys():
        episode['id'] = episode.id
    else:
        episode['id'] = episode.title

    epidict = {     'pub'   : published,
            'title' : u'{}'.format(episode.title),
            'desc'  : u'"{}"'.format(
                episode.description.replace('\n', '<br />')),
            'url'   : episode.enclosures[0].href,
            'file'  : filename,
            'id'    : episode.id }

    with open(pod['epis'], 'a') as epis:
        epis.write(u'PUB={} TITLE={} DESC={} URL={} FILE={}\n'.format(
            epidict['pub'], epidict['title'], epidict['desc'], epidict['url'],
            os.path.basename(epidict['file'])).encode(
                'ascii', 'ignore'))

    #with open(pod['pickle'], 'ab') as p:
    #    pickle.dump(epidict, p)

    with open(pod['db'], 'a') as db:
        title = epidict['title'].replace(' ', '_')
        title = title.replace('/', '-').encode('ascii', 'ignore')
        title = title.replace(':', '-')
        db.write(u'{}\n'.format(os.path.basename(epidict['url'])))
        db.write(u'{}\n'.format(title))
        db.write('{}\n'.format(epidict['id']))

    with open(pod['log'], 'a') as log:
        log.write('download: {}\n'.format(published))

    return epidict
'''
__main__
set podcast_home
load pods from podcast_home
iterate pod in pods:
    check updated rss
    get new episodes
    download new episodes + tag + rename
'''
if __name__ == "__main__":
    colorama.init()
    program_name = os.path.basename(sys.argv[0])
    program_version = "v{}".format(__version__)
    program_build_date = str(__updated__)
    program_version_message = "{} ({})".format(
        program_version, program_build_date)
    program_shortdesc = "%(prog)s: Archive Podcasts Automatically"
    program_license = "Free"

    # set podcast_home
    podcast_home = os.environ.get('PODCASTS')
    if not podcast_home:
        podcast_home = os.environ.get('PODCAST_HOME')
    if not podcast_home:
        exit(' env variable "PODCASTS" and/or "PODCAST_HOME" are not defined.')
    if not os.path.isdir(podcast_home):
        exit(' pod directory {} cannot be read.'.format(podcast_home))

    '''Command line options'''
    parser = argparse.ArgumentParser(
        description=program_license,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-d', '--dir', dest='podcast_home', action='store',
        default= podcast_home, help= 'PODCAST_HOME directory. [default: %(default)s]')
    parser.add_argument(
        '-p', '--pod', dest='podcast_home', action='store',
        default= podcast_home, help= 'PODCAST_HOME directory. [default: %(default)s]')
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help='no progress bar - use with cron [default: %(default)s]')
    parser.add_argument(
        "-c", "--cron", action="store_true",
        help="no progress bar - use with cron [default: %(default)s]")
    parser.add_argument(
        'dotpods', nargs='*', metavar= 'dotpod[.pod]',
        default= [], help= 'list of dotpods. [default: %(default)s]')

    # Process arguments
    args = parser.parse_args()
    if args.quiet:
        progress = False
    elif args.cron:
        progress = False
    else:
        progress = True

    if args.podcast_home:
        podcast_home = args.podcast_home

    dotpods = args.dotpods

    # load pods
    if len(dotpods) > 0:
        selected_pods = []
        for pod in dotpods:
            if not pod.endswith('.pod'):
                selected_pods.append(pod + '.pod')
            else:
                selected_pods.append(pod)

        pods = get_selected_pod_list(podcast_home, selected_pods)

    else:

        pods = get_pod_list(podcast_home)

    # iterate pod in pods
    for pod in pods:
        if pod['error']:
            pod_error(pod)
            continue

        podname = pod['title']
        header = u'{}{}{}: '.format(PCODES['DOTPOD'], podname, PCODES['END'])

        if progress:
            print(
                header + '{} {}{}{}'.format(
                    '=' * (78 - len(header) - len(podname)),
                    PCODES['DOTPOD'], podname, PCODES['END']))
        else: # pod.py --cron
            print(
                header + '{} '.format('=' * (78 - len(header) - len(podname))))

        new_episodes = get_new_episodes(pod)
        new_episodes.reverse()

        if not new_episodes:
            print(header + 'no new episodes.')
        else:
            for episode in new_episodes:
                print(
                    header + 'new episode in {}{}{}'.format(
                        PCODES['DOTPOD'], podname, PCODES['END']))
                published = header + 'published: {}{}{}'.format(
                    PCODES['PUBDATE'], episode.published, PCODES['END'])
                title = header + u'title: {}"{}"{}'.format(
                    PCODES['EPISODE'], episode.title, PCODES['END'])
                description = header + u'desc: {}{}{}'.format(
                    PCODES['DESC'], episode.description, PCODES['END'])
                url = header + 'url: {}{}{}'.format(
                    PCODES['URL'], episode.enclosures[0].href, PCODES['END'])
                print(published)
                print(title.encode('ascii', 'ignore'))
                print(description.encode('ascii', 'backslashreplace'))
                print(url)

                # download
                downloaded_episode = download_episode(
                    pod, episode, progress= progress)

                if not downloaded_episode:
                        continue

                try:
                    new_filename = tag_and_rename(pod, episode,
                            downloaded_episode)
                except IOError as e:
                    print('{}error{} in {}{}{}\n failed to tag_and_rename episode. {}\n {}{}{}'.format(PCODES['ERROR'], PCODES['END'], PCODES['DOTPOD'], pod['title'], PCODES['END'], url.rstrip(), PCODES['DESC'], str(e), PCODES['END']))
                    continue

                print(header + u'new tagged file: {}{}{}'.format(
                    PCODES['FILE'], os.path.join(
                        pod['dir'], new_filename), PCODES['END']))

                epidict = log_episode(pod, episode, new_filename)

# vim: set expandtab shiftwidth=4 tabstop=4 linebreak: #
