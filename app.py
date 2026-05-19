# Word Temple Church of God International Website
# Copyright (c) 2026 Word Temple Church of God International
# All rights reserved.

from flask import Flask, render_template, session, redirect, url_for, request, flash, send_from_directory
from functools import wraps
import os
import json
from werkzeug.utils import secure_filename
from admin import verify_admin, save_registration, get_registrations, get_quotes, get_events, get_settings, save_settings, update_quotes

app = Flask(__name__)
app.secret_key = 'wordtemple-church-secret-key-2026'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please login first', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

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
        'name': 'Apostle Michael Wambua Wambua',
        'title': 'Apostle Over The Commission',
        'role': 'Founder & Presiding Bishop',
        'bio': 'Apostle Michael Wambua Wambua is the Founder and Presiding Bishop of Word Temple Church of God International.',
        'conference': 'He is the convener of the annual Revelation and Power Conference.',
        'international': 'He has ministered in over 23 countries.',
        'education': 'Holds a Diploma in Transformational Church Leadership.',
        'author': 'Author of several books.',
        'family': 'Devoted husband and father of two.',
        'founded': '18th January 2004',
        'commission_date': '18th May 1999',
        'commission_word': '"I am sending you for a Worldwide Mission"',
        'mission': 'Defending and confirming the gospel'
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
    'theme_verse': '"like a breakthrough of water?"',
    
    'services': [
        {'name': '1st Service', 'time': '5:30 AM - 8:00 AM', 'day': 'Sunday', 'type': 'Morning Glory'},
        {'name': '2nd Service', 'time': '8:30 AM - 11:00 AM', 'day': 'Sunday', 'type': 'Family Service'},
        {'name': '3rd Service', 'time': '11:00 AM - 2:00 PM', 'day': 'Sunday', 'type': 'Prophetic Blessing'}
    ],
    
    'weekly_programs': [
        {'day': 'Monday - Friday', 'name': 'Morning Breakthrough', 'time': '6:30 AM - 7:30 AM', 'location': 'Church Auditorium & Online', 'icon': 'fa-sun', 'description': 'Start your day with God\'s Word'},
        {'day': 'Monday - Friday', 'name': 'Lunch Hour Services', 'time': '12:30 PM - 2:00 PM', 'location': 'Church Auditorium & Online', 'icon': 'fa-utensils', 'description': 'Daily spiritual nourishment'},
        {'day': 'Tuesday', 'name': 'Pastors & Leaders Meeting', 'time': '9:00 AM - 11:30 AM', 'location': 'Church Auditorium', 'icon': 'fa-chalkboard-user', 'description': 'Leadership training'},
        {'day': 'Wednesday', 'name': 'Gospel Master Class', 'time': '6:30 PM - 8:00 PM', 'location': 'Church Auditorium & Online', 'icon': 'fa-fire', 'description': 'Deep teaching and anointing'},
        {'day': 'First Friday', 'name': 'Mini-Kesha Prayer Service', 'time': '6:30 PM - 9:30 PM', 'location': 'Church Auditorium', 'icon': 'fa-pray', 'description': 'Powerful prayer service'},
        {'day': 'Saturday', 'name': 'Youth Service', 'time': '10:00 AM - 12:00 PM', 'location': 'Church Auditorium', 'icon': 'fa-child', 'description': 'Young adults and teens'}
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

# Serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Gallery API
@app.route('/get-gallery-images')
def get_gallery_images():
    gallery_path = 'static/images/gallery/'
    images = []
    if os.path.exists(gallery_path):
        for f in os.listdir(gallery_path):
            if f.lower().endswith(('.jpg', '.jpeg', '.JPG', '.png', '.gif')):
                images.append(f)
        images.sort()
    return {'images': images}

# Page routes
@app.route('/')
def home():
    return render_template('index.html', church=church_info)

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
    return render_template('events.html', church=church_info)

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
    return render_template('quotes.html', church=church_info)

@app.route('/give')
def give():
    return render_template('give.html', church=church_info)

@app.route('/resources')
def resources():
    return render_template('resources.html', church=church_info)

@app.route('/membership')
def membership():
    return render_template('membership.html', church=church_info)

@app.route('/conference-register')
def conference_register():
    return render_template('conference-register.html', church=church_info)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
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
    return render_template('admin_login.html')

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
    return render_template('admin_dashboard.html', registrations=registrations, settings=settings, quotes=quotes, church=church_info)

@app.route('/admin/registrations')
@login_required
def admin_registrations():
    registrations = get_registrations()
    return render_template('admin_registrations.html', registrations=registrations)

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
    return render_template('admin_quotes.html', quotes=quotes)

@app.route('/admin/events')
@login_required
def admin_events():
    events = get_events()
    return render_template('admin_events.html', events=events)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    settings = get_settings()
    if request.method == 'POST':
        settings['theme_2026'] = request.form.get('theme_2026')
        settings['theme_scripture'] = request.form.get('theme_scripture')
        settings['theme_verse'] = request.form.get('theme_verse')
        announcements = request.form.getlist('announcements')
        settings['announcements'] = [a for a in announcements if a.strip()]
        for i in range(3):
            settings['services']['sunday'][i]['time'] = request.form.get(f'sunday_time_{i}')
        for i in range(6):
            settings['services']['weekly'][i]['time'] = request.form.get(f'weekly_time_{i}')
        save_settings(settings)
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('admin_settings'))
    return render_template('admin_settings.html', settings=settings)

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
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/images/gallery/', filename))
            flash(f'Photo {filename} uploaded successfully!', 'success')
            return redirect(url_for('admin_upload_photo'))
    photos = []
    if os.path.exists('static/images/gallery/'):
        photos = os.listdir('static/images/gallery/')
    return render_template('admin_upload.html', photos=photos)

@app.route('/admin/delete-photo/<filename>')
@login_required
def delete_photo(filename):
    file_path = os.path.join('static/images/gallery/', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
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

if __name__ == '__main__':
    app.run(debug=True)
