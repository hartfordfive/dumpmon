'''
helper.py - provides misc. helper functions
Author: Jordan

'''

import requests
import settings
from time import sleep, strftime
import logging


r = requests.Session()


def download(url, headers=None):
    if not headers:
        headers = None
    if headers:
        r.headers.update(headers)
    try:
        response = r.get(url).text
    except requests.ConnectionError:
        logging.warn('[!] Critical Error - Cannot connect to site')
        sleep(5)
        logging.warn('[!] Retrying...')
        response = download(url)
    return response


def log(text):
    '''
    log(text): Logs message to both STDOUT and to .output_log file

    '''
    print(text)
    with open(settings.log_file, 'a') as logfile:
        logfile.write(text + '\n')


def build_tweet(paste):
    '''
    build_tweet(url, paste) - Determines if the paste is interesting and, if so, builds and returns the tweet accordingly

    '''
    tweet = None
    if paste.match():
        tweet = paste.url
        if paste.type == 'db_dump':
            if paste.num_emails > 0:
                tweet += ' Emails: ' + str(paste.num_emails)
            if paste.num_hashes > 0:
                tweet += ' Hashes: ' + str(paste.num_hashes)
            if paste.num_hashes > 0 and paste.num_emails > 0:
                tweet += ' E/H: ' + str(round(
                    paste.num_emails / float(paste.num_hashes), 2))
            tweet += ' Keywords: ' + str(paste.db_keywords)
        elif paste.type == 'google_api':
            tweet += ' Found possible Google API key(s)'
        elif paste.type in ['cisco', 'juniper']:
            tweet += ' Possible ' + paste.type + ' configuration'
        elif paste.type == 'ssh_private':
            tweet += ' Possible SSH private key'
        elif paste.type == 'honeypot':
            tweet += ' Dionaea Honeypot Log'
        elif paste.type == 'pgp_private':
            tweet += ' Found possible PGP Private Key'
        tweet += ' #infoleak'
    if paste.num_emails > 0:
        print(paste.emails)
    return tweet
    
    
 def dump_to_file(json_data,dump_site):
    '''
    Writes the obtained data to a text file
    {
    'pid' : paste.id,
    'text' : paste.text,
    'emails' : paste.emails,
    'hashes' : paste.hashes,
    'num_emails' : paste.num_emails,
    'num_hashes' : paste.num_hashes,
    'type' : paste.type,
    'db_keywords' : paste.db_keywords,
    'url' : paste.url
    }
    '''
    with open("data_{0}.txt".format(dump_site), "a") as f:
        line_item = "paste_id={0}, text={1}, emails={2}, hashes={3}, num_emails={4}, num_hashes={5}, type={6}, db_keywords={7}, paste_url={8}"
        f.write(line_item)
