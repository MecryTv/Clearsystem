from datetime import datetime

import discord
import asyncio
from discord.ext import commands
from discord.commands import slash_command
from discord import File


class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Lösche Nachrichten")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, zahl: int, grund: str):
        await interaction.response.defer()

        if zahl <= 0:
            await interaction.channel.send("Die Anzahl der zu löschenden Nachrichten muss größer als 0 sein.")
            return

        messages = await interaction.channel.history(limit=zahl + 1).flatten()
        await interaction.channel.delete_messages(messages)

        embed = discord.Embed(
            title="Nachrichten gelöscht",
            description=f"Es wurden {zahl} Nachrichten von {interaction.user.mention} gelöscht.",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.add_field(name="Grund", value=grund, inline=False)

        thumbnail_path = "img/Mülleimer.png"
        thumbnail_file = File(thumbnail_path, filename="thumbnail.png")
        embed.set_thumbnail(url="attachment://thumbnail.png")
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=self.bot.user.avatar.url)

        msg = await interaction.channel.send(embed=embed, file=thumbnail_file)
        await asyncio.sleep(10)
        await msg.delete()


    @clear.error
    async def clear_error(self, interaction: discord.Interaction, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message(
                "Du hast keine Rechte, um den Befehl zu benutzen", ephemeral=True
            )


def setup(bot):
    bot.add_cog(ClearCommand(bot))
