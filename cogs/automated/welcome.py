from typing import TYPE_CHECKING

import discord
from discord import Color
from discord.ext import commands
from discord.ui import View

if TYPE_CHECKING:
    from main import TitaniumBot


class WelcomeCog(commands.Cog):
    def __init__(self, bot: "TitaniumBot") -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        embed = discord.Embed(
            title="Welcome to Titanium!",
            description="**Thank you for choosing Titanium!** To interact with Titanium, use `t!` (this can be changed!), mention Titanium, or use slash commands.",
            color=Color.green(),
        )

        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.add_field(
            name="Getting Started",
            value="1. Use the `/settings` slash command to enable modules and change the prefix.\n"
            f"2. Log into the [Titanium Dashboard](https://dash.titanium.fyi/guild/{guild.id}) to set up Titanium's modules - for example, moderation, automod and fireboard.\n"
            "3. Use `t!help` or `/help` for help with a command, or run `t!help commands` or `/help commands` for a full command list.",
            inline=False,
        )
        embed.add_field(
            name="Feedback",
            value="Found a bug or have a feature request? Join the support server, use the `/feedback` command, or create an issue in the GitHub repo. Enjoying Titanium? Leave a star on GitHub!",
            inline=False,
        )

        view = View()
        view.add_item(
            discord.ui.Button(
                label="Website", style=discord.ButtonStyle.url, url="https://titanium.fyi", row=0
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Dashboard",
                style=discord.ButtonStyle.url,
                url="https://dash.titanium.fyi",
                row=0,
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Source Code",
                style=discord.ButtonStyle.url,
                url="https://github.com/restartb/titanium",
                row=0,
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Support Server",
                style=discord.ButtonStyle.url,
                url="https://titanium.fyi/server",
                row=0,
            )
        )

        view.add_item(
            discord.ui.Button(
                label="Privacy Policy",
                style=discord.ButtonStyle.url,
                url="https://titanium.fyi/privacy",
                row=1,
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Terms of Use",
                style=discord.ButtonStyle.url,
                url="https://titanium.fyi/terms",
                row=1,
            )
        )

        try:
            if guild.system_channel is not None:
                if guild.system_channel.permissions_for(guild.me).send_messages:
                    await guild.system_channel.send(embed=embed, view=view)
                    return

            for channel in guild.channels:
                if (
                    not isinstance(channel, discord.abc.Messageable)
                    or not channel.permissions_for(guild.me).send_messages
                ):
                    continue

                await channel.send(embed=embed, view=view)
                return
        except Exception:
            pass


async def setup(bot: "TitaniumBot") -> None:
    await bot.add_cog(WelcomeCog(bot))
