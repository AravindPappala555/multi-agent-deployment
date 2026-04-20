# Rasool Khan Real Estate Services — AI Chatbot

A luxury real estate chatbot powered by Claude AI, built with Flask.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your API key
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

Or set it directly:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Run the app
```bash
python app.py
```

Visit: http://localhost:5000

## Features
- Warm, personalised property advisor conversation
- Collects user info: profession, family size, house type preference
- Location-aware property suggestions with realistic pricing
- Budget matching — ask for higher or lower options
- Quick-start chips for common queries
- Full conversation memory per session
- Responsive 3-column luxury dark UI

## Stack
- **Backend**: Flask + Anthropic Claude API
- **Frontend**: Vanilla HTML/CSS/JS — no frameworks, zero dependencies
- **Fonts**: Cormorant Garamond + DM Sans (Google Fonts)
