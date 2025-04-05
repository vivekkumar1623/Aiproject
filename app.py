# this is the code of our project
from flask import Flask, render_template, request, jsonify
import requests
import wikipedia

app = Flask(__name__)


NASA_API_KEY = "5EPslw3dWVLi31xtqGgNrjMrjqXwHZLe7uYhfHNW"
NASA_MISSION_URL = "https://api.nasa.gov/techtransfer/patent/?engine&api_key=" + NASA_API_KEY
SPACEX_API_URL = "https://api.spacexdata.com/v4/launches/latest"
