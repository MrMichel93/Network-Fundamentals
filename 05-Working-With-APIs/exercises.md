# 🏋️ Exercises: Working With APIs

Practice consuming APIs with different tools and handling responses.

## Exercise 1: GitHub API Exploration 🔍

**Objective**: Learn to read API documentation and make requests.

**Tasks**:
1. Read GitHub API docs: https://docs.github.com/en/rest
2. Use Python requests to get user info:
   ```python
   import requests
   response = requests.get('https://api.github.com/users/octocat')
   print(response.json())
   ```
3. Answer: How many public repos does octocat have?

**Success Criteria**: You can fetch and parse API responses.

---

## Exercise 2: Handle Query Parameters 🔧

**Objective**: Learn to send query parameters.

**Task**: Search GitHub repositories for "python machine learning"

```python
import requests

params = {
    'q': 'python machine learning',
    'sort': 'stars'
}

response = requests.get(
    'https://api.github.com/search/repositories',
    params=params
)

data = response.json()
print(f"Total count: {data['total_count']}")
print(f"Top repo: {data['items'][0]['name']}")
```

**Success Criteria**: You understand query parameters.

---

## Exercise 3: Error Handling 🚨

**Objective**: Handle API errors properly.

**Task**: Try to fetch a non-existent user and handle the error.

```python
import requests

response = requests.get('https://api.github.com/users/thisuserdoesnotexist12345')

if response.status_code == 404:
    print("User not found!")
elif response.ok:
    data = response.json()
    print(f"User: {data['login']}")
else:
    print(f"Error: {response.status_code}")
```

**Success Criteria**: Your code handles errors gracefully.

---

## Exercise 4: POST Request 📤

**Objective**: Send data to an API.

**Task**: Create a new post using JSONPlaceholder.

```python
import requests

data = {
    'title': 'My Test Post',
    'body': 'This is a test',
    'userId': 1
}

response = requests.post(
    'https://jsonplaceholder.typicode.com/posts',
    json=data
)

print(f"Status: {response.status_code}")
print(f"Created post: {response.json()}")
```

**Success Criteria**: You can send JSON data with POST requests.

---

## Exercise 5: Weather API 🌤️

**Objective**: Work with a real API that requires authentication.

**Tasks**:
1. Sign up for free API key at https://openweathermap.org/api
2. Get weather for your city:

```python
import requests
import os

API_KEY = os.environ.get('WEATHER_API_KEY')  # Set this environment variable
city = 'London'

url = 'https://api.openweathermap.org/data/2.5/weather'
params = {
    'q': city,
    'appid': API_KEY,
    'units': 'metric'
}

response = requests.get(url, params=params)

if response.ok:
    data = response.json()
    temp = data['main']['temp']
    desc = data['weather'][0]['description']
    print(f"Weather in {city}: {temp}°C, {desc}")
else:
    print(f"Error: {response.status_code}")
```

**Success Criteria**: You can work with authenticated APIs.

---

## Challenge Exercise: API Wrapper 🎯

**Objective**: Create a reusable API client class.

**Task**: Build a GitHub API wrapper.

```python
import requests

class GitHubAPI:
    BASE_URL = 'https://api.github.com'
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json'
        })
    
    def get_user(self, username):
        response = self.session.get(f'{self.BASE_URL}/users/{username}')
        response.raise_for_status()
        return response.json()
    
    def get_repos(self, username):
        response = self.session.get(f'{self.BASE_URL}/users/{username}/repos')
        response.raise_for_status()
        return response.json()

# Usage
api = GitHubAPI()
user = api.get_user('octocat')
print(f"User: {user['login']}, Repos: {user['public_repos']}")

repos = api.get_repos('octocat')
for repo in repos[:3]:
    print(f"- {repo['name']}: {repo['description']}")
```

**Success Criteria**: You understand object-oriented API design.

---

## What's Next?

Once you're comfortable working with APIs, learn about [Authentication and Authorization](../06-Authentication-and-Authorization/)!

---

[← Back to Lesson](./README.md)
