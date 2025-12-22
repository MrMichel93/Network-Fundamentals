# Project 1: Weather API Client - Requirements

## Learning Objectives
By completing this project, you will:
- [ ] Make HTTP requests programmatically
- [ ] Parse JSON responses
- [ ] Handle errors gracefully
- [ ] Use API keys securely
- [ ] Display data to users
- [ ] Work with environment variables
- [ ] Implement caching strategies
- [ ] Format console output effectively

## Requirements

### Functional Requirements
1. **User Input**: User can enter a city name
2. **API Integration**: App fetches weather data from OpenWeather API
3. **Data Display**: App displays:
   - Current temperature (Celsius and Fahrenheit)
   - Weather description
   - Humidity percentage
   - Wind speed
   - "Feels like" temperature
4. **Error Handling**: App handles errors:
   - Invalid city name
   - API unavailable/down
   - Network connectivity issues
   - Invalid API key
   - Rate limiting
5. **Input Validation**: Validates city name input before making API calls
6. **Cache Results**: Caches weather data to reduce unnecessary API calls (10-minute TTL)

### Non-Functional Requirements
- **Performance**: Response time under 2 seconds for cached data, under 5 seconds for API calls
- **Security**: API key stored securely (environment variable, not in code)
- **Usability**: User-friendly error messages with actionable suggestions
- **Code Quality**: Clean, readable code with appropriate comments
- **Reliability**: Handles network failures gracefully with retry logic
- **Maintainability**: Modular code structure with separation of concerns

## Technical Specifications

**API**: OpenWeather API (free tier - 60 calls/min, 1M calls/month)  
**Language**: Python 3.8+ or JavaScript (Node.js 14+)  
**Libraries**: 
- Python: `requests`, `python-dotenv`, `colorama`
- JavaScript: `axios`, `dotenv`, `chalk`

**API Endpoint**: `https://api.openweathermap.org/data/2.5/weather`

**Required API Parameters**:
- `q`: City name
- `appid`: Your API key
- `units`: metric (for Celsius) or imperial (for Fahrenheit)

## Milestones

### Milestone 1: Basic Request (Due: Week 1, Day 1-2)
- [ ] Sign up for OpenWeather API key
- [ ] Set up project structure
- [ ] Install required dependencies
- [ ] Make successful API call with hardcoded city
- [ ] Print raw JSON response
- [ ] Store API key in .env file

**Success Criteria**: Successfully fetch and print raw weather data for at least one city.

### Milestone 2: Parse Data (Due: Week 1, Day 3-4)
- [ ] Extract temperature from JSON response
- [ ] Extract weather description
- [ ] Extract humidity and wind speed
- [ ] Format output in a readable way
- [ ] Add colored console output
- [ ] Display appropriate weather emoji

**Success Criteria**: Display formatted weather information including temperature, description, humidity, and wind speed.

### Milestone 3: User Input (Due: Week 2, Day 1-2)
- [ ] Accept city name from user via console input
- [ ] Validate input (non-empty, reasonable length)
- [ ] Sanitize input (trim whitespace, handle special characters)
- [ ] Make request with user-provided city
- [ ] Handle multiple consecutive requests

**Success Criteria**: User can input any city name and receive weather information.

### Milestone 4: Error Handling (Due: Week 2, Day 3-4)
- [ ] Handle invalid city (404 error)
- [ ] Handle API errors (401, 429, 500)
- [ ] Handle network errors (timeout, connection refused)
- [ ] Display friendly, actionable error messages
- [ ] Log errors for debugging
- [ ] Implement retry logic for transient failures

**Success Criteria**: App handles all common error scenarios gracefully without crashing.

### Milestone 5: Polish (Due: Week 2, Day 5-7)
- [ ] Add caching to reduce API calls
- [ ] Add more weather data (sunrise/sunset, visibility)
- [ ] Improve formatting with colors and icons
- [ ] Add unit tests for key functions
- [ ] Document code with docstrings
- [ ] Create comprehensive README

**Success Criteria**: Production-ready app with caching, comprehensive error handling, and documentation.

## Starter Code

### Python Template

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    """
    Fetch weather data for a given city.
    
    Args:
        city (str): Name of the city
        
    Returns:
        dict: Weather data or None if error
    """
    # TODO: Implement API call
    pass

def display_weather(data):
    """
    Display weather data in a formatted way.
    
    Args:
        data (dict): Weather data from API
    """
    # TODO: Implement display logic
    pass

def main():
    """Main application entry point."""
    print("Weather App")
    city = input("Enter city name: ")
    
    # TODO: Validate input
    # TODO: Fetch weather
    # TODO: Display results

if __name__ == '__main__':
    main()
```

### .env Template

```
OPENWEATHER_API_KEY=your_api_key_here
```

### requirements.txt

```
requests>=2.31.0
python-dotenv>=1.0.0
colorama>=0.4.6
```

## Testing Checklist

### Functional Testing
- [ ] Works with valid city names (London, Tokyo, New York)
- [ ] Handles invalid city names gracefully
- [ ] Handles special characters in city names (São Paulo, Zürich)
- [ ] Displays all required weather information
- [ ] Cache works correctly (doesn't make duplicate API calls)
- [ ] Cache expires after TTL

### Error Handling Testing
- [ ] Handles no internet connection
- [ ] Handles invalid API key
- [ ] Handles API rate limiting (429 error)
- [ ] Handles API server errors (500 error)
- [ ] Handles empty input
- [ ] Handles very long city names

### Code Quality Testing
- [ ] Code follows style guidelines (PEP 8 for Python)
- [ ] All functions have docstrings
- [ ] No hardcoded credentials
- [ ] No sensitive data in git repository
- [ ] Code is modular and reusable

## Rubric

| Criteria | Needs Work (1) | Good (2) | Excellent (3) |
|----------|---------------|----------|---------------|
| **Functionality** | Missing key features (no user input or error handling) | All basic features work (fetch, display, input) | All features + edge cases handled + caching |
| **Error Handling** | No error handling, app crashes | Basic error handling with try/catch | Comprehensive error handling with specific messages and recovery |
| **Code Quality** | Hard to read, no structure | Readable with some organization | Clean, well-documented, modular code |
| **Security** | API key in code or committed to git | API key in .env file but not in .gitignore | API key in env var + .gitignore + security best practices |
| **User Experience** | Plain text, unclear messages | Formatted output with basic styling | Colored output, emojis, clear messages, intuitive flow |
| **Testing** | No testing | Manual testing performed | Automated tests + comprehensive test cases |

**Scoring**:
- 16-18 points: Excellent (Production-ready)
- 12-15 points: Good (Functional with room for improvement)
- 6-11 points: Needs Work (Missing key components)
- Below 6: Incomplete

## Extensions (Optional)

### Beginner Extensions
- [ ] Add 5-day forecast
- [ ] Support multiple temperature units (toggle between C/F)
- [ ] Display weather icons/emojis based on conditions
- [ ] Show local time in the queried city

### Intermediate Extensions
- [ ] Save favorite cities to a file
- [ ] Compare weather between multiple cities
- [ ] Add command-line arguments (e.g., `--city Boston --units F`)
- [ ] Export weather data to JSON/CSV file
- [ ] Add weather alerts and warnings

### Advanced Extensions
- [ ] Create a web interface using Flask/FastAPI
- [ ] Build a GUI using Tkinter or PyQt
- [ ] Add location auto-detection using IP geolocation
- [ ] Integrate multiple weather APIs for comparison
- [ ] Add historical weather data and trends
- [ ] Implement weather predictions/forecasting
- [ ] Create a weather notification system

## Common Pitfalls to Avoid

1. **Hardcoding API keys**: Never put API keys directly in code
2. **Not handling errors**: Always expect API calls to fail
3. **Making too many API calls**: Implement caching to respect rate limits
4. **Poor error messages**: "Error" is not helpful - be specific
5. **Ignoring edge cases**: Empty input, special characters, very long strings
6. **Not validating data**: Check if API response has expected fields
7. **Committing sensitive files**: Always use .gitignore for .env files

## Resources

- [OpenWeather API Documentation](https://openweathermap.org/api)
- [Python requests library](https://requests.readthedocs.io/)
- [python-dotenv documentation](https://pypi.org/project/python-dotenv/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [JSON in Python](https://docs.python.org/3/library/json.html)

## Next Steps

Once you complete this project, proceed to [Project 2: URL Shortener](./02-url-shortener.md) to learn about building RESTful APIs!

---

[Back to Projects](./README.md)
