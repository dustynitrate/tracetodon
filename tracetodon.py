import argparse
import json
import logging
import os
import os.path
from mastodon import Mastodon
import tracery
from tracery.modifiers import base_english

class Config:
    def __init__(self, path):
        self.path = os.path.abspath(os.path.expanduser(path))

        with open(self.path) as f:
            self.from_dict(json.load(f))

    def from_dict(self, json):
        self.base_url = json['base_url']
        self.client_id = json['client_id']
        self.client_secret = json['client_secret']
        self.access_token = json['access_token']
        self.grammar_file = json['grammar_file']

def get_api(config):
    return Mastodon(client_id=config.client_id,
        client_secret=config.client_secret,
        api_base_url=config.base_url,
        access_token=config.access_token)

class SimpleBot:
    def __init__(self, config):
        self.config = config
        self.api = get_api(self.config)

        with open(self.config.grammar_file) as f:
            self.grammar = tracery.Grammar(json.load(f))
        self.grammar.add_modifiers(base_english)

    def post_toot(self):
        attempts_remaining = 10
        while attempts_remaining:
            toot = self.grammar.flatten("#origin#")
            if len(toot) <= 500:
                break
            attempts_remaining -= 1

        if attempts_remaining == 0:
            logging.debug("Couldn't generate toot")
            return

        self.api.status_post(toot, visibility='public')

    def run(self):
        self.post_toot()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', help='File to load the config from.',
        default='config.json')

    args = parser.parse_args()

    config = Config(args.config)

    bot = SimpleBot(config)
    bot.run()

if __name__ == '__main__':
    main()
