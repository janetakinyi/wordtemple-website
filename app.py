# Word Temple Church of God International Website
# Copyright (c) 2026 Word Temple Church of God International
# All rights reserved.

from flask import Flask, abort, render_template, session, redirect, url_for, request, flash, send_from_directory
from functools import wraps
import os
from dotenv import load_dotenv
load_dotenv()
import json
import time
from datetime import datetime
from pathlib import Path
import re
import secrets
from uuid import uuid4
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename
from admin import delete_event, verify_admin, save_registration, get_registrations, get_quotes, get_events, get_settings, save_settings, update_quotes, save_events

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError('SECRET_KEY is required. Add it as a Render environment variable.')
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=os.environ.get('SESSION_COOKIE_SECURE', 'true').lower() == 'true',
    SESSION_COOKIE_SAMESITE='Lax',
    MAX_CONTENT_LENGTH=5 * 1024 * 1024,
)

UPLOAD_ROOT = Path(os.environ.get('UPLOAD_DIR', Path(app.root_path) / 'static' / 'images')).resolve()
LEGACY_IMAGE_ROOT = (Path(app.static_folder) / 'images').resolve()
ALLOWED_IMAGE_FORMATS = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp', 'GIF': '.gif'}

def csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_urlsafe(32)
    return session['csrf_token']

@app.context_processor
def inject_security_helpers():
    return {'csrf_token': csrf_token}

@app.before_request
def protect_admin_forms():
    if request.path.startswith('/admin/') and request.method in {'POST', 'PUT', 'PATCH', 'DELETE'}:
        expected_token = session.get('csrf_token')
        submitted_token = request.form.get('csrf_token')
        if not expected_token or not submitted_token or not secrets.compare_digest(expected_token, submitted_token):
            abort(400, 'Invalid or missing CSRF token.')

@app.errorhandler(413)
def upload_too_large(error):
    flash('Image files must be 5 MB or smaller.', 'error')
    return redirect(request.referrer or url_for('admin_dashboard'))

def upload_directory(category):
    if category not in {'gallery', 'events'}:
        abort(404)
    directory = UPLOAD_ROOT / category
    directory.mkdir(parents=True, exist_ok=True)
    return directory

def save_image(file, category, label=None):
    """Verify image content and save it with a server-generated, collision-proof name."""
    try:
        image = Image.open(file.stream)
        image.verify()
        extension = ALLOWED_IMAGE_FORMATS[image.format]
    except (UnidentifiedImageError, KeyError, OSError):
        raise ValueError('Please upload a valid JPEG, PNG, WEBP, or GIF image.')
    finally:
        file.stream.seek(0)

    filename = f'{secure_filename(label)}_{uuid4().hex}{extension}' if label else f'{uuid4().hex}{extension}'
    file.save(upload_directory(category) / filename)
    return filename

def gallery_images(include_legacy=True):
    """Return persistent uploads and, during migration, images bundled with the app."""
    sources = [(upload_directory('gallery'), lambda name: url_for('uploaded_file', category='gallery', filename=name))]
    legacy_gallery = LEGACY_IMAGE_ROOT / 'gallery'
    if include_legacy and legacy_gallery != upload_directory('gallery') and legacy_gallery.exists():
        sources.append((legacy_gallery, lambda name: url_for('static', filename=f'images/gallery/{name}')))

    images = []
    for directory, make_url in sources:
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
                images.append({'name': file_path.name, 'url': make_url(file_path.name), 'time': file_path.stat().st_mtime})
    return sorted(images, key=lambda image: image['time'], reverse=True)

@app.route('/uploads/<category>/<filename>')
def uploaded_file(category, filename):
    if category not in {'gallery', 'events'}:
        abort(404)
    return send_from_directory(upload_directory(category), filename)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please login first', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def is_event_past(event_date_str):
    """
    Check if an event date is in the past.
    """
    if not event_date_str:
        return False
    
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day
    
    # Try to extract year from the date string
    year_match = re.search(r'(\d{4})', event_date_str)
    if year_match:
        event_year = int(year_match.group(1))
        if event_year < current_year:
            return True
        elif event_year > current_year:
            return False
    
    # Check for specific month names
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    for month in months:
        if month in event_date_str:
            month_index = months.index(month) + 1
            if month_index < current_month and year_match and int(year_match.group(1)) <= current_year:
                return True
            break
    
    return False

# Church information
church_info = {
    'name': 'Word Temple Church of God International',
    'short_name': 'Word Temple Church',
    'headquarters': 'Eastleigh, Nairobi',
    'address': 'PRJX+JF2, Nairobi, Kenya',
    'address_full': 'PRJX+JF2, Nairobi, Kenya - Eastleigh, 1st Avenue, 3rd Street, Next to St. Teresa\'s Dispensary',
    'phone': '+254 719 306011',
    'phone_alt': '+254 720 313 832',
    'email': 'wordtemple@hotmail.com',
    'apostle': {
        'name': 'Apostle Michael Wambua',
        'title': 'Apostle Over The Commission',
        'role': 'Founder & Presiding Bishop',
        'bio': 'Apostle Michael Wambua is the Founder and Presiding Bishop of Word Temple Church of God International.',
        'conference': 'He is the convener of the annual Revelation and Power Conference.',
        'international': 'He has ministered in over 23 countries.',
        'education': 'Holds a Diploma in Transformational Church Leadership.',
        'author': 'Author of several books.',
        'family': 'Devoted husband and father of two.',
        'founded': '18th January 2004',
        'commission_date': '18th May 1999',
        'commission_word': '"I am sending you for a Worldwide Mission"',
        'mission': 'From Vision to Revelation: The Gospel on Television'
    },
    'rev_bancy': {
        'name': 'Reverend Bancy Wambua',
        'title': 'Co-Founder, Worship Leader, Women\'s Ministry Director',
        'bio': 'Reverend Bancy is a devoted servant of God and passionate worshiper.',
        'conference': 'Leader of the annual Daughters of the Kingdom Women Conference.',
        'youth': 'Serves as a youth patron.',
        'co_founder': 'Co-founder of Word Temple Church of God International.',
        'mission': 'Spreading His Word and transforming lives through worship.'
    },
    'vision': 'Restoration of the Full Gospel and planting churches worldwide',
    'mission': 'To teach and preach the whole council of God\'s word worldwide',
    'core_values': ['Integrity', 'Credibility', 'Holiness', 'Humility', 'Determination', 'Seizing opportunities', 'Exemplary living', 'Team player'],
    'theme_2026': 'Our Year of SUPERNATURAL BREAKTHROUGHS',
    'theme_scripture': '2 Samuel 5:20 (NKJV)',
    'theme_verse': 'So David came to Baal Perazim, and David defeated them there; and he said, "The LORD has broken through my enemies before me, like a breakthrough of water." Therefore he called the name of that place Baal Perazim.',
    # Theme of the Month
    'theme_month': 'JULY 2026 | HAVE DOMINION',
    'theme_month_scripture': 'Genesis 1:26',
    'theme_month_verse': '"Let Us make man in Our image, according to Our likeness; let them have dominion......"',
    'services': [
        {'name': '1st Service', 'time': '5:30 AM - 8:00 AM', 'day': 'Sunday', 'type': 'Morning Glory'},
        {'name': '2nd Service', 'time': '8:30 AM - 11:00 AM', 'day': 'Sunday', 'type': 'Family Service'},
        {'name': '3rd Service', 'time': '11:00 AM - 2:00 PM', 'day': 'Sunday', 'type': 'Prophetic Blessing'}
    ],
    'weekly_programs': [
        {'day': 'Monday - Friday', 'name': 'Morning Breakthrough', 'time': '6:30 AM - 7:30 AM', 'location': 'Church Auditorium & Online', 'icon': 'fa-sun', 'description': 'Start your day with God\'s Word'}
    ],
    'first_sunday': 'Prophetic Family Blessing Sunday',
    'giving': {
        'mpesa_till': '841690',
        'mpesa_account': 'WORD TEMPLE CHURCH OF GOD',
        'equity_paybill': '247247',
        'equity_account': '841690',
        'partnership_paybill': '247247',
        'partnership_account': '841690',
        'development_account': 'WORD TEMPLE CHURCH',
        'sendwave': '+254 720 313 832',
        'sendwave_name': 'Michael Ndiku',
        'paypal': 'wordtemple@hotmail.com',
        'kcb_paybill': '52252',
        'kcb_account': '7544081',
        'kcb_cheque': '1325540706'
    },
    'youtube': 'https://www.youtube.com/channel/UChcwF0pY1uwpVRWLUVCbfDw',
    'youtube_channel': '@WordTempleChurchofGod',
    'youtube_subs': '4.49K',
    'facebook': 'https://web.facebook.com/WTCOFGOD',
    'twitter': 'https://x.com/WordTempleofGod',
    'instagram': 'https://www.instagram.com/wordtemplechurchofgod/'
}

# Gallery API
@app.route('/get-gallery-images')
def get_gallery_images():
    return {'images': gallery_images()}

# Page routes
@app.route('/')

def home():
    settings = get_settings()
    return render_template('index.html', church=church_info, settings=settings)

@app.route('/about')

def about():
    return render_template('about.html', church=church_info)

@app.route('/founders')

def founders():
    return render_template('founders.html', church=church_info)

@app.route('/leaders')

def leaders():
    return redirect('/founders')


@app.route('/events')
def events():
    # Load all events from data file
    events_data = load_events_data()
    
    # Filter out past events
    upcoming_events = []
    for event in events_data:
        event_date = event.get('dates', '')
        if '2025' not in event_date and '2024' not in event_date:
            upcoming_events.append(event)
    
    return render_template('events.html', events=upcoming_events, church=church_info)

@app.route('/connect')

def connect():
    return render_template('connect.html', church=church_info)

@app.route('/ministries')

def ministries():
    return render_template('ministries.html', church=church_info)

@app.route('/gallery')

def gallery():
    return render_template('gallery.html', church=church_info)

@app.route('/quotes')

def quotes():
    quotes_data = get_quotes()
    return render_template('quotes.html', quotes=quotes_data, church=church_info)

@app.route('/give')

def give():
    return render_template('give.html', church=church_info)

@app.route('/resources')

def resources():
    return render_template('resources.html', church=church_info)

@app.route('/membership')

def membership():
    return render_template('membership.html', church=church_info)

@app.route('/conference-register', methods=['GET', 'POST'])

def conference_register():
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('Full Name', '')
        email = request.form.get('Email', '')
        phone = request.form.get('Phone Number', '')
        conference = request.form.get('Conference', '')
        
        # Save to JSON (for admin dashboard)
        registration_data = {
            'Full Name': full_name,
            'Email': email,
            'Phone Number': phone,
            'Conference': conference,
            'Church/Organization': request.form.get('Church/Organization', ''),
            'Accommodation Needed': request.form.get('Accommodation Needed', 'No'),
            'Room Type': request.form.get('Room Type', ''),
            'Check-in Date': request.form.get('Check-in Date', ''),
            'Check-out Date': request.form.get('Check-out Date', ''),
            'Number of Nights': request.form.get('Number of Nights', ''),
            'Meal Preference': request.form.get('Meal Preference', ''),
            'Special Requests': request.form.get('Special Requests', ''),
            'date_registered': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 1. Save to JSON (admin dashboard)
        save_registration(registration_data)
        
        # 2. Send email via FormSubmit
        import requests
        try:
            form_data = request.form.to_dict()
            form_data['_captcha'] = 'false'
            form_data['_template'] = 'table'
            form_data['_subject'] = '🎟️ NEW CONFERENCE REGISTRATION - Word Temple Church'
            form_data['_autoresponse'] = 'Thank you for registering for our conference! We have received your information and will contact you within 24 hours. God bless you! - Word Temple Church Team'
            
            response = requests.post('https://formsubmit.co/wordtemple@hotmail.com', data=form_data)
            if response.status_code == 200:
                print("✅ Email sent successfully")
            else:
                print(f"⚠️ Email sending failed: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Email error: {e}")
        
        flash('✅ Registration Successful! Thank you for registering. You will receive a confirmation email shortly.', 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html', church=church_info)

def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if verify_admin(username, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('admin_login.html', church=church_info)

@app.route('/admin/logout')

def admin_logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    registrations = get_registrations()
    settings = get_settings()
    quotes = get_quotes()
    gallery_count = 0
    gallery_count = len(gallery_images())
    events = get_events()
    return render_template('admin_dashboard.html', 
                         registrations=registrations, 
                         settings=settings, 
                         quotes=quotes,
                         gallery_count=gallery_count,
                         events_count=len(events),
                         registrations_count=len(registrations),
                         quotes_count=len(quotes),
                         church=church_info)

@app.route('/admin/registrations')
@login_required
def admin_registrations():
    registrations = get_registrations()
    return render_template('admin_registrations.html', registrations=registrations, church=church_info)

@app.route('/admin/quotes', methods=['GET', 'POST'])
@login_required
def admin_quotes():
    quotes = get_quotes()
    if request.method == 'POST':
        new_quote = request.form.get('quote')
        author = request.form.get('author')
        if new_quote and author:
            quotes.append({'text': new_quote, 'source': author})
            update_quotes(quotes)
            flash('Quote added successfully!', 'success')
            return redirect(url_for('admin_quotes'))
    return render_template('admin_quotes.html', quotes=quotes, church=church_info)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    settings = get_settings()
    if request.method == 'POST':
        # Yearly Theme
        settings['theme_2026'] = request.form.get('theme_2026')
        settings['theme_scripture'] = request.form.get('theme_scripture')
        settings['theme_verse'] = request.form.get('theme_verse')
        
        # Monthly Theme
        settings['theme_month'] = request.form.get('theme_month')
        settings['theme_month_scripture'] = request.form.get('theme_month_scripture')
        settings['theme_month_verse'] = request.form.get('theme_month_verse')
        
        announcements = request.form.getlist('announcements')
        settings['announcements'] = [a for a in announcements if a.strip()]
        for i in range(3):
            settings['services']['sunday'][i]['time'] = request.form.get(f'sunday_time_{i}')
        for i in range(6):
            settings['services']['weekly'][i]['time'] = request.form.get(f'weekly_time_{i}')
        save_settings(settings)
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('admin_settings'))
    return render_template('admin_settings.html', settings=settings, church=church_info)

@app.route('/admin/upload-photo', methods=['GET', 'POST'])
@login_required
def admin_upload_photo():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('admin_upload_photo'))
        file = request.files['photo']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('admin_upload_photo'))
        if file:
            try:
                gallery_category = request.form.get('gallery_category', '')
                if gallery_category not in {'worship', 'rp', 'preaching', 'youth', 'wconf', 'praise'}:
                    raise ValueError('Please select a gallery category.')
                filename = save_image(file, 'gallery', gallery_category)
            except ValueError as error:
                flash(str(error), 'error')
                return redirect(url_for('admin_upload_photo'))
            flash(f'Photo {filename} uploaded successfully!', 'success')
            return redirect(url_for('admin_upload_photo'))
    photos = []
    photos = gallery_images(include_legacy=False)
    return render_template('admin_upload.html', photos=photos, church=church_info)

@app.route('/admin/delete-photo/<filename>', methods=['POST'])
@login_required
def delete_photo(filename):
    filename = secure_filename(filename)
    file_path = upload_directory('gallery') / filename
    if file_path.is_file():
        file_path.unlink()
        flash(f'Photo {filename} deleted successfully!', 'success')
    else:
        flash(f'Photo {filename} not found!', 'error')
    return redirect(url_for('admin_upload_photo'))

@app.route('/register', methods=['GET', 'POST'])

def register():
    if request.method == 'POST':
        registration_data = {
            'Full Name': request.form.get('Full Name'),
            'Email': request.form.get('Email'),
            'Phone Number': request.form.get('Phone Number'),
            'Conference': request.form.get('Conference'),
        }
        save_registration(registration_data)
        flash('Registration successful!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', church=church_info)

def load_events_data():
    return get_events()

def save_events_data(events):
    save_events(events)


@app.route('/admin/events')
@login_required
def admin_events():
    events = load_events_data()
    return render_template('admin_events_management.html', events=events, church=church_info)

@app.route('/admin/add-event', methods=['POST'])
@login_required
def admin_add_event():
    if 'event_image' not in request.files:
        flash('No image file selected', 'error')
        return redirect(url_for('admin_events'))
    
    file = request.files['event_image']
    if file.filename == '':
        flash('No image selected', 'error')
        return redirect(url_for('admin_events'))
    
    if file:
        try:
            filename = save_image(file, 'events')
        except ValueError as error:
            flash(str(error), 'error')
            return redirect(url_for('admin_events'))
        
        category = request.form.get('category', '')
        title = request.form.get('title', '')
        scripture = request.form.get('scripture', '')
        verse_text = request.form.get('verse_text', '')
        dates = request.form.get('dates', '')
        host = request.form.get('host', '')
        guest_speakers = request.form.getlist('guest_speaker[]')
        location = request.form.get('location', 'Eastleigh, 1st Avenue, 3rd Street, Nairobi')
        
        event = {
            'id': f'event-{int(datetime.now().timestamp())}',
            'title': title,
            'category': category,
            'dates': dates,
            'image': filename,
            'image_url': url_for('uploaded_file', category='events', filename=filename),
            'filename': filename,
            'scripture': scripture,
            'verse_text': verse_text,
            'host': host,
            'guest_speakers': [g for g in guest_speakers if g.strip()],
            'venue': location
        }
        
        events = load_events_data()
        events.append(event)
        save_events_data(events)
        
        flash('Event published successfully!', 'success')
        return redirect(url_for('admin_events'))
    events = load_events_data()
    return render_template('admin_events_management.html', events=events, church=church_info)

@app.route('/admin/delete-event/<event_id>', methods=['POST'])
@login_required
def admin_delete_event(event_id):
    delete_event(event_id)
    flash('Event deleted successfully.', 'success')
    return redirect(url_for('admin_events'))

@app.route('/admin/edit-event/<event_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_event(event_id):
    # CSRF validation - temporarily disabled
    # expected_token = session.get('csrf_token')
    # submitted_token = request.form.get('csrf_token')
    # if not expected_token or submitted_token != expected_token:
    #     flash('Invalid CSRF token', 'error')
    #     return redirect(url_for('admin_events'))

    events = load_events_data()
    event = None
    for e in events:
        if str(e.get('id')) == str(event_id):
            event = e
            break
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('admin_events'))
    if request.method == 'POST':
        event['title'] = request.form.get('title', event['title'])
        event['category'] = request.form.get('category', event['category'])
        event['dates'] = request.form.get('dates', event['dates'])
        event['theme'] = request.form.get('theme', event.get('theme', ''))
        event['scripture'] = request.form.get('scripture', event.get('scripture', ''))
        event['hosts'] = request.form.get('hosts', event.get('hosts', ''))
        event['venue'] = request.form.get('venue', event.get('venue', ''))
        event['entry'] = request.form.get('entry', event.get('entry', 'FREE ENTRY'))
        event['time'] = request.form.get('time', event.get('time', ''))
        if 'event_image' in request.files:
            file = request.files['event_image']
            if file and file.filename != '':
                from werkzeug.utils import secure_filename
                import os
                filename = secure_filename(file.filename)
                file_path = os.path.join('static/images/events', filename)
                file.save(file_path)
                event['image'] = filename
        save_events_data(events)
        flash('Event updated successfully!', 'success')
        return redirect(url_for('admin_events'))
    return render_template('admin_edit_event.html', event=event, church=church_info)

if __name__ == '__main__':
    app.run(debug=True)
