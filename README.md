# Travel Agent Assistant

An AI-powered application designed to help travel agents find optimal travel options for their clients. The application integrates with Amadeus API endpoints and Sherpa API to provide intelligent travel recommendations, considering factors like visa requirements, budget, and travel preferences.

## 🚀 Features

### Currently Implemented

* **Intelligent Flight Search:** Finds optimal flight routes considering visa requirements and suggesting alternative routes to save time and money.
* **Multi-modal Travel Suggestions:** Recommends alternative travel options like driving to a nearby airport to find cheaper or more direct flights.
* **Visa Requirements Check:** Integrates with Sherpa API to check visa requirements for travel between countries.
* **Nearest Airport Search:** Finds nearby airports to a given location for alternative routing options.
* **Hotel Search:** Search for hotels in specific cities (via Amadeus API).
* **Activity Search:** Discover activities near a given location.

### Coming Soon

* **Comprehensive Travel Search:** Enhanced search for hotels, cars, and activities with advanced filtering.
* **Visa Recommendations:** AI-powered visa recommendations based on travel history and preferences.
* **E-visa Procurement Facilitation:** Streamlined process for obtaining e-visas through integrated services.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (usually comes with Python)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Amadeus API Account** - See [API Setup](#api-setup) section below
- **Sherpa API Key** (optional, for visa requirements) - See [API Setup](#api-setup) section below

## 🛠️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Travel-Agent-Aid.git
cd Travel-Agent-Aid
```

### Step 2: Set Up Python Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Create a `.env` file in the `backend` directory:
   ```bash
   cd backend
   touch .env  # On Windows: type nul > .env
   ```

2. Open `.env` and add your API credentials (see [API Setup](#api-setup) for details):
   ```
   AMADEUS_CLIENT_ID=your_amadeus_client_id
   AMADEUS_CLIENT_SECRET=your_amadeus_client_secret
   SHERPA_API_KEY=your_sherpa_api_key
   ```

   **Note:** The `.env` file is excluded from version control for security. Never commit your API keys!

### Step 5: Run the Application

**Start the Flask backend:**
```bash
cd backend
python app.py
```

The backend will start on `http://localhost:5000` by default.

**Open the frontend:**
Simply open `frontend/index.html` in your web browser, or serve it using a local web server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 8000
```

Then navigate to `http://localhost:8000` in your browser.

## 🔑 API Setup

### Amadeus API Setup

1. **Create an Account:**
   - Visit [Amadeus for Developers](https://developers.amadeus.com/)
   - Sign up for a free account

2. **Create an Application:**
   - Go to "My Self-Service" → "Create New App"
   - Fill in the application details
   - Choose "Test" environment for development

3. **Get Your Credentials:**
   - After creating the app, you'll receive:
     - `Client ID`
     - `Client Secret`
   - Add these to your `.env` file as `AMADEUS_CLIENT_ID` and `AMADEUS_CLIENT_SECRET`

4. **API Endpoints Used:**
   - Flight Offers Search
   - Airport & City Search
   - Hotel Search
   - Airport Nearest Relevant
   - Activities Search

**Note:** The Test environment has rate limits. For production use, you'll need to upgrade to a paid plan.

### Sherpa API Setup (Optional)

1. **Create an Account:**
   - Visit [Sherpa API](https://www.joinsherpa.com/api)
   - Sign up for an account

2. **Get Your API Key:**
   - Navigate to your dashboard
   - Copy your API key
   - Add it to your `.env` file as `SHERPA_API_KEY`

**Note:** Visa requirements feature requires a valid Sherpa API key. The application will still work for other features without it.

## 🏗️ Technology Stack

### Backend
- **Python 3.8+** - Programming language
- **Flask 2.2.2** - Web framework
- **Amadeus Python SDK 5.0.0** - Amadeus API integration
- **python-dotenv 0.21.0** - Environment variable management
- **requests 2.28.1** - HTTP library for API calls

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **Vanilla JavaScript** - Client-side logic

## 📖 Usage Examples

### Flight Search

1. Open the application in your browser
2. Navigate to the "Flight Search" section
3. Enter:
   - **Origin:** Airport code (e.g., `JFK` for New York)
   - **Destination:** Airport code (e.g., `LHR` for London)
   - **Departure Date:** Select a future date
   - **Adults:** Number of passengers
4. Click "Search Flights"
5. Results will display flight options with prices and airlines

**Example API Call:**
```bash
curl "http://localhost:5000/api/flights?origin=JFK&destination=LHR&departure_date=2025-06-15&adults=1"
```

### Visa Requirements Check

1. Navigate to the "Visa Requirements" section
2. Enter:
   - **Origin Country Code:** ISO country code (e.g., `US`)
   - **Destination Country Code:** ISO country code (e.g., `FR`)
   - **Nationality Country Code:** Traveler's nationality (e.g., `US`)
3. Click "Check Visa"
4. Results will show visa requirements and documentation needed

**Example API Call:**
```bash
curl "http://localhost:5000/api/visa-requirements?origin=US&destination=FR&nationality=US"
```

### Find Nearest Airports

1. Navigate to the "Find Nearest Airports" section
2. Enter a location keyword (city name, e.g., `Paris`)
3. Click "Find Airports"
4. Results will show nearby airports with distances

**Example API Call:**
```bash
curl "http://localhost:5000/api/nearest-airports?keyword=Paris"
```

## 🧪 Testing

Run the test suite:

```bash
cd backend
python -m pytest tests/
```

Or run specific test files:

```bash
python -m pytest tests/test_amadeus_api.py
python -m pytest tests/test_sherpa_api.py
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET must be set"

**Solution:** Ensure your `.env` file exists in the `backend` directory and contains valid credentials. Check that you're running the application from the correct directory.

#### 2. "Could not retrieve flight offers"

**Possible Causes:**
- Invalid airport codes (use IATA codes like `JFK`, `LHR`, `CDG`)
- Date format incorrect (use `YYYY-MM-DD`)
- No flights available for the selected route/date
- API rate limit exceeded (wait a few minutes and try again)

**Solution:** Verify your input parameters and check the Amadeus API status.

#### 3. Flask server not starting

**Solution:**
- Ensure you're in the `backend` directory
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.8+)
- Check if port 5000 is already in use

#### 4. CORS Errors in Browser

**Solution:** The Flask backend needs CORS headers. If you encounter CORS issues, install flask-cors:
```bash
pip install flask-cors
```
Then add to `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

#### 5. API Rate Limits

**Solution:** 
- Amadeus Test environment has rate limits
- Wait a few minutes between requests
- Consider upgrading to a paid plan for production use

## 📁 Project Structure

```
Travel-Agent-Aid/
├── backend/
│   ├── app.py                 # Flask application and API routes
│   ├── amadeus_api.py         # Amadeus API integration
│   ├── sherpa_api.py          # Sherpa API integration
│   ├── requirements.txt       # Python dependencies
│   ├── tests/                 # Unit tests
│   └── .env                   # Environment variables (not in git)
├── frontend/
│   ├── index.html             # Main HTML file
│   ├── app.js                 # Frontend JavaScript
│   └── style.css              # Styling
├── .gitignore                 # Git ignore rules
├── .env.example               # Environment variable template
├── LICENSE                    # MIT License
├── CONTRIBUTING.md            # Contribution guidelines
└── README.md                  # This file
```

## 🔒 Security Considerations

- **Never commit `.env` files** - They contain sensitive API keys
- **Use environment variables** - All API credentials are loaded from environment variables
- **Keep API keys secure** - Don't share your API keys publicly
- **Use Test environment for development** - Only use production API keys in secure, production environments

## 🛣️ Roadmap

### Phase 1 (Current)
- ✅ Flight search with visa considerations
- ✅ Multi-modal travel suggestions
- ✅ Basic visa requirements check
- ✅ Nearest airport search

### Phase 2 (In Progress)
- 🔄 Enhanced hotel search with filtering
- 🔄 Car rental search integration
- 🔄 Improved activity recommendations

### Phase 3 (Planned)
- ⏳ AI-powered visa recommendations
- ⏳ E-visa procurement facilitation
- ⏳ Travel itinerary generation
- ⏳ Price alerts and notifications

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Usman Alex Kadiri**

## 🙏 Acknowledgments

- [Amadeus for Developers](https://developers.amadeus.com/) for travel API services
- [Sherpa](https://www.joinsherpa.com/) for visa requirement data
- Flask community for the excellent web framework

## 📞 Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

---

**Note:** This application is designed for travel agents and requires valid API credentials to function. Ensure you have set up your API keys before use.
