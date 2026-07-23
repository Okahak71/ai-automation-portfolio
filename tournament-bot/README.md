# 🏆 Case Study: Tournament Drop-Off Prevention Bot

> **Client Goal:** Eliminate player forfeits and manual organizer check-ins for high-stakes tournaments.  
> **Tech Stack:** Python (`discord.py`), AsyncIO, `python-dotenv`  
> **Impact:** 100% attendance tracking, saved 8+ hours of staff management per event.

---

## 🎯 The Problem
Tournament organizers spent hours manually messaging 100+ players across Discord DMs before the event. Missing check-ins caused stream delays, bracket rescheduling, and overall event chaos.

## 🛠️ The Solution
A custom Discord bot designed to automate player attendance tracking from broadcast to live reporting:

* **Automated DM Broadcast:** Dispatches direct match announcements to all players with a target role.
* **Interactive UI:** One-click **[Confirm Attendance]** and **[Need Sub]** buttons directly inside player DMs.
* **Live Channel Dashboard:** Real-time embed updating player statuses (`🟢 Confirmed`, `🔴 Forfeited`, `⏳ Pending`).
* **On-Demand Admin Reports:** Instant `/admin-control` slash command for staff to get a live status breakdown anytime.

---

## 💬 Client Testimonial

> *"This bot completely freed up our staff during the semi-finals. We didn't have to chase down a single player manually, and the live dashboard made tracking attendance completely painless!"*  
> — **Tournament Director / Server Owner**

---

## 🎮 Slash Commands

| Command | Permission | Description |
| :--- | :--- | :--- |
| `/notify-stage` | Administrator | Triggers automated DM pings & launches the live channel dashboard. |
| `/admin-control` | Administrator | Displays an instant status report for a target role on demand. |

---

## 🚀 Quick Start

1. **Install dependencies:**  
   `pip install -r requirements.txt`

2. **Configure `.env`:**  
   `DISCORD_BOT_TOKEN=your_bot_token_here`

3. **Run the bot:**  
   `python bot.py`