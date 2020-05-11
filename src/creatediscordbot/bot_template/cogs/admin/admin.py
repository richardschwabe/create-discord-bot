# This is your Cog
import logging
import discord
from discord.ext import commands

from settings import COGS_FOLDER

from .controller import AdminController
from .converter import ActivityTypeConverter

logger = logging.getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.controller = AdminController()

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        """
        Load Cog

        Allows you to quickly LOAD a cog from within discord.
        """
        cog = f'{COGS_FOLDER.name}.{cog}.{cog}'
        logger.debug(f"Loading Cog: {cog}")
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send("Could not unload cog")
            return
        await ctx.send("Cog unloaded")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        """
        Unload Cog

        Allows you to quickly UNLOAD a cog from within discord.
        """
        cog = f'{COGS_FOLDER.name}.{cog}.{cog}'
        logger.debug(f"Unloading Cog: {cog}")
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not load cog")
            return
        await ctx.send("Cog loaded")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        """
        Reload Cog

        Allows you to quickly RELOAD a cog from within discord.
        """
        cog = f'{COGS_FOLDER.name}.{cog}.{cog}'
        logger.debug(f"Reloading Cog: {cog}")
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send("Could not reload cog")
            return
        await ctx.send("Cog reloaded")

    @commands.command()
    @commands.is_owner()
    async def presence(self, ctx, presence_type: ActivityTypeConverter, *message: str, ):
        """
        Sets the presence status of the bot

        presence_type can be any of:
        - listening
        - watching
        - streaming
        - playing

        """
        if presence_type.cleaned_value != discord.ActivityType.unknown:
            activity = discord.Activity(
                name=" ".join(message), type=presence_type.cleaned_value)
            await self.bot.change_presence(activity=activity)
            await ctx.send("Presence update. Please wait a few seconds to see the change.")
        else:
            await ctx.send("This is an unknown type. Please use !help presence to learn more about the types.")


def setup(bot):
    bot.add_cog(Admin(bot))
