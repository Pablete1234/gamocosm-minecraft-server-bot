import logging

from discord.ext import commands


def apiErrorHandler(err):
    if not err:
        return "Action succesfully triggered"
    else:
        return err


class Category(commands.Cog):
    """Base class for command category"""

    def __init__(self, client, discord_channel, api):
        self.client = client
        self.discord_channel = discord_channel
        self.api = api


class Diagnostic(Category):
    """Diagnostic information for Bot"""

    def __init__(self, client, discord_channel, api):
        Category.__init__(self, client, discord_channel, api)

    @commands.command()
    async def ping(self, ctx):
        """The latency of the bot"""
        channel = self.client.get_channel(self.discord_channel)
        response = f"Pong! {int(self.client.latency * 1000)}ms"
        await channel.send(response)
        logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

    @commands.command()
    async def status(self, ctx):
        """Current status of the server"""
        channel = self.client.get_channel(self.discord_channel)
        raw_response = self.api._status()
        pserver = ['online' if raw_response['server'] else 'offline'][0]
        minecraft = ['online' if raw_response['minecraft'] else 'offline'][0]
        pending = raw_response['status']
        domain = raw_response['domain']
        ip = raw_response['ip']
        response = f"Physical practice server: {pserver}\n" \
            f"Minecraft PGM server: {minecraft}\n" \
            f"Pending operations: {pending}\n"
        await channel.send(response)
        logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")


class DOServer(Category):
    """Control the practice server"""

    def __init__(self, client, discord_channel, api):
        Category.__init__(self, client, discord_channel, api)

    @commands.command()
    async def start(self, ctx):
        """Starts the practice server"""
        channel = self.client.get_channel(self.discord_channel)
        response = apiErrorHandler(self.api.start())
        await channel.send(response)
        msg = "This will take a few minutes. Use .status to check when the server is online!"
        await channel.send(msg)
        logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

    @commands.command()
    async def stop(self, ctx):
        """Stops the practice server"""
        channel = self.client.get_channel(self.discord_channel)
        response = apiErrorHandler(self.api.stop())
        await channel.send(response)
        logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

    @commands.command()
    async def reboot(self, ctx):
        """Reboots the practice server"""
        channel = self.client.get_channel(self.discord_channel)
        response = apiErrorHandler(self.api.reboot())
        await channel.send(response)
        logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")


class Minecraft(Category):
    """Control the Minecraft PGM server"""

    def __init__(self, client, discord_channel, api):
        Category.__init__(self, client, discord_channel, api)

    @commands.command()
    async def pause(self, ctx):
        """Stops the PGM Server"""
        channel = self.client.get_channel(self.discord_channel)
        response = apiErrorHandler(self.api.pause())
        await channel.send(response)
        logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

    @commands.command()
    async def resume(self, ctx):
        """Starts the PGM server"""
        channel = self.client.get_channel(self.discord_channel)
        response = apiErrorHandler(self.api.resume())
        await channel.send(response)
        logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")
