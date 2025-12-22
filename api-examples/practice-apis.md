# 🌐 Public APIs for Practice

A curated collection of free APIs perfect for learning and practicing API consumption, testing, and development.

## Table of Contents
- [No Authentication Required](#no-authentication-required)
- [Simple Authentication (API Key)](#simple-authentication-api-key)
- [OAuth Required](#oauth-required)
- [Practice Challenges](#practice-challenges)

---

## No Authentication Required

These APIs are perfect for beginners - no signup or authentication needed!

### 1. JSONPlaceholder (Fake REST API)
**URL:** https://jsonplaceholder.typicode.com  
**Use for:** Basic CRUD operations, testing, prototyping  
**Rate Limits:** None

**Endpoints:**
- `GET /posts` - List all posts
- `GET /posts/1` - Get specific post
- `GET /posts/1/comments` - Get post comments
- `POST /posts` - Create post (fake)
- `PUT /posts/1` - Update post (fake)
- `PATCH /posts/1` - Partial update (fake)
- `DELETE /posts/1` - Delete post (fake)

**Example:**
```bash
# Get a post
curl https://jsonplaceholder.typicode.com/posts/1

# Create a post (fake - nothing actually saved)
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "body": "This is a test", "userId": 1}'
```

**Python Example:**
```python
import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
post = response.json()
print(f"Title: {post['title']}")
print(f"Body: {post['body']}")
```

---

### 2. HTTPBin (Request/Response Testing)
**URL:** https://httpbin.org  
**Use for:** Testing HTTP methods, headers, status codes, authentication  
**Rate Limits:** None (be reasonable)

**Endpoints:**
- `GET /get` - Returns GET request details
- `POST /post` - Returns POST request details
- `GET /status/:code` - Returns specified status code
- `GET /delay/:seconds` - Delayed response (max 10s)
- `GET /headers` - Returns request headers
- `GET /ip` - Returns origin IP
- `GET /user-agent` - Returns user agent
- `GET /uuid` - Returns a UUID
- `POST /anything` - Returns anything sent

**Example:**
```bash
# Test POST request
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 123}'

# Get a specific status code
curl https://httpbin.org/status/404

# Test delay
curl https://httpbin.org/delay/3
```

**Python Example:**
```python
import requests

# Test posting JSON
data = {"username": "alice", "password": "secret"}
response = requests.post('https://httpbin.org/post', json=data)
print(response.json()['json'])  # Echo back our data
```

---

### 3. REST Countries (Country Information)
**URL:** https://restcountries.com/v3.1  
**Use for:** Geographic data, country information  
**Rate Limits:** None

**Endpoints:**
- `GET /all` - All countries
- `GET /name/{name}` - Search by country name
- `GET /alpha/{code}` - Get by country code (US, GB, etc.)
- `GET /currency/{currency}` - Countries by currency
- `GET /region/{region}` - Countries by region

**Example:**
```bash
# Get country by name
curl https://restcountries.com/v3.1/name/germany

# Get country by code
curl https://restcountries.com/v3.1/alpha/us

# Get countries in Europe
curl https://restcountries.com/v3.1/region/europe
```

**Python Example:**
```python
import requests

response = requests.get('https://restcountries.com/v3.1/name/canada')
country = response.json()[0]
print(f"Capital: {country['capital'][0]}")
print(f"Population: {country['population']:,}")
print(f"Region: {country['region']}")
```

---

### 4. Dog CEO (Dog Images)
**URL:** https://dog.ceo/api  
**Use for:** Random images, fun API testing  
**Rate Limits:** None

**Endpoints:**
- `GET /breeds/image/random` - Random dog image
- `GET /breeds/image/random/{count}` - Multiple random images
- `GET /breeds/list/all` - List all breeds
- `GET /breed/{breed}/images` - Images for specific breed
- `GET /breed/{breed}/images/random` - Random image of breed

**Example:**
```bash
# Get random dog image
curl https://dog.ceo/api/breeds/image/random

# Get 3 random images
curl https://dog.ceo/api/breeds/image/random/3

# Get random husky image
curl https://dog.ceo/api/breed/husky/images/random
```

**Python Example:**
```python
import requests

response = requests.get('https://dog.ceo/api/breeds/image/random')
data = response.json()
print(f"Dog image URL: {data['message']}")
```

---

### 5. Bored API (Activity Suggestions)
**URL:** https://www.boredapi.com/api  
**Use for:** Random data generation  
**Rate Limits:** None

**Endpoints:**
- `GET /activity` - Random activity suggestion
- `GET /activity?type={type}` - Activity by type
- `GET /activity?participants={n}` - Activity by participant count

**Example:**
```bash
# Random activity
curl https://www.boredapi.com/api/activity

# Social activity
curl "https://www.boredapi.com/api/activity?type=social"
```

---

### 6. IP-API (Geolocation)
**URL:** http://ip-api.com/json  
**Use for:** IP geolocation lookup  
**Rate Limits:** 45 requests/minute

**Example:**
```bash
# Get your IP location
curl http://ip-api.com/json

# Get location of specific IP
curl http://ip-api.com/json/8.8.8.8
```

**Python Example:**
```python
import requests

response = requests.get('http://ip-api.com/json')
data = response.json()
print(f"Country: {data['country']}")
print(f"City: {data['city']}")
print(f"IP: {data['query']}")
```

---

### 7. Cat Facts API
**URL:** https://catfact.ninja  
**Use for:** Random text data  
**Rate Limits:** None

**Endpoints:**
- `GET /fact` - Random cat fact
- `GET /facts` - List of facts (with pagination)
- `GET /breeds` - List of cat breeds

**Example:**
```bash
curl https://catfact.ninja/fact
```

---

### 8. Numbers API
**URL:** http://numbersapi.com  
**Use for:** Fun facts about numbers  
**Rate Limits:** None

**Example:**
```bash
# Fact about number 42
curl http://numbersapi.com/42

# Math fact
curl http://numbersapi.com/42/math

# Random fact
curl http://numbersapi.com/random/trivia
```

---

### 9. JokeAPI
**URL:** https://v2.jokeapi.dev  
**Use for:** Random jokes, filtering practice  
**Rate Limits:** 120 requests/minute

**Endpoints:**
- `GET /joke/Any` - Random joke
- `GET /joke/Programming` - Programming joke
- `GET /joke/Any?type=single` - Single-line jokes only

**Example:**
```bash
# Random programming joke
curl https://v2.jokeapi.dev/joke/Programming

# Safe joke (no NSFW)
curl "https://v2.jokeapi.dev/joke/Any?safe-mode"
```

---

### 10. Advice Slip API
**URL:** https://api.adviceslip.com  
**Use for:** Random advice text  
**Rate Limits:** None (cache recommended)

**Example:**
```bash
# Random advice
curl https://api.adviceslip.com/advice

# Search for advice
curl https://api.adviceslip.com/advice/search/life
```

---

### 11. Open-Meteo (Weather)
**URL:** https://api.open-meteo.com/v1  
**Use for:** Weather data without API key  
**Rate Limits:** 10,000 requests/day

**Example:**
```bash
# Weather for coordinates (New York)
curl "https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.01&current_weather=true"
```

**Python Example:**
```python
import requests

params = {
    'latitude': 40.71,
    'longitude': -74.01,
    'current_weather': True
}
response = requests.get('https://api.open-meteo.com/v1/forecast', params=params)
weather = response.json()['current_weather']
print(f"Temperature: {weather['temperature']}°C")
print(f"Wind Speed: {weather['windspeed']} km/h")
```

---

### 12. Agify.io (Predict Age from Name)
**URL:** https://api.agify.io  
**Use for:** Name-based predictions  
**Rate Limits:** 1000 requests/day

**Example:**
```bash
curl "https://api.agify.io?name=michael"
```

---

### 13. Random User Generator
**URL:** https://randomuser.me/api  
**Use for:** Fake user data for testing  
**Rate Limits:** None

**Example:**
```bash
# Generate 1 random user
curl https://randomuser.me/api/

# Generate 5 users
curl "https://randomuser.me/api/?results=5"
```

---

### 14. Quotes API (ZenQuotes)
**URL:** https://zenquotes.io/api  
**Use for:** Inspirational quotes  
**Rate Limits:** 5 requests/30 seconds

**Example:**
```bash
# Random quote
curl https://zenquotes.io/api/random

# Today's quote
curl https://zenquotes.io/api/today
```

---

### 15. CoinGecko (Cryptocurrency)
**URL:** https://api.coingecko.com/api/v3  
**Use for:** Crypto prices (no auth for basic features)  
**Rate Limits:** 10-50 requests/minute

**Example:**
```bash
# Bitcoin price
curl https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd

# List of coins
curl "https://api.coingecko.com/api/v3/coins/list"
```

---

## Simple Authentication (API Key)

These APIs require a free API key - great for learning authentication!

### 1. OpenWeatherMap
**URL:** https://api.openweathermap.org/data/2.5  
**Signup:** https://openweathermap.org/api  
**Free Tier:** 1,000 calls/day

**Example:**
```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
```

**Python Example:**
```python
import requests

API_KEY = 'your_api_key_here'
city = 'London'

response = requests.get(
    'https://api.openweathermap.org/data/2.5/weather',
    params={'q': city, 'appid': API_KEY, 'units': 'metric'}
)
data = response.json()
print(f"Temperature: {data['main']['temp']}°C")
```

---

### 2. NewsAPI
**URL:** https://newsapi.org/v2  
**Signup:** https://newsapi.org/register  
**Free Tier:** 100 requests/day, 1000/month

**Example:**
```bash
curl "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY"
```

---

### 3. Alpha Vantage (Stock Market)
**URL:** https://www.alphavantage.co/query  
**Signup:** https://www.alphavantage.co/support/#api-key  
**Free Tier:** 5 requests/minute, 500/day

**Example:**
```bash
# Stock quote
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apiKey=YOUR_API_KEY"
```

---

### 4. NASA API
**URL:** https://api.nasa.gov  
**Signup:** https://api.nasa.gov/#signUp  
**Free Tier:** 1000 requests/hour

**Endpoints:**
- APOD (Astronomy Picture of the Day)
- Mars Rover Photos
- Earth Imagery

**Example:**
```bash
# Astronomy Picture of the Day
curl "https://api.nasa.gov/planetary/apod?api_key=YOUR_API_KEY"
```

**Python Example:**
```python
import requests

API_KEY = 'your_api_key_here'
response = requests.get(
    'https://api.nasa.gov/planetary/apod',
    params={'api_key': API_KEY}
)
apod = response.json()
print(f"Title: {apod['title']}")
print(f"Explanation: {apod['explanation']}")
print(f"Image: {apod['url']}")
```

---

### 5. TMDB (The Movie Database)
**URL:** https://api.themoviedb.org/3  
**Signup:** https://www.themoviedb.org/settings/api  
**Free Tier:** 40 requests/10 seconds

**Example:**
```bash
# Search for movies
curl "https://api.themoviedb.org/3/search/movie?api_key=YOUR_API_KEY&query=Inception"
```

---

### 6. Giphy (GIFs)
**URL:** https://api.giphy.com/v1  
**Signup:** https://developers.giphy.com/  
**Free Tier:** 42 requests/hour

**Example:**
```bash
# Search for GIFs
curl "https://api.giphy.com/v1/gifs/search?api_key=YOUR_API_KEY&q=cats&limit=5"
```

---

### 7. ExchangeRate-API
**URL:** https://v6.exchangerate-api.com/v6  
**Signup:** https://www.exchangerate-api.com/  
**Free Tier:** 1,500 requests/month

**Example:**
```bash
# Get USD exchange rates
curl "https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/USD"
```

---

### 8. IPGeolocation
**URL:** https://api.ipgeolocation.io  
**Signup:** https://ipgeolocation.io/signup.html  
**Free Tier:** 1,000 requests/day

**Example:**
```bash
curl "https://api.ipgeolocation.io/ipgeo?apiKey=YOUR_API_KEY"
```

---

### 9. Abstract API
**URL:** https://www.abstractapi.com  
**Signup:** https://app.abstractapi.com/users/signup  
**Free Tier:** Various limits per service

Services include: Email validation, IP geolocation, Phone validation, etc.

---

### 10. Spoonacular (Food/Recipes)
**URL:** https://api.spoonacular.com  
**Signup:** https://spoonacular.com/food-api  
**Free Tier:** 150 requests/day

**Example:**
```bash
# Search recipes
curl "https://api.spoonacular.com/recipes/complexSearch?query=pasta&apiKey=YOUR_API_KEY"
```

---

## OAuth Required

Advanced authentication - perfect for learning OAuth 2.0!

### 1. GitHub API (Full Access)
**URL:** https://api.github.com  
**Docs:** https://docs.github.com/en/rest  
**OAuth:** Required for write operations and higher rate limits

**Without OAuth:** 60 requests/hour  
**With OAuth:** 5,000 requests/hour

**Setup:**
1. Create OAuth app at https://github.com/settings/developers
2. Get client ID and secret
3. Implement OAuth flow

**Example (with Personal Access Token):**
```bash
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
```

---

### 2. Twitter API v2
**URL:** https://api.twitter.com/2  
**Docs:** https://developer.twitter.com/en/docs  
**OAuth:** OAuth 2.0 required

**Example (with Bearer Token):**
```bash
curl -H "Authorization: Bearer YOUR_BEARER_TOKEN" \
  "https://api.twitter.com/2/tweets/search/recent?query=python"
```

---

### 3. Google APIs
**URL:** Various (Gmail, Drive, Calendar, etc.)  
**Docs:** https://developers.google.com/apis-explorer  
**OAuth:** OAuth 2.0 required for user data

Examples: Gmail API, Google Drive API, Google Calendar API

---

## Practice Challenges

### Challenge 1: API Explorer Tool 🔍
Build a command-line tool that:
- Tests all HTTPBin endpoints systematically
- Displays formatted results
- Compares expected vs actual responses
- Handles errors gracefully

**Skills practiced:**
- Making different HTTP requests
- Error handling
- JSON parsing
- Output formatting

**Starter code:**
```python
import requests

class APIExplorer:
    def __init__(self):
        self.base_url = 'https://httpbin.org'
    
    def test_get(self):
        """Test GET endpoint"""
        response = requests.get(f'{self.base_url}/get')
        # TODO: Parse and display results
    
    def test_post(self):
        """Test POST endpoint"""
        # TODO: Implement
    
    def test_status_codes(self):
        """Test various status codes"""
        # TODO: Implement

# Run all tests
explorer = APIExplorer()
explorer.test_get()
```

---

### Challenge 2: Multi-API Dashboard 📊
Create a "daily dashboard" that combines data from multiple APIs:

**Required APIs:**
- Weather API (Open-Meteo) - Current weather
- News API - Top headlines
- Quote API (ZenQuotes) - Inspirational quote
- Crypto API (CoinGecko) - Bitcoin price

**Features:**
- Fetch all data in parallel
- Display in formatted dashboard
- Handle failures gracefully
- Cache results for 1 hour

**Sample output:**
```
╔════════════════════════════════════════╗
║        DAILY DASHBOARD                 ║
╠════════════════════════════════════════╣
║ WEATHER                                ║
║ New York: 72°F, Sunny                  ║
║                                        ║
║ TOP NEWS                               ║
║ • Breaking: ...                        ║
║ • Tech: ...                            ║
║                                        ║
║ QUOTE OF THE DAY                       ║
║ "Success is not final..." - Churchill  ║
║                                        ║
║ CRYPTO                                 ║
║ Bitcoin: $45,234.56 USD                ║
╚════════════════════════════════════════╝
```

**Starter code:**
```python
import requests
from concurrent.futures import ThreadPoolExecutor

def fetch_weather():
    # TODO: Implement
    pass

def fetch_news():
    # TODO: Implement
    pass

def fetch_quote():
    # TODO: Implement
    pass

def fetch_crypto():
    # TODO: Implement
    pass

def main():
    # Use ThreadPoolExecutor for parallel requests
    with ThreadPoolExecutor(max_workers=4) as executor:
        weather = executor.submit(fetch_weather)
        news = executor.submit(fetch_news)
        quote = executor.submit(fetch_quote)
        crypto = executor.submit(fetch_crypto)
        
        # Get results
        # TODO: Display formatted dashboard

if __name__ == '__main__':
    main()
```

---

### Challenge 3: API Rate Limiter 🚦
Build a rate-limiting wrapper for API calls:

**Requirements:**
- Track requests per time window
- Queue requests when limit reached
- Retry with exponential backoff
- Log rate limit status

---

### Challenge 4: API Response Cache 💾
Implement a caching system:

**Features:**
- Cache responses with TTL
- Invalidate on demand
- Memory-efficient
- Handle cache misses

---

### Challenge 5: API Error Recovery 🔄
Create a robust API client:

**Features:**
- Automatic retry on failures
- Circuit breaker pattern
- Fallback responses
- Detailed error logging

---

## Tips for Working with APIs 💡

1. **Always read the documentation first** - Save time by understanding before coding
2. **Test with curl first** - Verify the API works before writing code
3. **Handle errors gracefully** - Networks fail, APIs change
4. **Respect rate limits** - Use delays, caching, or upgrade plans
5. **Use environment variables** - Never hardcode API keys
6. **Log everything** - Debug issues faster with good logging
7. **Use sessions** - Reuse connections for better performance
8. **Set timeouts** - Don't wait forever for responses
9. **Validate responses** - Check status codes and data structure
10. **Read the terms of service** - Know what you're allowed to do

---

## Additional Resources 📚

- [Public APIs GitHub](https://github.com/public-apis/public-apis) - 1000+ free APIs
- [RapidAPI](https://rapidapi.com/) - API marketplace
- [Postman Learning Center](https://learning.postman.com/) - API testing
- [REST API Tutorial](https://restfulapi.net/) - Best practices

---

[← Back to Main](../README.md) | [Try Local Practice API →](./local-practice-api/)
