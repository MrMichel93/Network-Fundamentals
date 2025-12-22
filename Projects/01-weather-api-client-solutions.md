# Weather API Client - Solutions

This document provides three different implementations of the Weather API Client, each demonstrating different levels of complexity and best practices.

## Approach 1: Beginner (Basic but Working)

This approach focuses on getting the core functionality working with minimal complexity. Perfect for learning the basics.

### Features
- Basic API call
- Simple error handling
- Console output
- Environment variable for API key

### Code

```python
#!/usr/bin/env python3
"""
Weather API Client - Beginner Approach
Simple implementation with basic error handling.
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    """
    Fetch weather data for a city from OpenWeather API.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        Dictionary with weather data, or None if error occurs
    """
    # Build the request URL with parameters
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Use Celsius
    }
    
    try:
        # Make the API request with 10 second timeout
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Error: City '{city}' not found.")
            return None
        elif response.status_code == 401:
            print("Error: Invalid API key.")
            return None
        else:
            print(f"Error: API returned status code {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please check your internet connection.")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Please check your internet.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None

def display_weather(data):
    """
    Display weather data in a readable format.
    
    Args:
        data: Dictionary containing weather data from API
    """
    if data is None:
        return
    
    # Extract data from the response
    city = data['name']
    country = data['sys']['country']
    temperature = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']
    wind_speed = data['wind'].get('speed', 0)
    
    # Display formatted weather information
    print("\n" + "="*50)
    print(f"Weather in {city}, {country}")
    print("="*50)
    print(f"Temperature: {temperature}°C (Feels like {feels_like}°C)")
    print(f"Conditions: {description.capitalize()}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print("="*50 + "\n")

def main():
    """Main function to run the weather app."""
    print("Welcome to Weather App!")
    print("-" * 50)
    
    # Check if API key is set
    if not API_KEY:
        print("Error: OPENWEATHER_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key.")
        return
    
    # Get city name from user
    city = input("Enter city name: ").strip()
    
    # Validate input
    if not city:
        print("Error: City name cannot be empty.")
        return
    
    # Fetch and display weather
    weather_data = get_weather(city)
    display_weather(weather_data)

if __name__ == '__main__':
    main()
```

### Pros
✅ Simple and easy to understand  
✅ Gets the job done  
✅ Good for learning basics  
✅ Minimal dependencies  

### Cons
❌ No caching  
❌ Limited error handling  
❌ No retry logic  
❌ Basic output formatting  
❌ No unit tests  

---

## Approach 2: Intermediate (Better Practices)

This approach adds proper code organization, caching, better error handling, and colored output.

### Features
- Organized into classes
- Response caching
- Colored console output
- Input validation
- Better error messages
- Support for multiple temperature units

### Code

```python
#!/usr/bin/env python3
"""
Weather API Client - Intermediate Approach
Implements classes, caching, and better practices.
"""

import requests
import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

class WeatherCache:
    """Simple file-based cache for weather data."""
    
    def __init__(self, cache_file='weather_cache.json', ttl=600):
        """
        Initialize cache.
        
        Args:
            cache_file: Path to cache file
            ttl: Time-to-live in seconds (default: 10 minutes)
        """
        self.cache_file = cache_file
        self.ttl = ttl
        self.cache = self._load_cache()
    
    def _load_cache(self):
        """Load cache from file."""
        if Path(self.cache_file).exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        """Save cache to file."""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get(self, key):
        """
        Get cached value if not expired.
        
        Args:
            key: Cache key (city name)
            
        Returns:
            Cached data or None if expired/missing
        """
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                print(f"{Fore.CYAN}(Using cached data){Style.RESET_ALL}")
                return entry['data']
        return None
    
    def set(self, key, value):
        """
        Store value in cache.
        
        Args:
            key: Cache key (city name)
            value: Data to cache
        """
        self.cache[key] = {
            'timestamp': time.time(),
            'data': value
        }
        self._save_cache()

class WeatherClient:
    """Client for fetching weather data from OpenWeather API."""
    
    # Weather condition emoji mapping
    WEATHER_EMOJI = {
        'clear': '☀️',
        'clouds': '☁️',
        'rain': '🌧️',
        'drizzle': '🌦️',
        'thunderstorm': '⛈️',
        'snow': '❄️',
        'mist': '🌫️',
        'fog': '🌫️',
        'haze': '🌫️'
    }
    
    def __init__(self, api_key):
        """
        Initialize weather client.
        
        Args:
            api_key: OpenWeather API key
        """
        self.api_key = api_key
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
        self.cache = WeatherCache()
    
    def get_weather(self, city, units='metric'):
        """
        Fetch weather data for a city.
        
        Args:
            city: City name
            units: 'metric' (Celsius) or 'imperial' (Fahrenheit)
            
        Returns:
            Weather data dictionary or None
        """
        # Check cache first
        cache_key = f"{city}_{units}".lower()
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Make API request
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            # Cache the result
            self.cache.set(cache_key, data)
            return data
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"{Fore.RED}✗ City '{city}' not found.{Style.RESET_ALL}")
            elif response.status_code == 401:
                print(f"{Fore.RED}✗ Invalid API key.{Style.RESET_ALL}")
            elif response.status_code == 429:
                print(f"{Fore.RED}✗ Rate limit exceeded. Please try again later.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ HTTP Error: {e}{Style.RESET_ALL}")
            return None
            
        except requests.exceptions.Timeout:
            print(f"{Fore.RED}✗ Request timed out.{Style.RESET_ALL}")
            return None
            
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}✗ Connection error. Check your internet.{Style.RESET_ALL}")
            return None
            
        except Exception as e:
            print(f"{Fore.RED}✗ Unexpected error: {e}{Style.RESET_ALL}")
            return None
    
    def get_weather_emoji(self, description):
        """
        Get emoji for weather condition.
        
        Args:
            description: Weather description
            
        Returns:
            Emoji string
        """
        desc_lower = description.lower()
        for key, emoji in self.WEATHER_EMOJI.items():
            if key in desc_lower:
                return emoji
        return '🌡️'

class WeatherDisplay:
    """Display weather data in a formatted way."""
    
    @staticmethod
    def display(data, units='metric'):
        """
        Display weather data.
        
        Args:
            data: Weather data dictionary
            units: Temperature units
        """
        if not data:
            return
        
        # Extract data
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        
        # Get appropriate emoji
        client = WeatherClient('')
        emoji = client.get_weather_emoji(description)
        
        # Temperature unit symbol
        unit_symbol = '°C' if units == 'metric' else '°F'
        
        # Display with colors
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{emoji}  Weather in {city}, {country}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}🌡️  Temperature:{Style.RESET_ALL} {temp}{unit_symbol} (feels like {feels_like}{unit_symbol})")
        print(f"{Fore.GREEN}☁️  Conditions:{Style.RESET_ALL} {description.capitalize()}")
        print(f"{Fore.GREEN}💧 Humidity:{Style.RESET_ALL} {humidity}%")
        print(f"{Fore.GREEN}💨 Wind Speed:{Style.RESET_ALL} {wind_speed} m/s")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def validate_city(city):
    """
    Validate city name input.
    
    Args:
        city: City name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not city or not city.strip():
        print(f"{Fore.RED}✗ City name cannot be empty.{Style.RESET_ALL}")
        return False
    
    if len(city) > 100:
        print(f"{Fore.RED}✗ City name too long.{Style.RESET_ALL}")
        return False
    
    return True

def main():
    """Main application entry point."""
    load_dotenv()
    
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🌍 Weather Application{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    # Check API key
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print(f"{Fore.RED}✗ OPENWEATHER_API_KEY not found in environment.{Style.RESET_ALL}")
        print("Please create a .env file with your API key.")
        return
    
    # Initialize client
    client = WeatherClient(api_key)
    
    # Get user input
    city = input(f"{Fore.CYAN}Enter city name: {Style.RESET_ALL}").strip()
    
    # Validate input
    if not validate_city(city):
        return
    
    # Fetch and display weather
    weather_data = client.get_weather(city)
    WeatherDisplay.display(weather_data)

if __name__ == '__main__':
    main()
```

### Pros
✅ Well-organized code with classes  
✅ Caching reduces API calls  
✅ Colored output for better UX  
✅ Better error handling  
✅ Input validation  
✅ Weather emojis  

### Cons
❌ No retry logic  
❌ No unit tests  
❌ Cache is file-based (not optimal)  

---

## Approach 3: Advanced (Production-Ready)

This approach includes comprehensive testing, logging, retry logic, advanced caching, and follows professional software engineering practices.

### Features
- Comprehensive error handling with retry logic
- Structured logging
- Unit tests with pytest
- Type hints
- Advanced caching with TTL
- Configuration management
- Multiple output formats (JSON, table)
- CLI argument parsing

### Code Structure

```
weather-app/
├── weather/
│   ├── __init__.py
│   ├── client.py       # API client
│   ├── cache.py        # Caching logic
│   ├── display.py      # Display formatters
│   └── config.py       # Configuration
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   └── test_cache.py
├── main.py             # Entry point
├── .env
├── requirements.txt
└── pytest.ini
```

### weather/config.py

```python
"""Configuration management for weather app."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Application configuration."""
    
    api_key: str
    base_url: str = 'https://api.openweathermap.org/data/2.5/weather'
    cache_ttl: int = 600  # 10 minutes
    request_timeout: int = 10
    max_retries: int = 3
    retry_delay: int = 1
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from environment variables."""
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if not api_key:
            raise ValueError("OPENWEATHER_API_KEY not set in environment")
        
        return cls(
            api_key=api_key,
            cache_ttl=int(os.getenv('CACHE_TTL', '600')),
            request_timeout=int(os.getenv('REQUEST_TIMEOUT', '10')),
            max_retries=int(os.getenv('MAX_RETRIES', '3'))
        )
```

### weather/cache.py

```python
"""Caching implementation with TTL support."""

import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class WeatherCache:
    """Thread-safe cache with TTL for weather data."""
    
    def __init__(self, cache_file: str = 'weather_cache.json', ttl: int = 600):
        """
        Initialize cache.
        
        Args:
            cache_file: Path to cache file
            ttl: Time-to-live in seconds
        """
        self.cache_file = Path(cache_file)
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = self._load()
    
    def _load(self) -> Dict[str, Dict[str, Any]]:
        """Load cache from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    logger.debug(f"Loaded cache from {self.cache_file}")
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load cache: {e}")
        return {}
    
    def _save(self) -> None:
        """Save cache to disk."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self._cache, f, indent=2)
            logger.debug(f"Saved cache to {self.cache_file}")
        except IOError as e:
            logger.error(f"Failed to save cache: {e}")
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached value if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached data or None
        """
        if key not in self._cache:
            logger.debug(f"Cache miss for key: {key}")
            return None
        
        entry = self._cache[key]
        age = time.time() - entry['timestamp']
        
        if age >= self.ttl:
            logger.debug(f"Cache expired for key: {key} (age: {age:.1f}s)")
            del self._cache[key]
            self._save()
            return None
        
        logger.debug(f"Cache hit for key: {key} (age: {age:.1f}s)")
        return entry['data']
    
    def set(self, key: str, value: Dict[str, Any]) -> None:
        """
        Store value in cache.
        
        Args:
            key: Cache key
            value: Data to cache
        """
        self._cache[key] = {
            'timestamp': time.time(),
            'data': value
        }
        self._save()
        logger.debug(f"Cached data for key: {key}")
    
    def clear(self) -> None:
        """Clear all cached data."""
        self._cache.clear()
        self._save()
        logger.info("Cache cleared")
```

### weather/client.py

```python
"""Weather API client with retry logic."""

import requests
import time
import logging
from typing import Optional, Dict, Any
from .config import Config
from .cache import WeatherCache

logger = logging.getLogger(__name__)

class WeatherAPIError(Exception):
    """Base exception for weather API errors."""
    pass

class CityNotFoundError(WeatherAPIError):
    """City not found in API."""
    pass

class APIKeyError(WeatherAPIError):
    """Invalid or missing API key."""
    pass

class RateLimitError(WeatherAPIError):
    """API rate limit exceeded."""
    pass

class WeatherClient:
    """Client for OpenWeather API with caching and retry logic."""
    
    def __init__(self, config: Config):
        """
        Initialize client.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.cache = WeatherCache(ttl=config.cache_ttl)
        self.session = requests.Session()
    
    def get_weather(self, city: str, units: str = 'metric') -> Dict[str, Any]:
        """
        Fetch weather data for a city with caching and retry.
        
        Args:
            city: City name
            units: Temperature units ('metric' or 'imperial')
            
        Returns:
            Weather data dictionary
            
        Raises:
            WeatherAPIError: If request fails after retries
        """
        # Check cache
        cache_key = f"{city.lower()}_{units}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Using cached weather for {city}")
            return cached
        
        # Fetch from API with retry
        data = self._fetch_with_retry(city, units)
        
        # Cache result
        self.cache.set(cache_key, data)
        
        return data
    
    def _fetch_with_retry(self, city: str, units: str) -> Dict[str, Any]:
        """
        Fetch data with exponential backoff retry.
        
        Args:
            city: City name
            units: Temperature units
            
        Returns:
            Weather data
            
        Raises:
            WeatherAPIError: If all retries fail
        """
        params = {
            'q': city,
            'appid': self.config.api_key,
            'units': units
        }
        
        for attempt in range(self.config.max_retries):
            try:
                logger.debug(f"API request attempt {attempt + 1}/{self.config.max_retries}")
                
                response = self.session.get(
                    self.config.base_url,
                    params=params,
                    timeout=self.config.request_timeout
                )
                
                # Handle specific error codes
                if response.status_code == 404:
                    raise CityNotFoundError(f"City '{city}' not found")
                elif response.status_code == 401:
                    raise APIKeyError("Invalid API key")
                elif response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                
                response.raise_for_status()
                
                logger.info(f"Successfully fetched weather for {city}")
                return response.json()
                
            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout (attempt {attempt + 1})")
                if attempt < self.config.max_retries - 1:
                    delay = self.config.retry_delay * (2 ** attempt)
                    logger.debug(f"Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    raise WeatherAPIError("Request timed out after retries")
                    
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error (attempt {attempt + 1})")
                if attempt < self.config.max_retries - 1:
                    delay = self.config.retry_delay * (2 ** attempt)
                    time.sleep(delay)
                else:
                    raise WeatherAPIError("Connection failed after retries")
                    
            except (CityNotFoundError, APIKeyError, RateLimitError):
                # Don't retry these
                raise
                
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise WeatherAPIError(f"Failed to fetch weather: {e}")
        
        raise WeatherAPIError("Failed after all retries")
```

### tests/test_client.py

```python
"""Unit tests for weather client."""

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from weather.client import WeatherClient, CityNotFoundError, APIKeyError
from weather.config import Config

@pytest.fixture
def config():
    """Create test config."""
    return Config(
        api_key='test_key',
        max_retries=3,
        retry_delay=0.1
    )

@pytest.fixture
def client(config):
    """Create test client."""
    return WeatherClient(config)

def test_get_weather_success(client):
    """Test successful weather fetch."""
    mock_response = {
        'name': 'London',
        'main': {'temp': 15, 'humidity': 70},
        'weather': [{'description': 'cloudy'}]
    }
    
    with patch.object(client.session, 'get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        result = client.get_weather('London')
        
        assert result['name'] == 'London'
        assert result['main']['temp'] == 15

def test_get_weather_city_not_found(client):
    """Test city not found error."""
    with patch.object(client.session, 'get') as mock_get:
        mock_get.return_value.status_code = 404
        
        with pytest.raises(CityNotFoundError):
            client.get_weather('InvalidCity')

def test_get_weather_invalid_api_key(client):
    """Test invalid API key error."""
    with patch.object(client.session, 'get') as mock_get:
        mock_get.return_value.status_code = 401
        
        with pytest.raises(APIKeyError):
            client.get_weather('London')

def test_get_weather_uses_cache(client):
    """Test that cache is used."""
    mock_response = {'name': 'London', 'main': {'temp': 15}}
    
    # First call - should hit API
    with patch.object(client.session, 'get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        client.get_weather('London')
    
    # Second call - should use cache
    with patch.object(client.session, 'get') as mock_get:
        result = client.get_weather('London')
        
        # API should not be called
        mock_get.assert_not_called()
        assert result['name'] == 'London'
```

### main.py

```python
"""Main entry point for weather application."""

import sys
import logging
import argparse
from weather.config import Config
from weather.client import WeatherClient, WeatherAPIError
from weather.display import WeatherDisplay

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weather.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main application logic."""
    parser = argparse.ArgumentParser(description='Weather API Client')
    parser.add_argument('city', help='City name')
    parser.add_argument('--units', choices=['metric', 'imperial'], 
                       default='metric', help='Temperature units')
    parser.add_argument('--format', choices=['console', 'json'], 
                       default='console', help='Output format')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Load configuration
        config = Config.from_env()
        
        # Create client
        client = WeatherClient(config)
        
        # Fetch weather
        logger.info(f"Fetching weather for {args.city}")
        data = client.get_weather(args.city, args.units)
        
        # Display result
        display = WeatherDisplay()
        if args.format == 'json':
            display.display_json(data)
        else:
            display.display_console(data, args.units)
        
        return 0
        
    except WeatherAPIError as e:
        logger.error(f"Weather API error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
        
    except Exception as e:
        logger.exception("Unexpected error")
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
```

### Pros
✅ Production-ready code  
✅ Comprehensive error handling  
✅ Retry logic with exponential backoff  
✅ Unit tests with pytest  
✅ Structured logging  
✅ Type hints for better IDE support  
✅ CLI argument parsing  
✅ Configurable via environment  
✅ Proper exception hierarchy  

### Cons
❌ More complex  
❌ More files to manage  
❌ Overkill for simple use cases  

---

## Comparison

| Aspect | Approach 1 | Approach 2 | Approach 3 |
|--------|-----------|------------|------------|
| **Lines of Code** | ~100 | ~250 | ~500+ |
| **Error Handling** | Basic try/catch | Good with specific errors | Comprehensive with custom exceptions |
| **Code Organization** | Single file, functions | Classes, single file | Multiple modules, packages |
| **Testing** | None | Manual only | Automated unit tests |
| **Performance** | No caching | File-based cache | Optimized cache with TTL |
| **Logging** | Print statements | Colored print | Structured logging to file |
| **Configuration** | Hardcoded | Environment vars | Config class with validation |
| **CLI** | Basic input() | Basic input() | argparse with options |
| **Retry Logic** | None | None | Exponential backoff |
| **Type Safety** | No type hints | No type hints | Full type hints |
| **Suitable For** | Learning, prototypes | Small projects | Production systems |

## When to Use Each Approach

### Use Approach 1 when:
- Learning HTTP APIs for the first time
- Building a quick prototype
- Simplicity is more important than features
- Working on a tutorial or educational project

### Use Approach 2 when:
- Building a personal project
- Need better UX with colors
- Want to reduce API calls with caching
- Need organized code without too much complexity

### Use Approach 3 when:
- Building for production use
- Need reliability and error recovery
- Want comprehensive testing
- Working in a team environment
- Need to maintain the code long-term
- Require detailed logging for debugging

## Learning Path

1. **Start with Approach 1**: Understand the basics
2. **Move to Approach 2**: Learn about classes, caching, and better UX
3. **Study Approach 3**: See professional patterns and practices

Each approach builds upon the previous one, demonstrating progressive improvement in software engineering practices.

---

[Back to Requirements](./01-weather-api-client-requirements.md) | [Back to Projects](./README.md)
