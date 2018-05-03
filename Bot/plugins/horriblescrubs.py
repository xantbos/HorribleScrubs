import os, sys, io
import asyncio
import json
import requests
import urllib.parse
import discord
from discord.ext import commands
from bs4 import BeautifulSoup

from utils.filemg import returnJsonUnicode, setUnicodeData

from utils.checks import (
    is_owner,
	server_moderator
)

# Core class cog file
# Author: 	Xant
# @version 	1.0
# @since 	1.0

#@desc
#  Scrapes horriblesubs' RSS feeds for new releases
#  and then sends and embed response to the designated
#  channels. Users may opt-in server or DM channels
#  to recieve the notifications.

#  The backend magnetlink provider is a self-hosted
#  solution which handles the content as a GET response,
#  sanitizes the data and then displays a clickable
#  magnet link for the end user.

#  Since discord doesn't support magnet links any more,
#  this was the fastest way to go about it.
#----------------------------------------------------

class HorribleScrubs:

#Init functions and debugging tools
#----------------------------------------------------

    def __init__(self, bot):
        # we declare most of our variables here, allowing easy modification later on
		
        # the _sourcemagnethost value requires backend that
        # takes the magnetname and magnetlink arguments
        # in GET, and decodes them for usage. It's for php.
        # You can leave this empty if you're unable to 
        # prepare a host for this functionality, it will be skipped.
		
        self.bot = bot
        self.folderDir = "files\\optin\\"
        self.fileName = "optin"
        self._checkinterval = 10
        self._sourcemagnethost = ""
        self._DEFVALS = ["480", "720", "1080"]
        self._KNOWN480LIST = []
        self._KNOWN720LIST = []
        self._KNOWN1080LIST = []
        self._ROOTLIST = ['http://horriblesubs.info/rss.php?res=sd', 'http://horriblesubs.info/rss.php?res=720', 'http://horriblesubs.info/rss.php?res=1080']
        self._KNOWNLISTS = [self._KNOWN480LIST, self._KNOWN720LIST, self._KNOWN1080LIST]
        self.bot_init()

    @commands.check(is_owner)
    @commands.command(name="debugscrubber", pass_context=True, hidden=True)	
    async def bot_scrubber_debug(self, ctx):
        streamtype=1
        uValues = returnJsonUnicode(self.folderDir, self.fileName)
        newNews = self.bot_scrubber_checks_for_content(self._ROOTLIST[streamtype])
        newNews = newNews[:1]
        for channel in uValues[self._DEFVALS[streamtype]]["channelID"]:
            thisChannel = discord.Object(id=channel)
            for i in newNews:
                links = i.splitlines()
                em = self.generate_embed_from_package(links, "New {}p Stream".format(self._DEFVALS[streamtype]))
                try:
                    await self.bot.send_message(thisChannel, embed=em)
                except:
                    pass
        self.first_run_to_fill_lists(streamtype)
        pass
		
    def bot_init(self):
        # init that is called during the core __init__ for clarity purposes
        self.bot_horriblescrubber_creates_structured_json(self.fileName)
        [self.first_run_to_fill_lists(i) for i in range(3)]
        [asyncio.ensure_future(self.timer_for_update_check(i)) for i in range(3)]
		
# Interaction functions
#----------------------------------------------------

    @commands.check(server_moderator)
    @commands.command(name="stream", pass_context=True)
    async def bot_adds_channel_to_stream_notifications(self, ctx, resolution, decision):
        """Used to add a server or private channel to the notification system"""
        if not resolution in self._DEFVALS:
            await self.bot.say("You must use one of the valid resolutions: {}".format(" ".join(self.DEFVALS)))
            return
        if decision == "add":
            self.bot_horriblescrubber_handles_optin(self.fileName, resolution, ctx)
            await self.bot.say("This channel has been set up to receive {}p stream notifications.".format(resolution))
            try:
                await self.bot.delete_message(ctx.message)
            except:
                pass
        elif decision == "remove":
            self.bot_horriblescrubber_handles_optout(self.fileName, resolution, ctx)
            await self.bot.say("This channel has been removed from the {}p stream notifications.".format(resolution))
            try:
                await self.bot.delete_message(ctx.message)
            except:
                pass
        else:
            await self.bot.say("You must either use `add` or `remove` after the resolution.")
            return
		
		
# First run functions to fill content lists
#----------------------------------------------------

    def first_run_to_fill_lists(self, rootid):
        self._KNOWNLISTS[rootid] = list(self.bot_scrubber_checks_for_content(self._ROOTLIST[rootid]))

# Update calls
#----------------------------------------------------
	
    def check_for_new_content(self, listid):
        currentAnnounces = self.bot_scrubber_checks_for_content(self._ROOTLIST[listid])
        currentAnnounces = [i for i in currentAnnounces if i not in self._KNOWNLISTS[listid]]
        return currentAnnounces
		
# Actual function that parses the rss data
#----------------------------------------------------
		
    def bot_scrubber_checks_for_content(self, roothtml):
        page = requests.get(roothtml)
        page.encoding = 'utf-8'
        source = page.text
        soup = BeautifulSoup(source, "lxml")
        splitSoup = soup.find_all('item')
        updateText = []
        for i in splitSoup:
            updateText.append("{}\n{}\n{}".format(i.contents[0].get_text(), i.contents[2], i.contents[4].get_text()))
        return updateText

# Generator functions		
#----------------------------------------------------
	
    def generate_embed_from_package(self, pack, headertype):
        em = discord.Embed(title="Horribly Scrubbed", description="", colour=0x00AE86)
        em.add_field(name="{} Magnet".format(headertype), value="**Filename**\n{}\n\n**Date Published**\n{}".format(pack[0], pack[2]))
        em.set_footer(text="Crunchyroll shouldn't forget its roots")
        thisURL = self.generate_html_get_for_magnet(pack[0], pack[1])
        if not thisURL == "":
            em.url = thisURL
        return em
		
    def generate_html_get_for_magnet(self, magnetname, magnetlink):
        if not _sourcemagnethost == "":
            return self._sourcemagnethost + urllib.parse.urlencode({'magnetname' : magnetname, 'magnetlink' : magnetlink})
        return ""

# File management
#----------------------------------------------------

    def bot_horriblescrubber_handles_optin(self, fileHandle, resolution, ctx):
        uValues = returnJsonUnicode(self.folderDir, fileHandle)
        if not ctx.message.channel.is_private:
            if not ctx.message.channel.id in uValues[resolution]["channelID"]:
                uValues[resolution]["channelID"] = uValues[resolution]["channelID"] + [ctx.message.channel.id]
        else:
            if not ctx.message.author.id in uValues[resolution]["channelID"]:
                uValues[resolution]["channelID"] = uValues[resolution]["channelID"] + [ctx.message.author.id]
        setUnicodeData(uValues, self.folderDir + fileHandle)
	
    def bot_horriblescrubber_handles_optout(self, fileHandle, resolution, ctx):
        uValues = returnJsonUnicode(self.folderDir, fileHandle)
        if not ctx.message.channel.is_private:
            if ctx.message.channel.id in uValues[resolution]["channelID"]:
                uValues[resolution]["channelID"].remove(ctx.message.channel.id)
        else:
            if ctx.message.author.id in uValues[resolution]["channelID"]:
                uValues[resolution]["channelID"].remove(ctx.message.author.id)
        setUnicodeData(uValues, self.folderDir + fileHandle)
		
    def bot_horriblescrubber_creates_structured_json(self, fileHandle):
        if not os.path.isfile(self.folderDir + fileHandle + '.json'):
            data = {}
            for res in self._DEFVALS:
                data[res] = {'channelID' : []}
            setUnicodeData(data, self.folderDir + fileHandle)
	
# Timer functions
#----------------------------------------------------
		
    async def timer_for_update_check(self, streamtype):
        while not self.bot.is_logged_in:
            await asyncio.sleep(5)
        preString = "Starting {}p Scrubber Timer...".format(self._DEFVALS[streamtype])
        print("{:<35}".format(preString), end="")
        print("\tSuccess")
        self.first_run_to_fill_lists(streamtype)
        doNothing = True
        while doNothing:
            await asyncio.sleep(self._checkinterval)
            newNews = self.check_for_new_content(streamtype)
            if(len(newNews) > 0):
                uValues = returnJsonUnicode(self.folderDir, self.fileName)
                for channel in uValues[self._DEFVALS[streamtype]]["channelID"]:
                    thisChannel = discord.Object(id=channel)
                    for i in newNews:
                        links = i.splitlines()
                        em = self.generate_embed_from_package(links, "New {}p".format(self._DEFVALS[streamtype]))
                        try:
                            await self.bot.send_message(thisChannel, embed=em)
                        except:
                            pass
                self.first_run_to_fill_lists(streamtype)
		
#Setup cog		
def setup(bot):
    bot.add_cog(HorribleScrubs(bot))