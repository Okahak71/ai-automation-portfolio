import os
import requests
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

@bot.tree.command(name="price", description="Fetch current crypto price and 24h change")
@app_commands.describe(coin="Coin ID (e.g. bitcoin, ethereum, solana)")
async def price(interaction: discord.Interaction, coin: str):
    await interaction.response.defer()
    coin_id = coin.lower().strip()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if coin_id in data:
                usd_price = data[coin_id]["usd"]
                change_24h = data[coin_id].get("usd_24h_change", 0)

                color = discord.Color.green() if change_24h >= 0 else discord.Color.red()
                embed = discord.Embed(
                    title=f"📈 {coin_id.capitalize()} Market Data",
                    color=color
                )
                embed.add_field(name="Price (USD)", value=f"${usd_price:,.2f}", inline=True)
                embed.add_field(name="24h Change", value=f"{change_24h:+.2f}%", inline=True)
                embed.set_footer(text="Data provided by CoinGecko")

                await interaction.followup.send(embed=embed)
                return

        await interaction.followup.send(f"❌ Could not find data for **'{coin}'**. Ensure you are using the correct CoinGecko ID.")
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error fetching data: {str(e)}")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
