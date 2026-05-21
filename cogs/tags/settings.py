from typing import TYPE_CHECKING, Optional

import discord
from discord import app_commands
from discord.ext import commands

from cogs.tags.tags import tag_autocomplete_base
from lib.embeds.general import cancelled
from lib.helpers.validation import is_valid_uuid
from lib.sql.sql import GuildSettings, Tag, get_session
from lib.views.confirm import ConfirmView
from lib.views.tags_modals import TagModal

if TYPE_CHECKING:
    from main import TitaniumBot


class TagSettingsCog(commands.Cog):
    def __init__(self, bot: TitaniumBot) -> None:
        self.bot = bot

    def __get_if_server_tag_allowed(
        self, interaction: discord.Interaction["TitaniumBot"], config: Optional[GuildSettings]
    ) -> bool:
        return bool(
            interaction.guild
            and isinstance(interaction.user, discord.Member)
            and interaction.guild.id in [role.id for role in interaction.user.roles]
            and interaction.user.guild_permissions.manage_guild
            and config
            and config.tags_enabled
        )

    context = discord.app_commands.AppCommandContext(
        guild=True, dm_channel=True, private_channel=True
    )
    installs = discord.app_commands.AppInstallationType(guild=True, user=True)
    settings_group = app_commands.Group(
        name="tag-settings",
        description="Manage tag settings.",
        allowed_contexts=context,
        allowed_installs=installs,
    )

    # Create tag command
    @settings_group.command(
        name="add",
        description="Open the wizard to create a new user or server tag.",
    )
    @app_commands.checks.cooldown(1, 3)
    async def add_tag(self, interaction: discord.Interaction["TitaniumBot"]):
        config = (
            await self.bot.fetch_guild_config(interaction.guild_id)
            if interaction.guild_id
            else None
        )

        server_tag_allowed = self.__get_if_server_tag_allowed(interaction, config)
        user_tag_allowed = interaction.user.id not in self.bot.opt_out

        if not server_tag_allowed and not user_tag_allowed:
            embed = discord.Embed(
                title=f"{self.bot.error_emoji} No Possible Options",
                description="You are not able to create server tags in this server, and you have opted out of optional data collection for user tags. There are no further options available.",
                colour=discord.Colour.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        modal = TagModal(server_tag_allowed=server_tag_allowed, user_tag_allowed=user_tag_allowed)
        await interaction.response.send_modal(modal)

    async def tag_autocomplete(
        self, interaction: discord.Interaction["TitaniumBot"], current: str
    ) -> list[app_commands.Choice[str]]:
        config = (
            await self.bot.fetch_guild_config(interaction.guild_id)
            if interaction.guild_id
            else None
        )
        return await tag_autocomplete_base(
            bot=self.bot,
            interaction=interaction,
            current=current,
            verify=self.__get_if_server_tag_allowed(interaction, config),
        )

    # Edit tag command
    @settings_group.command(
        name="edit", description="Open the wizard to edit an existing server or user tag."
    )
    @app_commands.describe(tag="The tag to edit.")
    @app_commands.autocomplete(tag=tag_autocomplete)
    @app_commands.checks.cooldown(1, 3)
    async def edit_tag(self, interaction: discord.Interaction["TitaniumBot"], tag: str):
        async with get_session() as session:
            to_edit = await session.get(Tag, tag)

        if not is_valid_uuid(tag):
            embed = discord.Embed(
                title=f"{self.bot.error_emoji} Invalid Tag ID",
                description="The provided tag ID is invalid. Please select a tag from the autocomplete when typing the tag name.",
                colour=discord.Colour.red(),
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        if (
            not to_edit
            or (to_edit.is_user and to_edit.owner_id != interaction.user.id)
            or (
                not to_edit.is_user
                and (not interaction.guild or to_edit.guild_id != interaction.guild.id)
            )
        ):
            embed = discord.Embed(
                title=f"{self.bot.error_emoji} Not Found",
                description="Couldn't find the tag. Please select a tag from the autocomplete when typing the tag name.",
                colour=discord.Colour.red(),
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        config = (
            await self.bot.fetch_guild_config(interaction.guild_id)
            if interaction.guild_id
            else None
        )

        if not to_edit.is_user and not self.__get_if_server_tag_allowed(interaction, config):
            embed = discord.Embed(
                title=f"{self.bot.error_emoji} No Permissions",
                description="You are not allowed to create or modify server tags. Please ensure you have the **Manage Guild** permission.",
                colour=discord.Colour.red(),
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        modal = TagModal(
            server_tag_allowed=self.__get_if_server_tag_allowed(interaction, config),
            user_tag_allowed=interaction.user.id not in self.bot.opt_out,
            existing_tag=to_edit,
        )
        await interaction.response.send_modal(modal)

    # Delete tag command
    @settings_group.command(name="delete", description="Delete an existing server or user tag.")
    @app_commands.describe(tag="The tag to delete.")
    @app_commands.autocomplete(tag=tag_autocomplete)
    @app_commands.checks.cooldown(1, 3)
    async def delete_tag(self, interaction: discord.Interaction["TitaniumBot"], tag: str):
        await interaction.response.defer(ephemeral=True)

        if not is_valid_uuid(tag):
            embed = discord.Embed(
                title=f"{self.bot.error_emoji} Invalid Tag ID",
                description="The provided tag ID is invalid. Please select a tag from the autocomplete when typing the tag name.",
                colour=discord.Colour.red(),
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        async with get_session() as session:
            to_delete = await session.get(Tag, tag)

        if (
            not to_delete
            or (to_delete.is_user and to_delete.owner_id != interaction.user.id)
            or (
                not to_delete.is_user
                and (not interaction.guild or to_delete.guild_id != interaction.guild.id)
            )
        ):
            embed = discord.Embed(
                title=f"{self.bot.error_emoji} Not Found",
                description="Couldn't find the tag. Please select a tag from the autocomplete when typing the tag name.",
                colour=discord.Colour.red(),
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        config = (
            await self.bot.fetch_guild_config(interaction.guild_id)
            if interaction.guild_id
            else None
        )

        if not to_delete.is_user and not self.__get_if_server_tag_allowed(interaction, config):
            embed = discord.Embed(
                title=f"{self.bot.error_emoji} No Permissions",
                description="You are not allowed to create or modify server tags. Please ensure you have the **Manage Guild** permission.",
                colour=discord.Colour.red(),
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title=f"{self.bot.warn_emoji} Are you sure?",
            description=f"This will delete the `{to_delete.name}` tag and cannot be undone.",
            colour=discord.Colour.orange(),
        )

        view = ConfirmView(self.bot, ephemeral=True)
        view.interaction = interaction

        await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        await view.wait()

        if not view.interaction:
            raise Exception("Impossible: interaction is missing")

        if not view.value:
            return await view.interaction.edit_original_response(
                embed=cancelled(self.bot), view=None
            )

        async with get_session() as session:
            await session.delete(to_delete)

        # reload cache if this is a server tag
        if interaction.guild_id and not to_delete.is_user:
            await self.bot.refresh_guild_config_cache(interaction.guild_id)

        embed = discord.Embed(
            title=f"{self.bot.success_emoji} Done",
            description=f"The `{to_delete.name}` tag has been deleted.",
            colour=discord.Colour.green(),
        )
        await view.interaction.edit_original_response(embed=embed, view=None)


async def setup(bot: TitaniumBot) -> None:
    await bot.add_cog(TagSettingsCog(bot))
