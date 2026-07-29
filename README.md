# Word Temple Church of God International Website

![Word Temple Church](https://img.shields.io/badge/Word-Temple%20Church-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.3-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📖 About The Project

This is the official website for **Word Temple Church of God International**, a dynamic and growing ministry based in Eastleigh, Nairobi, Kenya.

## 🚀 Live Demo

[View Website](https://wordtemple-website.onrender.com)

## Production environment

The application stores admin data, registrations, settings, quotes, and events in PostgreSQL. Set these variables in the Render service before deploying:

- `DATABASE_URL`: the Neon pooled PostgreSQL connection string, including `sslmode=require`
- `SECRET_KEY`: a long random value for Flask sessions
- `INITIAL_ADMIN_USERNAME` and `INITIAL_ADMIN_PASSWORD`: used only to create the first admin account when the database is empty

Do not commit any of these values. After the first successful deployment, the initial-admin variables can be removed if desired.

For local HTTP development only, set `SESSION_COOKIE_SECURE=false` in `.env`. Keep the production default of `true`.

### Persistent uploads on Render

Gallery and event images are not stored in PostgreSQL. To retain them after deploys and restarts, attach a Render persistent disk to the web service at `/var/data`, then set `UPLOAD_DIR=/var/data/uploads` in the service environment. Without a persistent disk, uploads remain temporary.


## ✨ Key Features

- 🎥 **Live Streaming** - Watch services live on YouTube
- 📝 **Conference Registration** - Register with accommodation booking
- 💰 **Online Giving** - M-PESA, Bank, PayPal, Sendwave
- 🖼️ **Photo Gallery** - 180+ photos from events
- 📖 **Apostolic Quotes** - Daily inspiration
- 👥 **Admin Panel** - Easy content management

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Animations**: AOS
- **Icons**: Font Awesome 6
- **Hosting**: Render

## 📁 Project Structure

wordtemple-website/
├── app.py
├── admin.py
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── about.html
│ ├── leaders.html
│ ├── events.html
│ ├── gallery.html
│ ├── quotes.html
│ ├── give.html
│ └── conference-register.html
├── static/
│ ├── images/
│ └── videos/
└── requirements.txt

## 🛠️ Installation

```bash
git clone https://github.com/janetakinyi/wordtemple-website.git
cd wordtemple-website
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
