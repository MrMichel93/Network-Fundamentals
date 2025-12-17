# 🌤️ Project 1: Weather API Client

**Difficulty**: Beginner  
**Time**: 2-3 hours  
**Concepts**: HTTP requests, JSON parsing, error handling, API keys

## Project Description

Build a command-line weather application that fetches real-time weather data from a public API and displays it in a user-friendly format.

## Learning Objectives

- Make HTTP GET requests to external APIs
- Parse and process JSON responses
- Handle errors gracefully
- Work with API keys and authentication
- Format and display data to users

## Requirements

### Functional Requirements

1. **Fetch weather data** for a given city
2. **Display current conditions**: temperature, humidity, description
3. **Show 3-day forecast**
4. **Handle invalid cities** gracefully
5. **Cache results** to reduce API calls
6. **Colorful console output** for better UX

### Technical Requirements

- Use Python with `requests` library
- Use OpenWeatherMap API (free tier)
- Include error handling
- Follow best practices for API key management

## Getting Started

### Step 1: Get an API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for free account
3. Get your API key from the dashboard
4. Free tier allows 60 calls/minute, 1,000,000 calls/month

### Step 2: Project Structure

```
weather-app/
├── weather_client.py    # Main application
├── .env                 # API key (don't commit!)
├── .gitignore          # Ignore .env
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

### Step 3: Install Dependencies

```bash
pip install requests python-dotenv colorama
```

## Implementation Guide

### Basic Structure

```python
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5'

def get_current_weather(city):
    """Fetch current weather for a city."""
    url = f'{BASE_URL}/weather'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Celsius
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"City '{city}' not found")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def display_weather(data):
    """Display weather data in a formatted way."""
    if not data:
        return
    
    city = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']
    
    print(f"\n🌤️  Weather in {city}, {country}")
    print(f"━" * 40)
    print(f"🌡️  Temperature: {temp}°C (feels like {feels_like}°C)")
    print(f"💧 Humidity: {humidity}%")
    print(f"☁️  Conditions: {description.capitalize()}")
    print(f"━" * 40)

def main():
    print("🌍 Weather App")
    print("=" * 40)
    
    city = input("Enter city name: ").strip()
    
    if not city:
        print("Please enter a valid city name")
        return
    
    weather = get_current_weather(city)
    display_weather(weather)

if __name__ == '__main__':
    main()
```

## Features to Add (Progressive Difficulty)

### ⭐ Level 1: Basic Features
- [x] Fetch current weather
- [ ] Display temperature and conditions
- [ ] Handle invalid cities
- [ ] Format output nicely

### ⭐⭐ Level 2: Intermediate Features
- [ ] Show 5-day forecast
- [ ] Add icons for weather conditions (☀️ ☁️ 🌧️ ❄️)
- [ ] Support multiple temperature units (Celsius, Fahrenheit)
- [ ] Add wind speed and direction
- [ ] Show sunrise/sunset times

### ⭐⭐⭐ Level 3: Advanced Features
- [ ] Cache responses for 10 minutes
- [ ] Support multiple cities at once
- [ ] Save favorite cities
- [ ] Compare weather between cities
- [ ] Add command-line arguments (e.g., `--city Boston --units F`)
- [ ] Export data to JSON/CSV

## Challenges

### Challenge 1: Add 5-Day Forecast

```python
def get_forecast(city):
    """Get 5-day forecast."""
    url = f'{BASE_URL}/forecast'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'cnt': 5  # 5 forecasts
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def display_forecast(data):
    """Display forecast."""
    print("\n📅 5-Day Forecast")
    print("━" * 40)
    
    for item in data['list']:
        date = item['dt_txt']
        temp = item['main']['temp']
        desc = item['weather'][0]['description']
        print(f"{date}: {temp}°C - {desc}")
```

### Challenge 2: Weather Icons

```python
WEATHER_ICONS = {
    'clear': '☀️',
    'clouds': '☁️',
    'rain': '🌧️',
    'drizzle': '🌦️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'mist': '🌫️',
    'fog': '🌫️'
}

def get_weather_icon(description):
    """Get emoji icon for weather."""
    desc_lower = description.lower()
    for key in WEATHER_ICONS:
        if key in desc_lower:
            return WEATHER_ICONS[key]
    return '🌡️'
```

### Challenge 3: Caching

```python
import json
import time
from pathlib import Path

CACHE_FILE = 'weather_cache.json'
CACHE_DURATION = 600  # 10 minutes

def load_cache():
    """Load cached weather data."""
    if Path(CACHE_FILE).exists():
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    """Save weather data to cache."""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_cached_weather(city):
    """Get weather from cache if recent."""
    cache = load_cache()
    
    if city in cache:
        cached_time = cache[city]['timestamp']
        if time.time() - cached_time < CACHE_DURATION:
            return cache[city]['data']
    
    return None

def cache_weather(city, data):
    """Cache weather data."""
    cache = load_cache()
    cache[city] = {
        'timestamp': time.time(),
        'data': data
    }
    save_cache(cache)
```

## Testing

Test your application with:
- Valid cities: London, Tokyo, New York
- Invalid cities: XYZ123, ""
- Special characters: São Paulo, Zürich
- Network issues: disconnect internet and test error handling

## Success Criteria

- ✅ Fetches real weather data from API
- ✅ Displays current conditions clearly
- ✅ Handles errors gracefully (invalid city, network issues)
- ✅ API key stored securely (.env file)
- ✅ Clean, formatted output
- ✅ Code is well-commented
- ✅ Includes README with setup instructions

## Extensions

Want more challenge? Try:
- Build a GUI with Tkinter
- Add weather alerts/warnings
- Create a web version with Flask
- Add location auto-detection (IP-based)
- Integrate with other weather APIs
- Add historical weather data comparison

## Resources

- [OpenWeatherMap API Docs](https://openweathermap.org/api)
- [requests library docs](https://requests.readthedocs.io/)
- [python-dotenv docs](https://pypi.org/project/python-dotenv/)

## Next Steps

Once complete, move to [Project 2: URL Shortener](./02-url-shortener.md)!

---

[Back to Projects](./README.md)
