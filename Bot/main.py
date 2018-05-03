import sys
import discord
from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or
from utils import setup_file, user_agent

plugins = ["plugins.horriblescrubs"]

class MainBot(Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=when_mentioned_or(setup_file["discord"]["command_prefix"]),
                         description="HorribleScrubs, designed to scrape RSS feed info for HS and provide magnet links in discord.\nAll commands are prefaced with {}".format(setup_file["discord"]["command_prefix"]))
						 
        self.http.user_agent = user_agent
        self.ownerid = setup_file["discord"]["owner_id"]

    async def on_ready(self):
        print("\nLogged in as:\n\nBot Name: {0.user.name}\nBot ID: {0.user.id}".format(self))
        print("\n{} Servers".format(len(bot.servers)))
        print("{} users | {} uniques".format(sum(1 for x in bot.get_all_members()),len(set(bot.get_all_members()))))
		
        print("\nBot is live\n------------------------------------------------------------")
        await bot.change_presence(game=discord.Game(name='Scrub a dub dub~'.format(setup_file["discord"]["command_prefix"])))

    async def on_command_error(self, exception, ctx):
        print("Unhandled Exception")
        return

    def run(self):
        print("\nLoading Plugins...\n")
        for plugin in plugins:
            try:
                preString = "{0} is loading...".format(plugin)
                print("{:<35}".format(preString), end="")
                self.load_extension(plugin)
                print("\tSuccess")
            except discord.ClientException:
                print("{0} does not have a setup function!".format(plugin))
            except ImportError as IE:
                print(IE)
        print("\nPlugins Loaded!\n\nNow loading login token and connecting to Discord...\n\n")
        super().run(setup_file["discord"]["token"])
		
    async def on_message(self, message):
        await bot.process_commands(message)
		
if __name__ == "__main__":
    bot = MainBot()
    bot.run()