from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from groq_api import get_model_response

# Create the Flask app
app = Flask(__name__)

