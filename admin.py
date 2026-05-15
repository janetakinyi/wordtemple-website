import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# File paths
ADMIN_FILE = 'admin_users.json'
REGISTRATIONS_FILE = 'registrations.json'
SETTINGS_FILE = 'settings.json'
QUOTES_FILE = 'quotes_data.json'
EVENTS_FILE = 'events_data.json'

def init_admin():
    if not os.path.exists(ADMIN_FILE):
        default_admin = {
            "website": {
                "password": generate_password_hash("wordtempl32025"),
                "role": "super_admin",
                "created": str(datetime.now())
            }
        }
        with open(ADMIN_FILE, 'w') as f:
            json.dump(default_admin, f, indent=2)
        print("✅ Admin user created. Username: admin | Password: wordtemple2026")

def verify_admin(username, password):
    if not os.path.exists(ADMIN_FILE):
        init_admin()
    
    with open(ADMIN_FILE, 'r') as f:
        admins = json.load(f)
    
    if username in admins:
        return check_password_hash(admins[username]['password'], password)
    return False

def save_registration(data):
    registrations = []
    if os.path.exists(REGISTRATIONS_FILE):
        with open(REGISTRATIONS_FILE, 'r') as f:
            registrations = json.load(f)
    
    data['id'] = len(registrations) + 1
    data['date_registered'] = str(datetime.now())
    registrations.append(data)
    
    with open(REGISTRATIONS_FILE, 'w') as f:
        json.dump(registrations, f, indent=2)
    return True

def get_registrations():
    if os.path.exists(REGISTRATIONS_FILE):
        with open(REGISTRATIONS_FILE, 'r') as f:
            return json.load(f)
    return []

def get_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

def update_quotes(quotes_list):
    with open(QUOTES_FILE, 'w') as f:
        json.dump(quotes_list, f, indent=2)

def get_quotes():
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, 'r') as f:
            return json.load(f)
    return []

def update_events(events_list):
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events_list, f, indent=2)

def get_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'r') as f:
            return json.load(f)
    return []

init_admin()
