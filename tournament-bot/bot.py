import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

active_sessions = {}


class CheckInView(discord.ui.View):
    def __init__(self, tracker_message: discord.Message, target_role: discord.Role):
        super().__init__(timeout=None)
        self.tracker_message = tracker_message
        self.target_role = target_role
        
        self.confirmed = set()
        self.forfeited = set()

    async def update_tracker(self):
        """Helper function to update the original live admin tracking embed."""
        if not self.tracker_message:
            return

        embed = self.tracker_message.embeds[0]
        total_players = len(self.target_role.members)
        pending_count = total_players - (len(self.confirmed) + len(self.forfeited))
        
        confirmed_str = "\n".join([f"🟢 {user.mention}" for user in self.confirmed]) or "None"
        forfeited_str = "\n".join([f"🔴 {user.mention}" for user in self.forfeited]) or "None"
        
        embed.set_field_at(0, name=f"🟢 Confirmed ({len(self.confirmed)})", value=confirmed_str, inline=True)
        embed.set_field_at(1, name=f"🔴 Forfeited/Sub Needed ({len(self.forfeited)})", value=forfeited_str, inline=True)
        embed.set_field_at(2, name=f"⏳ Pending ({pending_count})", value=f"{pending_count} remaining", inline=False)
        
        try:
            await self.tracker_message.edit(embed=embed)
        except discord.HTTPException:
            pass

    @discord.ui.button(label="Confirm Attendance", style=discord.ButtonStyle.green, custom_id="confirm_attn")
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        if user in self.forfeited:
            self.forfeited.remove(user)
        self.confirmed.add(user)
        
        await interaction.response.send_message("✅ Your attendance is confirmed!", ephemeral=True)
        await self.update_tracker()

    @discord.ui.button(label="Need Sub / Forfeit", style=discord.ButtonStyle.red, custom_id="forfeit_attn")
    async def forfeit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        if user in self.confirmed:
            self.confirmed.remove(user)
        self.forfeited.add(user)
        
        await interaction.response.send_message("⚠️ Noted. Admins have been alerted.", ephemeral=True)
        await self.update_tracker()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")


@bot.tree.command(name="notify-stage", description="Send automated check-in DMs to tournament players.")
@app_commands.checks.has_permissions(administrator=True)
async def notify_stage(
    interaction: discord.Interaction,
    role: discord.Role,
    match_time: str,
    custom_message: str
):
    await interaction.response.defer()
    tracker_embed = discord.Embed(
        title=f"🏆 Live Tracker: {role.name}",
        description=f"**Match Time:** {match_time}\n**Announcement:** {custom_message}",
        color=discord.Color.gold()
    )
    tracker_embed.add_field(name="🟢 Confirmed (0)", value="None", inline=True)
    tracker_embed.add_field(name="🔴 Forfeited/Sub Needed (0)", value="None", inline=True)
    tracker_embed.add_field(name=f"⏳ Pending ({len(role.members)})", value=f"{len(role.members)} remaining", inline=False)
    
    tracker_msg = await interaction.followup.send(embed=tracker_embed)

    view = CheckInView(tracker_message=tracker_msg, target_role=role)
    active_sessions[role.id] = {
        "view": view,
        "match_time": match_time,
        "custom_message": custom_message
    }
    
    dm_embed = discord.Embed(
        title=f"⚠️ Action Required: Tournament Check-In ({role.name})",
        description=f"You are scheduled to compete!\n\n**Time:** {match_time}\n**Details:** {custom_message}\n\nPlease select your status below:",
        color=discord.Color.blue()
    )

    successful_dms = 0
    failed_dms = 0

    for member in role.members:
        if member.bot:
            continue
        try:
            await member.send(embed=dm_embed, view=view)
            successful_dms += 1
        except (discord.Forbidden, discord.HTTPException):
            failed_dms += 1

        await asyncio.sleep(0.5)

    await interaction.channel.send(
        f"📊 **Broadcast Finished:** DMs sent to {successful_dms} players ({failed_dms} unreachable due to closed DMs)."
    )


@bot.tree.command(name="admin-control", description="Get an on-the-spot status report for an active tournament check-in.")
@app_commands.checks.has_permissions(administrator=True)
async def admin_control(interaction: discord.Interaction, role: discord.Role):
    """Generates an immediate status report for the specified role."""
    
    if role.id not in active_sessions:
        await interaction.response.send_message(
            f"❌ No active tournament check-in found for {role.mention}. Run `/notify-stage` first.",
            ephemeral=True
        )
        return

    session = active_sessions[role.id]
    view = session["view"]
    match_time = session["match_time"]
    
    total_players = len(role.members)
    pending_players = [m for m in role.members if not m.bot and m not in view.confirmed and m not in view.forfeited]
    
    confirmed_str = "\n".join([f"🟢 {user.mention}" for user in view.confirmed]) or "None"
    forfeited_str = "\n".join([f"🔴 {user.mention}" for user in view.forfeited]) or "None"
    pending_str = "\n".join([f"⏳ {user.mention}" for user in pending_players]) or "None"

    if len(pending_str) > 1024:
        pending_str = f"{len(pending_players)} players pending..."

    report_embed = discord.Embed(
        title=f"📊 Instant Status Report: {role.name}",
        description=f"**Scheduled Time:** {match_time}\n**Total Players:** {total_players}",
        color=discord.Color.blue()
    )
    
    report_embed.add_field(name=f"🟢 Confirmed ({len(view.confirmed)})", value=confirmed_str, inline=False)
    report_embed.add_field(name=f"🔴 Forfeited/Sub Needed ({len(view.forfeited)})", value=forfeited_str, inline=False)
    report_embed.add_field(name=f"⏳ Pending Response ({len(pending_players)})", value=pending_str, inline=False)
    report_embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=report_embed)


bot.run(os.getenv("DISCORD_BOT_TOKEN"))