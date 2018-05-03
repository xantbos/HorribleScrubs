# HorribleScrubs

Scrapes horriblesubs' RSS feeds for new releases and then sends and embed response to the designated channels.
Users may opt-in server or DM channels to recieve the notifications.

The backend magnetlink provider is a self-hosted solution which handles the content as a GET response.
It then sanitizes the data (GET isn't terribly secure) and then displays a clickable magnet link for the end user.

Since discord doesn't support magnet links any more, this was the way I decided to go about it.

utils.filemg is included.
utils.checks is included.

# Usage

* If you already have a working bot

Download the core horriblescrubs.py file and put it wherever your cogs go, and ensure your setup file is configured with the needed values. Modify as you need I guess.

* If you do not have a working bot

Download this entire package and get started. There is a skeleton main.py so this can be used as a standalone bot.