# 📈 Discord Crypto Price Tracker Bot

A light, asynchronous Discord bot built with `discord.py` that utilizes slash commands to query real-time market data from CoinGecko.

## Features
- **Slash Commands:** Integrated `/price [coin]` command.
- **Dynamic Formatting:** Embed card changes color based on 24-hour gain/loss.
- **Secure Architecture:** Reads API tokens via environment variables (`.env`).

## Setup & Installation

1. Clone this directory and install dependencies:
   ```bash
   pip install -r requirements.txt
