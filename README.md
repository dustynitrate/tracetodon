# tracetodon

A simple, easy-to-run Mastodon bot to post procedurally-generated text using tracery. This bot is geared towards first-time botmakers or anyone who wants to crank out a very simple bot in a matter of minutes.

## how it's written
The bot is written in Python 3 and uses [Tracery](https://pypi.python.org/pypi/tracery) and [Mastodon.py](https://github.com/halcy/Mastodon.py).  It was adapted from [duxovni's tracerybot](https://github.com/duxovni/tracerybot), which was in turn adapted from [sipb's mastodon autoresponder](https://github.com/sipb/mastodon-bot-autoresponder).

## what it does
tracetodon simply toots/publishes text generated using your tracery grammar; it does not check or respond to notifications/interactions.

## about this guide
This guide walks the reader through configuring the bot with a tracery grammar and mastodon keys, and then instructs on using a shell script scheduled using cron to run the bot at a defined frequency.

My intention with this expanded readme and particular method of bot-ification was to walk the reader through a method that was fairly easy for a beginner/novice to set up, and did not require much intervention aside from pasting in the grammar, editing the config, and scheduling the bot. 

The other, sneaky intention was to help prospective bot-makers become more comfortable using tools that will come in handy for advanced bot-making. :D

If you already know how to do all of this and/or this guide is too hand-holdy for you, consult `readme_advanced.md` instead.

## requirements
This guide assumes the reader has written a tracery grammar but has little/no familiarity with how to bot-ify it. This readme walks the bot-maker though one method of botmaking, though there are countless others.  Basic understanding of the command line and of python is helpful but not entirely necessary.

This guide outlines a method that requires the use of a unix-like system, e.g. MacOS or your preferred flavour of Linux. A separate readme on using Windows may be added at a later date.

We'll focus on getting the bot running locally, then touch on other options for hosting it.

## setup
Before you customize the bot with your own grammar, let's go ahead and get it configured to run.
### clone this repo
You can clone the repo using command line/terminal or by downloading directly from the repo page.

#### From terminal
Open terminal and check to be sure you have git:

```
git --version
```

you should get something like this back:

```
git version 2.38.1
```

If you get a message that git is an unknown command, that means you need to install git first. See [this guide](https://github.com/git-guides/install-git) for multiple methods installing git depending on your OS. 

If/when git is installed, type this into terminal:

```
git clone git@github.com:dustynitrate/tracetodon.git
```
This will save the repo in your home directory. e.g.

```
Mac: /Users/[your_user]
Linux: /home/[your_user]
``` 

#### From repo page

Alternatively, if you don't want to use terminal, you can download the zip directly from the repo page by selecting Code/Download ZIP [from the repo](https://github.com/dustynitrate/tracetodon).

To run/test locally without having to mess with the filepaths later on, make sure it's saved to your home directory. e.g.

```
Mac: /Users/[your_user]
Linux: /home/[your_user]
```

### set up a virtual environment for Python and activate it
Next, we need to set up a virtual environment for the bot and activate it. We use a virtual environment so the bot is its own self-contained application with its own dependencies; that way we aren't accidentally messing with other scripts or your operating system's global Python. 

Open terminal and navigate to the repo you just downloaded:
```
cd tracetodon
```

Then type the following:
```
virtualenv -p python3 env
```
Then hit enter. To activate the virtual environment, type the following:
```
source env/bin/activate
```
And hit enter again. You should have `(env)` at the beginning of your command prompt now.

### install the dependencies
Required dependencies are in `requirements.txt`, so all you need to do is use `pip` to install them.

```
pip install -r requirements.txt
```

## getting ready to run
Now that we have our copy of tracetodon, let's get it customized with your grammar and point it to your bot's Mastodon account.

### add your grammar
All you need to do to get the bot customized with your tracery grammar is paste the grammar into `grammar.json`. Your grammar should look something like this:
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
The bot flattens `#origin#` when generating the toot, so make sure the meat of your grammar is there.
Your rules can be called whatever you want and expansions contain whatever your want, so long as they're passed to `#origin#`.

you can paste your grammar into `grammar.json` using your text editor of choice, or use nano or vim to do so from terminal. 
For example, from the tracetodon directory, type `vim grammar.json` to open `grammar.json` using vim, the hit `i` to insert, paste your grammar in, and then hit (one at a time) `esc`, `:`, `w`, then `q` to exit.


Since most instances limit toots to 500 characters, make sure the text generated is less than or equal to that; the bot will try 10 times to generate a toot under the character limit, but after that it will stop.

###set up your application on mastodon
If you haven't already registered/requested your bot's account on your instance of choice (eg [botsin.space](https://botsin.space/)), do that now & login to the web client. Time to set up our app!

First head over to "Profile" and select the following to signal to others that the account is a bot:
```
[✓] This is a bot account
```

Then head over to Preferences, select Development from the left sidebar, smash that "New application" button, and fill out the following:

```
Application name: [your bot's name here]
[✓] read
[✓] write
[✓] follow
```

Then hit submit! You'll get an "application successfully created" message and your app will appear in the application list now. Go ahead and select it now so we can grab our keys/secret/token.

###grab your key/secret/token
Go ahead and grab the following from the Application you just set up:
```
Client key
Client secret
Your access token
```

Goes without saying, but just in case: NEVER SHARE OR PUBLISH THESE. You can always regenerate them later and re-edit the config if you suspect they have been compromised.

Now that you have those, let's update the config so your bot can toot!

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

All the keys are mandatory. Here's what each of those keys are:

* `base_url`: The instance where you're running your bot. e.g. https://botsin.space
* `client_id`: Paste in the alphanumeric code you just grabbed from `Client Key`
* `client_secret`: Paste in the alphanumeric code you just grabbed from `Client secret`
* `access_token`: Paste in the alphanumeric code you just grabbed from `Your access token`
* `grammar_file`: Filepath to your grammar file. Unless you've made modifications to this bot, keep it as `grammar.json`

Again, you can add the values using your text editor of choice, or use vim or similar from terminal.

## Test the bot
Before scheduling, let's manually hit the bot to see if the output is what we want! 

Open the terminal and navigate to the directory where the bot lives. If it's in your home directory, do this:

```
cd tracetodon
```

Then run the script with this:
```
python3 tracetodon.py
```
It'll look like nothing happened in terminal; but if you head over to your bot's page, you should see the toot it generated!

##Bot-ify it
Now that we know the bot works, let's  get it set up to run at a pre-determined interval.

To do this we're going to first write a simple shell script that'll tap the bot, and then we'll use cron to schedule that script at whatever interval we want to.

###write the shell script
Navigate back to your home directory if you're not already there:
```
cd ~
```
Once there, let's create our shell script. First, type/paste this into the terminal:
```
cat > run_tracetodon.sh
```
Then hit enter. Copy/paste the following (our simple shell script) in:
```
#!/bin/bash
cd ./tracetodon
python3 tracetodon.py
```
And hit Enter followed by Ctrl+D to exit

To break it down a bit:

`#!/bin/bash` tells the parent shell which interpreter/shell to use to run the script. We're using bash here.

`cd ./tracetodon` changes the directory to where our bot is.

`python3 tracetodon.py` runs the bot.

Alternatively, you can navigate to your home directory and create/edit the `.sh` file there using a text editor.

### make it executable
Finally, we need to make the script executable. We do this using `chmod`. We're going to make it executable for all users:
```
chmod -x run_tracetodon.sh 
```

To test if your script works, run the following from your home directory:
```
./run_tracetodon.sh 
```
You should see the bot account post a toot!

### schedule using cron
Assuming you haven't used crontab before, you'll need to create a crontab file. To do that, do this:

```
crontab -e
```
If you haven't edited crontab before, you'll get an intimidatingly blank file opened in vim. 

This is where we'll put a cron expression and the path to our script.

To do that, hit `i`. You'll see `INSERT` at the bottom of the window. 

Then, let's paste in the below. This example runs at 0 minutes past the hour, every 2 hours.
```
0 */2 * * * ./run_tracetodon.sh
```
Then press the following keys in order (not holding them down) to exit vim: `esc`, `:`, `w`, then `q`.

To see if your cron job is there, you can view a list of jobs with the following:
```
crontab -l
```
If you want to modify the frequency to suit your needs, you can use [the cron expression generator by Cronhub](https://crontab.cronhub.io/) to generate an expression to paste in before the filepath, and can always edit crontab using `crontab -e`. 

Now we sit back and wait... and if you check your bot's account at the scheduled time, you should see the posted toot!

## What next?
Well, you could just let your bot run on your local machine forever... but that also requires your machine being on/active, so might not be the most practical choice. But, hey, less-than-perfect and erratic bots also have their charm.

However, if you were able to run through this extended readme successfully, you can get your bot hosted somewhere with little extra effort! Some of my favourite beginner-friendly options that offer a free or low-cost tier for hosting include:

[PythonAnywhere](https://www.pythonanywhere.com). Free tier is just fine if you only want your bot posting once or twice a day, plus scheduled tasks makes setting the bot to run a breeze.

[Pipedream](https://pipedream.com/). Offers a free tier and easy methods for automation and scheduling custom intervals.

[DigitalOcean](https://www.digitalocean.com/). Offers a $5/month VPS, and it's not too hard to find referral credits to get you a month or two freee.

[AWS Lambda](https://aws.amazon.com/lambda/). Offers a free tier.

[Google Cloud Platform](https://cloud.google.com/free/). Offers a free tier.

## FAQ
#### How do I stop my bot?
You can remove the cron job entirely by opening crontab with `crontab -e`, hitting `i` to insert, deleting the line with the job, then exit vim with:  To check if the cron job was removed, use `crontab -l`.
`esc`, `:`, `w`, then `q`.
#### Why cron when there's sleep()?
I opted for using cron job instead of a sleep loop so beginners wouldn't need to touch the bot's code to alter the frequency. Though there is an argument that shell scripts and cron are just as confusing; but, hey, now you can say you have experience with both. ;) 
This also keeps the cost low both in terms of money dollars (you can run it a couple of times a day on something like PythonAnywhere for free with no danger of going into the tarpit, or tap the bot at a scheduled frequency on any other service too) and CPU use if running locally (though a bot like this is not really all that resource-intensive).

#### Why shell script when you could just make the python executable for crontab?
Yes, yes, I know we could've skipped the shell script and stuck something like `#!/usr/bin/env python3` at the top of `tracetodon.py`; but that method would've also required a lengthier command in crontab and some diverging paths depending on the user's system/setup, and I was trying to beginner-proof this as much as possible.

#### Why did you put all this in a readme instead of the project wiki?
There is an argument that something like this is way too long for a readme and is probably better-suited to the wiki... but I was thinking of the beginner hear, and how they might find it useful to pull down the whole tutorial for reference when cloning the repo; makes things a little more self-contained, too.
