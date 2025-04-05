# this is the code of our project
from flask import Flask, render_template, request, jsonify
import requests
import wikipedia

app = Flask(__name__)


NASA_API_KEY = "5EPslw3dWVLi31xtqGgNrjMrjqXwHZLe7uYhfHNW"
NASA_MISSION_URL = "https://api.nasa.gov/techtransfer/patent/?engine&api_key=" + NASA_API_KEY
SPACEX_API_URL = "https://api.spacexdata.com/v4/launches/latest"
def get_wikipedia_info(query):
    """Fetches Wikipedia summary, page URL, and image for a mission"""
    try:
        page = wikipedia.page(query, auto_suggest=True)
        summary = wikipedia.summary(query, sentences=2)
        image = page.images[0] if page.images else ""
        return summary, page.url, image
    except wikipedia.exceptions.PageError:
        return "No Wikipedia page found for this mission.", "", ""
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple matches found: {e.options[:3]}", "", ""

def get_nasa_mission_info():
    """Fetches a NASA-related mission if available"""
    try:
        response = requests.get(NASA_MISSION_URL)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                first_result = data["results"][0]  # Taking the first available result
                mission_name = first_result[2] if len(first_result) > 2 else "NASA Mission"
                description = first_result[3] if len(first_result) > 3 else "No description available."
                return mission_name, description
    except Exception:
        pass
    return None, None

def get_spacex_mission():
    """Fetches latest SpaceX mission details"""
    try:
        response = requests.get(SPACEX_API_URL)
        if response.status_code == 200:
            data = response.json()
            mission_name = data.get("name", "Unknown SpaceX Mission")
            launch_date = data.get("date_utc", "Unknown Date")
            details = data.get("details", "No details available.")
            return f"{mission_name} (Launch Date: {launch_date}) - {details}"
    except Exception:
        pass
    return "No SpaceX mission data available."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "").strip()

    
    mission_name, nasa_description = get_nasa_mission_info()
    if mission_name and user_message.lower() in mission_name.lower():
        return jsonify({"response": f"{mission_name}: {nasa_description}", "url": "", "image": ""})

   
    summary, wiki_url, image = get_wikipedia_info(user_message)
    if summary:
        return jsonify({"response": summary, "url": wiki_url, "image": image})

    
    if "spacex" in user_message.lower() or "latest launch" in user_message.lower():
        spacex_info = get_spacex_mission()
        return jsonify({"response": spacex_info, "url": "", "image": ""})

    return jsonify({"response": "Mission details not found. Try another query.", "url": "", "image": ""})

if __name__ == '__main__':
    app.run(debug=True,port = 5000)
