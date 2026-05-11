# Word Temple Church of God International Website
# Copyright (c) 2026 Word Temple Church of God International
# All rights reserved. Unauthorized copying of this file, via any medium, is strictly prohibited.
from flask import Flask, render_template, session, redirect, url_for, request, flash
from functools import wraps
import os
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

# Church information - COMPLETE
church_info = {
    'name': 'Word Temple Church of God International',
    'short_name': 'Word Temple Church',
    'headquarters': 'Eastleigh, Nairobi',
    'address': 'PRJX+JF2, Nairobi, Kenya',
    'address_full': 'PRJX+JF2, Nairobi, Kenya - Eastleigh, 1st Avenue, 3rd Street, Next to St. Teresa\'s Dispensary',
    'phone': '+254 719 306011',
    'phone_alt': '+254 720 313 832',
    'email': 'wordtemple@hotmail.com',
    
    # APOSTLE MICHAEL WAMBUA
    'apostle': {
        'name': 'Apostle Michael Wambua',
        'title': 'Apostle Over The Commission',
        'role': 'Founder & Presiding Bishop',
        'bio': 'Apostle Michael Wambua is the Founder and Presiding Bishop of Word Temple Church of God International, a dynamic and rapidly growing ministry based in Eastleigh, Nairobi, with over 30 branches and affiliates nationwide. The ministry is committed to transforming lives through the teaching and preaching of the revealed Word of God.',
        'conference': 'He is the convener of the annual Revelation and Power Conference, a transformative gathering that ignites spiritual growth and revival, as well as the Pastors and Leaders Meeting, where he equips and imparts wisdom to church leaders for effective ministry.',
        'international': 'An international teacher and preacher of the Word, Apostle Wambua has ministered in over 23 countries, impacting lives across nations with profound revelation, clarity, and spiritual authority.',
        'education': 'Apostle Michael Wambua holds a Diploma in Transformational Church Leadership from Pan African University and is currently pursuing a Bachelor\'s degree in Biblical Studies from KAG East University.',
        'author': 'He is also a dedicated writer, authoring books that equip, inspire, and strengthen individuals in their spiritual journey.',
        'family': 'Beyond ministry, he is a devoted husband and a loving father of two, and a spiritual father to many sons and daughters in the faith.',
        'founded': '18th January 2004',
        'commission_date': '18th May 1999',
        'commission_word': '"I am sending you for a Worldwide Mission"',
        'mission': 'Defending and confirming the gospel'
    },
    
    # REVEREND BANCY WAMBUA
    'rev_bancy': {
        'name': 'Reverend Bancy Wambua',
        'title': 'Co-Founder, Worship Leader, Women\'s Ministry Director',
        'bio': 'Reverend Bancy is a devoted servant of God, a passionate worshiper, and a committed preacher of the Gospel. As a mother of two, she beautifully balances family life with her calling in ministry.',
        'conference': 'She is the leader of the annual Daughters of the Kingdom Women Conference, where she inspires and equips women to rise into their God-given calling.',
        'youth': 'Reverend Bancy also serves as a youth patron, mentoring and guiding the younger generation in their spiritual journey.',
        'co_founder': 'She is the co-founder of Word Temple Church of God International, where she continues to impact lives through worship, teaching, and leadership.',
        'mission': 'Her life reflects a heart fully surrendered to God, dedicated to spreading His Word and transforming lives through worship and teaching.'
    },
    
    # Church History
    'vision': 'Restoration of the Full Gospel unto the body of Christ and planting churches all over the World',
    'mission': 'To teach and preach the whole council of God\'s word, the Gospel of Jesus Christ worldwide through indoor meetings and outdoor meetings.',
    'core_values': ['Integrity', 'Credibility', 'Holiness', 'Humility', 'Determination', 'Seizing opportunities', 'Exemplary living', 'Team player'],
    
    # 2026 Theme
    'theme_2026': 'Our Year of SUPERNATURAL BREAKTHROUGHS',
    'theme_scripture': '2 Samuel 5:20 (NKJV)',
    'theme_verse': '"like a breakthrough of water? Therefore he called the name of that place Baal Perazim."',
    
    # SUNDAY SERVICES
    'services': [
        {'name': '1st Service', 'time': '5:30 AM - 8:00 AM', 'day': 'Sunday', 'type': 'Morning Glory'},
        {'name': '2nd Service', 'time': '8:30 AM - 11:00 AM', 'day': 'Sunday', 'type': 'Family Service'},
        {'name': '3rd Service', 'time': '11:00 AM - 2:00 PM', 'day': 'Sunday', 'type': 'Prophetic Blessing'}
    ],
    
    # WEEKLY PROGRAMS
    'weekly_programs': [
        {'day': 'Monday - Friday', 'name': 'Morning Meditation', 'time': '6:30 AM - 7:30 AM', 'location': 'Church Auditorium & Online', 'icon': 'fa-sun', 'description': 'Start your day with God\'s Word'},
        {'day': 'Monday - Friday', 'name': 'Lunch Hour Services', 'time': '12:30 PM - 2:00 PM', 'location': 'Church Auditorium & Online', 'icon': 'fa-utensils', 'description': 'Daily spiritual nourishment'},
        {'day': 'Tuesday', 'name': 'Pastors & Leaders Meeting', 'time': '9:00 AM - 11:30 AM', 'location': 'Church Auditorium', 'icon': 'fa-chalkboard-user', 'description': 'Leadership training with Apostle Michael Wambua'},
        {'day': 'Wednesday', 'name': 'Gospel Master Class', 'time': '6:30 PM - 8:00 PM', 'location': 'Church Auditorium & Online', 'icon': 'fa-fire', 'description': 'Deep teaching and anointing'},
        {'day': 'First Friday', 'name': 'Mini-Kesha Prayer Service', 'time': '6:30 PM - 9:30 PM', 'location': 'Church Auditorium', 'icon': 'fa-pray', 'description': 'Powerful prayer service with Apostle Michael Wambua'},
        {'day': 'Saturday', 'name': 'Youth Service - "The Remnant"', 'time': '10:00 AM - 12:00 PM', 'location': 'Church Auditorium', 'icon': 'fa-child', 'description': 'Young adults and teens'}
    ],
    
    # First Sunday Special
    'first_sunday': 'Prophetic Family Blessing Sunday',
    
    # APOSTLE QUOTES
    'apostle_quotes': [
        'NO MATTER HOW LOW YOU GO YOU CAN NEVER GO BEYOND GOD\'S MERCY',
        'YOU LOOSE WHAT GOD GAVE YOU WHEN YOU FORSAKE HIM',
        'You can only experience Jesus the Alpha in the spirit.',
        'Hearing from God connects you to the very Being/nature of God.',
        'WHATEVER COMES BY FAVOR WILL RULE.',
        'Favor is Sustained by Staying in the Teachings of God.',
        'The Anger and Envy of Men will Never overcome the Favor of God upon your life.',
        'Change is First done in the Invisible before it can be Manifested in the Physical.',
        'FAVOR WILL ALWAYS OUTWEIGH THE HATRED OF MEN.',
        'FAVOUR AFFECTS THE INVISIBLE WORLD AROUND YOU.',
        'GOD NEVER FORSAKES THE ANOINTED ONES.',
        'The target of Faith is your Heart.',
        'Divine encounters will leave a mark that will dissolve all kinds of Doubt and Fear.',
        'Everywhere God is and believed, Signs and wonders will always be present.',
        'GOD CAN USE ANYTHING TO BRING EVERYTHING IN YOUR LIFE.',
        'No matter how long the Devil prepares, God will always win.',
        'NO MATTER THE LEVEL OF ANOINTING, TEMPTATIONS WILL ALWAYS COME',
        'Worship is The highest degree of Spirituality.',
        'The majestic Presence of God is His Voice.',
        'Every genuine worshipper of God has Dominion.'
        'There is a time when God opens your eyes for you to see the value of a pastor in your life.',
        'Battles never end completely; you are always at war. It is important to know that you were anointed for that.',
        'When you discover the value of the man of God, help starts to come your way.',
        'Partnership is beyond natural transaction of things; it is impartation of power, wisdom and the anointing of God.'
    ],

    
    # REV BANCY QUOTES
    'rev_quotes': [
        'WHEN THE LORD EMPOWERS YOU, VICTORY IS ASSURED'
    ],
    
    # GIVING OPTIONS
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
        'kcb_paybill':'52252',
        'kcb_account':'7544081',
        'kcb_cheque':'1325540706'
    },
    
    # YOUTUBE PLAYLISTS & VIDEOS
    'youtube': 'https://www.youtube.com/channel/UChcwF0pY1uwpVRWLUVCbfDw',
    'youtube_channel': '@WordTempleChurchofGod',
    'youtube_subs': '4.49K',
    'youtube_videos': '4,035',
    
    # SOCIAL MEDIA
    'facebook': 'https://web.facebook.com/WTCOFGOD',
    'twitter': 'https://x.com/WordTempleofGod',
    'instagram': 'https://www.instagram.com/wordtemplechurchofgod/'
}

# ========== ROUTES ==========

@app.route('/')
def home():
    return render_template('index.html', church=church_info)

@app.route('/about')
def about():
    return render_template('about.html', church=church_info)

@app.route('/leaders')
def leaders():
    return render_template('leaders.html', church=church_info)

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

@app.route('/events')
def events():
    return render_template('events.html', church=church_info)

@app.route('/resources')
def resources():
    return render_template('resources.html', church=church_info)

# ========== REGISTER ROUTE (ONLY ONE) ==========

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        registration_data = {
            'Full Name': request.form.get('Full Name'),
            'Email': request.form.get('Email'),
            'Phone Number': request.form.get('Phone Number'),
            'Church/Organization': request.form.get('Church/Organization'),
            'Conference': request.form.get('Conference'),
            'Accommodation Needed': request.form.get('Accommodation Needed'),
            'Room Type': request.form.get('Room Type'),
            'Check-in Date': request.form.get('Check-in Date'),
            'Check-out Date': request.form.get('Check-out Date'),
            'Number of Nights': request.form.get('Number of Nights'),
            'Meal Preference': request.form.get('Meal Preference'),
            'Special Requests': request.form.get('Special Requests')
        }
        save_registration(registration_data)
        flash('Registration successful! You will receive a confirmation email.', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', church=church_info)

# ========== ADMIN ROUTES ==========

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

@app.route('/admin/events', methods=['GET', 'POST'])
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
            from werkzeug.utils import secure_filename
            import time
            
            # Get file extension
            original_filename = secure_filename(file.filename)
            name, ext = os.path.splitext(original_filename)
            
            # Add timestamp to filename to make it unique and show newest first
            timestamp = int(time.time())
            new_filename = f"{timestamp}_{original_filename}"
            
            # Save file
            save_path = os.path.join('static/images/gallery/', new_filename)
            file.save(save_path)
            
            flash(f'Photo {original_filename} uploaded successfully!', 'success')
            return redirect(url_for('admin_upload_photo'))
    
    # Get photos sorted by modification time (newest first)
    photos = []
    gallery_path = 'static/images/gallery/'
    if os.path.exists(gallery_path):
        files = os.listdir(gallery_path)
        # Filter only image files
        image_extensions = ('.jpg', '.jpeg', '.JPG', '.png', '.gif', '.jpeg', '.JPEG')
        image_files = []
        for f in files:
            if f.lower().endswith(image_extensions):
                image_files.append(f)
        # Sort by modification time (newest first)
        image_files.sort(key=lambda x: os.path.getmtime(os.path.join(gallery_path, x)), reverse=True)
        photos = image_files
    
    return render_template('admin_upload.html', photos=photos)

@app.route('/get-gallery-images')
def get_gallery_images():
    """Return list of all images in the gallery folder"""
    import os
    gallery_path = 'static/images/gallery/'
    images = []
    if os.path.exists(gallery_path):
        for f in os.listdir(gallery_path):
            if f.lower().endswith(('.jpg', '.jpeg', '.JPG', '.png', '.gif')):
                images.append(f)
        # Sort by modification time (newest first)
        images.sort(key=lambda x: os.path.getmtime(os.path.join(gallery_path, x)), reverse=True)
    return {'images': images}

@app.route('/admin/delete-photo/<filename>')
@login_required
def delete_photo(filename):
    """Delete a photo from the gallery"""
    import os
    file_path = os.path.join('static/images/gallery/', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'Photo {filename} deleted successfully!', 'success')
    else:
        flash(f'Photo {filename} not found!', 'error')
    return redirect(url_for('admin_upload_photo'))

@app.route('/membership')
def membership():
    return render_template('membership.html', church=church_info)


@app.route('/conference-register')
def conference_register():
    return render_template('conference-register.html', church=church_info)

if __name__ == '__main__':
    app.run(debug=True)
