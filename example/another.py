from nextcord.ext import commands

# This is an example cog that doesn't have or use any models


class Another(commands.Cog):
    def __init__(self, nextcord):
        self.nextcord = nextcord

    @commands.command("another")
    async def example(self, ctx: commands.Context, *args):
        await ctx.send("Hello!")


def setup(bot):
    bot.add_cog(Another(bot))
