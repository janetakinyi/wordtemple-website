# Word Temple Church of God International Website

![Word Temple Church](https://img.shields.io/badge/Word-Temple%20Church-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.3-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📖 About The Project

This is the official website for **Word Temple Church of God International**, a dynamic and growing ministry based in Eastleigh, Nairobi, Kenya.

## 🚀 Live Demo

[View Website](https://wordtemple-website.onrender.com)


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
