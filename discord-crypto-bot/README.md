# 📈 Discord Crypto Price Tracker Bot

A light, asynchronous Discord bot built with `discord.py` that utilizes slash commands (`/price`) to query real-time cryptocurrency market data from the CoinGecko public API.

---

## 🚀 Features
- **Slash Commands:** Modern `/price [coin]` interaction tree.
- **Dynamic Formatting:** Embed card automatically changes color based on 24-hour gain/loss (Green for positive, Red for negative).
- **Secure Architecture:** Reads API tokens via environment variables (`.env`) to protect private credentials.
- **Error Handling:** Handles unknown coin queries and API timeouts gracefully.

---

## 🛠️ Prerequisites
- **Python 3.8+** installed on your system.
- A **Discord Application Token** (from the [Discord Developer Portal](https://discord.com/developers/applications)).

---

## 📁 Repository Layout
```text
discord-crypto-bot/
├── main.py              # Main bot script with slash command logic
├── requirements.txt      # Python dependencies
├── .env.example          # Template for environment variables
└── README.md             # Documentation
```

---

## ⚙️ Setup & Installation

1. **Navigate to the project directory:**
   ```bash
   cd discord-crypto-bot
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   - Copy `.env.example` to a new file named `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` in your code editor and insert your actual Discord Bot Token:
     ```env
     DISCORD_BOT_TOKEN=your_actual_discord_bot_token_here
     ```

4. **Launch the Bot:**
   ```bash
   python main.py
   ```

---

## 🎮 How to Use
1. Invite the bot to your server using the OAuth2 URL from the Discord Developer Portal (ensure both `bot` and `applications.commands` scopes are checked).
2. In any server text channel, type `/price` followed by the CoinGecko coin ID:
   - `/price bitcoin`
   - `/price ethereum`
   - `/price solana`

---

## 📝 License
This project is open-source and available under the [MIT License](../LICENSE).
