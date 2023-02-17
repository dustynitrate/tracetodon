# tracetodon

A simple, easy-to-run Mastodon bot to post procedurally-generated text using tracery. This bot is geared towards first-time botmakers or anyone who wants to crank out a very simple bot in a matter of minutes that they can then trigger using their method of choice.

## a note about the readme
If you're an experienced botmaker and know to schedule your bot using your chosen method, this readme is for you. If not, use `readme.md`.

## how it's written
The bot is written in Python 3 and uses [Tracery](https://pypi.python.org/pypi/tracery) and [Mastodon.py](https://github.com/halcy/Mastodon.py).  It was adapted from [duxovni's tracerybot](https://github.com/duxovni/tracerybot), which was in turn adapted from [sipb's mastodon autoresponder](https://github.com/sipb/mastodon-bot-autoresponder).

## what it does
tracetodon toots text generated using your tracery grammar; it does not check or respond to notifications/interactions. A scheduling function via a defined interval and `sleep()` is not included, so you'll use your preferred method of scheduling e.g. cron to set the interval for prompting the bot. 

## setting up the bot
### clone this repo
```
git clone git@github.com:dustynitrate/tracetodon.git
```
### set up + activate your virtual environment
```
virtualenv -p python3 env
source env/bin/activate
```
### install dependencies
```
pip install -r requirements.txt
```
### add your grammar
Paste your tracery grammar into `grammar.json`. Your grammar should look something like this:
```
{
	"mysteryword": [
		"mystery",
		"clue",
		"secret"

	],
	"descriptor": [
		"hidden",
		"haunted",
		"strange"
	],
	"noun": [
		"key",
		"album",
		"robot",
		"clock",
		"diary",
		"charm"
	],
	"origin": [
		"Nancy Drew and the #mysteryword# of the #descriptor# #noun#"
	]
}
```
### set up your application on mastodon
Designate your bot's account as a bot in "Profile":
```
[✓] This is a bot account
```
Go to Preferences, select Development, add "New application", and fill out the following:
```
Application name: [your bot's name here]
[✓] read
[✓] write
[✓] follow
```
### grab your key/secret/token
Grab the following from the Application you just set up:
```
Client key
Client secret
Your access token
```

### grab your key/secret/token & update the config
The bot is configured in config.json. The config will look like this, but with your values subbed in:

```
{
    "base_url": "https://botsin.space",  
    "client_id": "2wd...72x",
    "client_secret": "8d7...9s0",
    "access_token": "2fg...d20",  
    "grammar_file": "grammar.json"
}
```

All the keys are mandatory:

* `base_url`: Instance hosting the bot, e.g. `https://botsin.space`
* `client_id`: `Client Key`
* `client_secret`: `Client secret`
* `access_token`: `Your access token`
* `grammar_file`: Filepath to your grammar file.

### run the bot!
```
python3 tracetodon.py
```
If you want the bot to run at a certain frequency, you can write a little shell script to hit the bot:
```
cat > run_tracetodon.sh
#!/bin/[your shell here]
cd ./tracetodon
python3 tracetodon.py
```
And then add it to crontab; this example runs the every 4 hours.
```
0 */4 * * * ./run_tracetodon.sh
```

Or you can skil the shell script and make `tracetodon.py` executable with something like `#!/usr/bin/env python3`.
