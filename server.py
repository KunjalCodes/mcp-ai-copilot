from mcp.server.fastmcp import FastMCP
import requests
import urllib.parse
import json
import os



print("Starting MCP server...")

mcp = FastMCP("AI Copilot")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone"""
    return f"Hello, {name}! MCP is working 🎉"

@mcp.tool()
def calculate(a: float, b: float, op: str) -> str:
    """Simple calculator: add, subtract, multiply, divide"""
    if op == "add":
        return str(a + b)

    elif op == "subtract":
        return str(a - b)

    elif op == "multiply":
        return str(a * b)

    elif op == "divide":
        if b == 0:
            return "Cannot divide by zero"
        return str(a / b)
    else:
        return "Invalid operation"

@mcp.tool()
def wiki_search(query: str) -> str:
    """Search Wikipedia and return a summary"""

    headers = {
        "User-Agent": "MCP-Learning-Project/1.0"
    }

    try:
        # Step 1: search
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }

        search_res = requests.get(
            search_url,
            params=params,
            headers=headers
        ).json()

        if not search_res["query"]["search"]:
            return "No results found."

        title = search_res["query"]["search"][0]["title"]

        # Step 2: summary
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"

        summary_res = requests.get(
            summary_url,
            headers=headers
        ).json()

        return summary_res.get("extract", "No summary found.")

    except Exception as e:
        return f"Error: {str(e)}"
    
@mcp.tool()
def get_weather(location: str) -> str:
    """Get current weather using location name"""

    try:
        # Step 1: geocode location
        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
            f"?name={location}&count=1"
        )

        geo_res = requests.get(geo_url).json()

        if "results" not in geo_res:
            return "Location not found."

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]

        # Step 2: get weather
        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current_weather=true"
        )

        weather_res = requests.get(weather_url).json()

        temp = weather_res["current_weather"]["temperature"]
        wind = weather_res["current_weather"]["windspeed"]

        return f"{location}: {temp}°C, Wind {wind} km/h"

    except Exception as e:
        return f"Error: {str(e)}"
    
NOTES_FILE = "notes.json"

# Ensure file exists
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w") as f:
        json.dump([], f)


@mcp.tool()
def save_note(note: str) -> str:
    """Save a note to memory"""

    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)

    notes.append(note)

    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)

    return "Note saved!"


@mcp.tool()
def get_notes() -> str:
    """Retrieve saved notes"""

    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)

    if not notes:
        return "No notes yet."

    return "\n".join(notes)



if __name__ == "__main__":
    print("MCP server is running...")
    mcp.run()
