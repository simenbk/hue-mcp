import os
from dotenv import load_dotenv

load_dotenv()

# Hue
HUE_IP = os.getenv('HUE_IP')
HUE_USERNAME = os.getenv('HUE_USERNAME')