import os
import json
from datetime import datetime

# Data file paths
EVENTS_FILE = 'data/events.json'
SETTINGS_FILE = 'data/settings.json'
QUOTES_FILE = 'data/quotes.json'
REGISTRATIONS_FILE = 'data/registrations.json'
ADMIN_FILE = 'data/admin_users.json'

# Make sure data directory exists
os.makedirs('data', exist_ok=True)

# ---------- SETTINGS ----------
def get_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {
        'theme_2026': 'SUPERNATURAL BREAKTHROUGHS',
        'theme_scripture': '2 Samuel 5:20 (NKJV)',
        'theme_verse': 'So David came to Baal Perazim...',
        'theme_month': 'JULY 2026 | HAVE DOMINION',
        'theme_month_scripture': 'Genesis 1:26',
        'theme_month_verse': '"Let Us make man in Our image..."',
        'announcements': [],
        'services': {
            'sunday': [],
            'weekly': []
        }
    }

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

# ---------- ADMIN ----------
def verify_admin(username, password):
    if username == 'admin' and password == 'admin123':
        return True
    if os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, 'r') as f:
            admins = json.load(f)
            for admin in admins:
                if admin.get('username') == username and admin.get('password') == password:
                    return True
    return False

# ---------- EVENTS ----------
def get_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_events(events):
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f, indent=2)

def delete_event(event_id):
    events = get_events()
    events = [e for e in events if e.get('id') != event_id and e.get('filename') != event_id]
    save_events(events)
    return True

# ---------- QUOTES ----------
def get_quotes():
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, 'r') as f:
            return json.load(f)
    return []

def update_quotes(quotes):
    with open(QUOTES_FILE, 'w') as f:
        json.dump(quotes, f, indent=2)

# ---------- REGISTRATIONS ----------
def get_registrations():
    if os.path.exists(REGISTRATIONS_FILE):
        with open(REGISTRATIONS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_registration(registration_data):
    registrations = get_registrations()
    registration_data['id'] = len(registrations) + 1
    registration_data['date_registered'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    registrations.append(registration_data)
    with open(REGISTRATIONS_FILE, 'w') as f:
        json.dump(registrations, f, indent=2)
    return True

print("✅ admin.py updated with all required functions")
