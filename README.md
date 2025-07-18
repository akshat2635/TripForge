# 🌍 TripForge - Streamlit Chat App

A conversational AI travel planner powered by LangGraph and Google Gemini, deployed as a Streamlit web application.

## 🚀 Features

- **💬 Chat Interface**: Natural conversation with your AI travel assistant
- **🧠 Intelligent Planning**: Powered by Google Gemini 2.0 Flash model
- **✈️ Real-time Data**: Live flight, hotel, and activity searches via SerpAPI
- **📱 Session-based**: Each device/browser maintains separate chat sessions
- **📥 Export Options**: Download preferences and itineraries as text files
- **🎯 Two-phase Planning**:
  1. **Preferences Collection**: Gather travel requirements through conversation
  2. **Itinerary Creation**: Generate detailed travel plans with bookings

## 📁 Project Structure

```
streamlit_app/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── core/
│   ├── chat_agent.py          # Main chat agent logic
│   └── state_manager.py       # Streamlit session state management
├── graphs/
│   ├── main_graph.py          # Main LangGraph workflow
│   ├── preferences_graph.py   # Preferences collection graph
│   └── itinerary_graph.py     # Itinerary creation graph
├── utils/
│   ├── schema.py              # Data schemas
│   ├── prompts.py             # LLM prompts
│   └── tools.py               # API integration tools
└── data/                      # Generated files storage
```

## 🛠️ Setup & Installation

### 1. Prerequisites

- Python 3.8+
- Google Gemini API key
- SerpAPI key (for flight/hotel searches)

### 2. Installation

```bash
# Clone or navigate to the streamlit_app directory
cd streamlit_app

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 3. Environment Variables

Create a `.env` file with:

```env
GOOGLE_API_KEY=your_google_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 Usage

1. **Start Planning**: Open the app and begin chatting with TripForge
2. **Share Preferences**: Tell the AI about your travel plans:
   - Departure and destination cities
   - Travel dates
   - Budget and preferences
   - Group size and travel style
3. **Review & Confirm**: The AI will summarize your preferences
4. **Get Itinerary**: Receive a personalized travel plan with:
   - Flight recommendations
   - Hotel suggestions
   - Activity recommendations
   - Day-by-day schedules
5. **Download**: Save your preferences and itinerary files

## 💡 Example Conversation

```
👤 You: I want to plan a boys trip to Goa
🤖 TripForge: Sounds exciting! For your Goa boys trip, I need a few details.
              Where will you be departing from?

👤 You: Delhi, leaving next weekend
🤖 TripForge: Perfect! So departing from Delhi next weekend. How many people
              in your group, and what's your approximate budget per person?
```

## 🔧 Key Features

### Session Management

- Each browser session is independent
- Chat history persists during the session
- Progress tracking with visual indicators

### Real-time API Integration

- **Flights**: Live search via SerpAPI Google Flights
- **Hotels**: Real hotel availability and pricing
- **Activities**: Location-based recommendations

### Export & Download

- Save preferences as structured text files
- Download complete itineraries
- Easy sharing and printing

## 🚀 Deployment Options

### Local Development

```bash
streamlit run app.py
```

### Streamlit Cloud

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add environment variables in Streamlit Cloud settings
4. Deploy!

### Docker (Optional)

```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🔄 Migration from Console App

This Streamlit version maintains the same core functionality as the original console application:

### What's the Same:

- ✅ LangGraph workflow logic
- ✅ Google Gemini integration
- ✅ SerpAPI tool integration
- ✅ File storage and preferences
- ✅ Two-phase planning process

### What's Different:

- 🔄 Web chat interface instead of console I/O
- 🔄 Session-based state management
- 🔄 Visual progress indicators
- 🔄 Download buttons for files
- 🔄 Enhanced UI with styling

## 📝 Troubleshooting

### Common Issues:

1. **API Key Errors**

   - Ensure `.env` file exists with valid keys
   - Check API key format and permissions

2. **Import Errors**

   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path configuration

3. **Session State Issues**
   - Refresh the browser page
   - Use "Start New Trip" button to reset

### Debug Mode:

Add to your `.env`:

```env
STREAMLIT_DEBUG=true
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

[Add your license information here]

---

**Happy Travels with TripForge! ✈️🌍**
