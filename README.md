# HorribleScrubs

Scrapes horriblesubs' RSS feeds for new releases and then sends and embed response to the designated channels.
Users may opt-in server or DM channels to recieve the notifications.

The backend magnetlink provider is a self-hosted solution which handles the content as a GET response.
It then sanitizes the data (GET isn't terribly secure) and then displays a clickable magnet link for the end user.

Since discord doesn't support magnet links any more, this was the way I decided to go about it.