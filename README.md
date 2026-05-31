# 🌴 Travel WhatsApp Agent

**Tired of being the group trip organizer who answers the same questions 47 times?**

"What time is checkout?" "What's the Airbnb address?" "Do we need cash or card?" "What are we doing Thursday?"

You know the drill. You spend hours researching flights, hotels, and activities — and then spend the entire trip forwarding the same info over and over in WhatsApp.

This agent fixes that. You dump all your trip details into one file, deploy it, and share the WhatsApp number with your travel group. Now everyone can ask the bot instead of you. It knows the itinerary, the accommodation, the activities, who's coming, emergency contacts — everything. And it answers instantly, 24/7, in whatever language your friends write in.

**You go from being the group's travel helpdesk to actually enjoying the trip.**

## How it works

A FastAPI server receives WhatsApp messages via Twilio's webhook, sends them to Claude (Anthropic) with your trip data as context, and replies back through WhatsApp. The agent knows who's messaging based on their phone number and can give personalized answers.

```
WhatsApp → Twilio → FastAPI → Claude API → Twilio → WhatsApp
```

## Quick start

```bash
# Clone and setup
git clone https://github.com/MirandaCavalie/travel-whatsapp-agent.git
cd travel-whatsapp-agent
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1

# Install and configure
pip install -r requirements.txt
cp .env.example .env       # Fill in your API keys

# Run
uvicorn app.main:app --reload --port 8000
```

Health check: `GET /health` → `{"status": "ok"}`

## Prerequisites

- **Twilio account** with WhatsApp Sandbox enabled ([console.twilio.com](https://console.twilio.com))
- **Anthropic API key** ([console.anthropic.com](https://console.anthropic.com))
- **Python 3.11+**

## Add your trip details

Edit `app/trip_data.py` with your actual trip info:

- **`general`** — destination, dates, currency, timezone, travel tips
- **`travelers`** — one entry per person (name, phone in `+country...` format so the bot recognizes who's writing)
- **`accommodation`** — hotel/Airbnb address, check-in/out, confirmation number
- **`activities`** — day-by-day itinerary with times and locations
- **`emergency`** — emergency contacts, travel insurance info

Changes take effect on the next message — no restart needed if running with `--reload`.

## Deploy to production

This project is deploy-ready for [Render](https://render.com):

1. Push your repo to GitHub
2. Create a **Web Service** on Render, connect your repo
3. Render auto-detects the `Dockerfile`
4. Set your environment variables:

| Variable | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `TWILIO_ACCOUNT_SID` | From Twilio Console |
| `TWILIO_AUTH_TOKEN` | From Twilio Console |
| `TWILIO_WHATSAPP_NUMBER` | `whatsapp:+14155238886` (sandbox) |
| `ENVIRONMENT` | `production` |
| `PUBLIC_BASE_URL` | Your Render URL (e.g. `https://your-app.onrender.com`) |

5. In Twilio Console, set the webhook URL to `https://your-app.onrender.com/webhook/whatsapp` (POST)

## Local development with ngrok

For testing locally, expose your server with [ngrok](https://ngrok.com):

```bash
# Terminal 1: run the server
uvicorn app.main:app --reload --port 8000

# Terminal 2: expose it
ngrok http 8000
```

Copy the ngrok URL into Twilio's sandbox webhook settings.

## Project structure

```
travel-whatsapp-agent/
├── Dockerfile
├── render.yaml
├── requirements.txt
└── app/
    ├── main.py          # FastAPI app + webhook endpoint
    ├── config.py        # Environment variable loading
    ├── whatsapp.py      # Twilio message sending + chunking
    ├── agent.py         # Claude system prompt + conversation history
    └── trip_data.py     # Your trip details (edit this!)
```

## Limitations

This is an MVP built for a specific trip:

- Conversation history lives in memory (resets on deploy/restart)
- Single-instance only (no shared state across workers)
- No database — trip data is a Python dict

For something more robust, you'd want to move the history to Redis or Postgres and the trip data to a proper database.

## Built with

- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [Claude API](https://docs.anthropic.com/) — LLM for natural language responses
- [Twilio](https://www.twilio.com/docs/whatsapp) — WhatsApp messaging
- [Render](https://render.com/) — hosting

