from nextcord.ext import commands


class Another(commands.Cog):
    def __init__(self, nextcord):
        self.nextcord = nextcord

    @commands.command("another")
    async def example(self, ctx: commands.Context, *args):
        await ctx.send("Hello!")


def setup(bot):
    bot.add_cog(Another(bot))
