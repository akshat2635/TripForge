# 🌍 TripForge - AI Travel Planning Assistant

<!-- Repository Status Badges -->
<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![LangChain](https://img.shields.io/badge/langchain-v0.1+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

</div>

> **Your intelligent travel companion that transforms conversation into personalized trip itineraries**

TripForge is a sophisticated AI-powered travel planning application built with Streamlit and LangGraph. It leverages Google Gemini's advanced language model to understand your travel preferences through natural conversation and creates detailed, actionable travel itineraries with real-time flight and hotel data.

## ✨ Key Features

- **🤖 Intelligent Conversations**: Natural language understanding with context-aware responses
- **🚀 Advanced AI**: Powered by Google Gemini 2.0 Flash with LangGraph workflow engine
- **🌐 Real-Time Data**: Live flight/hotel search via SerpAPI with multiple options
- **💼 Professional UI**: Session management, export capabilities, mobile responsive design
- **🔧 Developer-Friendly**: Modular architecture, extensible design, secure configuration

## 📁 Project Structure

```
TripForge app/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies  
├── .env.example             # Environment template
├── static/styles.css        # UI styling
├── core/chat_agent.py       # Conversation orchestrator
├── graphs/                  # LangGraph workflows
│   ├── preferences_graph.py # Phase 1: Preference collection
│   └── itinerary_graph.py  # Phase 2: Itinerary generation
└── utils/                   # Core utilities
    ├── schema.py           # State definitions
    ├── prompts.py          # LLM prompts
    └── tools.py            # SerpAPI integration
```

**Two-Phase System:**
1. **Preference Collection**: Natural conversation to gather travel requirements
2. **Itinerary Generation**: Detailed travel plans with real-time flight/hotel data

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (Recommended: 3.10+)
- [Google Gemini API Key](https://makersuite.google.com/app/apikey)
- [SerpAPI Key](https://serpapi.com/) (free tier: 100 searches/month)

### Installation

1. **Clone & Setup**
   ```bash
   git clone <repository-url>
   cd "TripForge app"
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   copy .env.example .env
   # Edit .env with your API keys
   ```

3. **Add API Keys to `.env`**
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   SERPAPI_API_KEY=your_serpapi_key_here
   ```

4. **Run Application**
   ```bash
   streamlit run app.py
   # Access at http://localhost:8501
   ```

## 🎯 How It Works

### Conversation Example
```
👤 "Plan a boys trip to Goa"
🤖 "Sounds exciting! I'm seeing beach parties, decent hotels near the action. 
    Where will you be departing from?"

👤 "Delhi, leaving next weekend with 4 friends"  
🤖 "Perfect! For your 5-person Goa boys trip from Delhi next weekend.
    What's your approximate budget per person?"
```

### What TripForge Captures
- 📍 Departure & destination cities
- 📅 Travel dates (smart parsing)
- 👥 Group size and composition  
- 💰 Budget per person (local currency)
- 🎯 Interests and preferences
- ✈️ Travel class & accommodation style
- 🛂 Visa status (international trips)

### Generated Itinerary Features
- **Flight Options**: 2-3 alternatives with pricing and timing
- **Hotel Recommendations**: Multiple choices with ratings and amenities  
- **Day-by-Day Plans**: Activities, meals, transportation, costs
- **Budget Breakdown**: Transparent per-person calculations
- **Insider Tips**: Local insights and practical advice

## 💡 Sample Itinerary Output

```
🌍 PARIS ROMANTIC WEEKEND ITINERARY

✈️ FLIGHT OPTIONS
Option 1: Air France AF006 | JFK → CDG | Fri 8:15 PM - Sat 9:45 AM 
7h 30m | Business Class | $1,600 per person

🏨 HOTEL OPTIONS  
Hotel des Grands Boulevards (4-star) | 4.2/5 (1,247 reviews)
$180/night x 2 nights = $180 per person

Day 1: Romantic Paris Arrival & Seine Discovery
- Airport transfer & hotel check-in (2h)
- Seine River lunch cruise ($85 per person)  
- Louvre & Tuileries romantic stroll ($45 per person)
Total Day Cost: $248 per person

GRAND TOTAL: $1,542 per person
```

## 🎨 Interface Features

- **Chat Interface**: Natural conversation with message bubbles
- **Sidebar Tools**: New chat, download itinerary/preferences/chat history
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Professional Styling**: Dark theme with blue accents

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Add secrets in dashboard:
   ```toml
   GOOGLE_API_KEY = "your_key"
   SERPAPI_API_KEY = "your_key" 
   ```
4. Deploy!

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🛠️ Development

### Adding New Tools
```python
# In utils/tools.py
@tool
def search_activities(location: str, interests: list) -> str:
    """Search for activities and attractions."""
    return activity_results

# Register tool
tools = [search_flights, search_hotels, search_activities]
```

### Customizing Prompts
Edit `utils/prompts.py` to modify conversation flow and AI behavior.

### Testing
```bash
# Test locally
streamlit run app.py

# Test API integrations  
python utils/tools.py
```

## 🔍 Troubleshooting

### Common Issues

**API Key Errors**
```
Error: "google.api_core.exceptions.Unauthenticated"
```
- Verify `.env` file contains valid `GOOGLE_API_KEY`
- Check API key has Gemini access enabled
- Remove extra spaces/quotes around key

**SerpAPI Limits**
```
Error: "Monthly search limit reached"
```
- Check [SerpAPI dashboard](https://serpapi.com/dashboard) for usage
- Upgrade plan or implement caching

**Module Errors**
```
ModuleNotFoundError: No module named 'langchain'
```
- Reinstall: `pip install -r requirements.txt --force-reinstall`
- Use virtual environment: `python -m venv venv`

**Session Issues**
- Clear browser cache
- Use "🔄 New Chat" button
- Restart server: `Ctrl+C` then `streamlit run app.py`

### Debug Mode
```env
# In .env file
STREAMLIT_DEBUG=true
LANGCHAIN_TRACING_V2=true
```

## 🤝 Contributing

We welcome contributions! Here's how to help:

### Getting Started
```bash
git clone https://github.com/yourusername/tripforge.git
cd tripforge
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
git checkout -b feature/your-feature-name
```

### Areas for Contribution
- [ ] Multi-language support
- [ ] Booking platform integration
- [ ] Calendar integration
- [ ] Group trip collaboration
- [ ] Weather integration
- [ ] Mobile app improvements

### Code Style
- Follow PEP 8
- Add type hints and docstrings
- Test new features thoroughly
- Update documentation as needed

### Submitting Changes
1. Test locally: `streamlit run app.py`
2. Create pull request with clear description
3. Include screenshots for UI changes
4. Reference related issues

## 📄 License & Legal

**License**: MIT License - see [LICENSE](LICENSE) file

**Third-Party Services**:
- Google Gemini: Subject to [Google's Terms](https://ai.google.dev/terms)
- SerpAPI: Subject to [SerpAPI Terms](https://serpapi.com/terms)
- Streamlit: Apache 2.0 License

**Privacy**: 
- Data processed locally in browser session
- No permanent server storage
- API calls subject to respective privacy policies

**Disclaimer**: Verify all travel information independently. Check visa requirements, travel restrictions, and confirm prices before booking.

---

## 🎉 Ready to Start Planning?

TripForge transforms travel planning complexity into enjoyable conversation. Whether planning a romantic getaway, adventure with friends, or family vacation, TripForge creates personalized itineraries matching your style and budget.

**🚀 Get Started:**
1. Follow the [Quick Start](#-quick-start) guide
2. Get your API keys  
3. Launch TripForge and start planning!

**💬 Need Help?**
- Check [Troubleshooting](#-troubleshooting)
- Review [Development Guide](#️-development)
- Contribute via [GitHub Issues](https://github.com/yourusername/tripforge/issues)

---

**Happy Travels with TripForge! ✈️🌍**

*Where conversation meets perfect travel planning.*
