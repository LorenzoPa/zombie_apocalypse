# 🧟‍♂️ Zombie Apocalypse

A Django-based **survival management game** where every player must try to survive day after day in a world overrun by zombies.

Each player controls their own **shelter**, managing resources like food, defense, and survivors — but beware: every new day brings a random event that could help you… or doom you.

---

## ⚙️ Features

- 🧑‍🤝‍🧑 User authentication (each user has their own shelter)
- 🏚️ Shelter management (food, survivors, defense, day counter)
- 🎲 Random daily events (attack, find food, disease, quiet day)
- 📅 “Next Day” mechanic that advances the game and returns results
- 🧩 REST API endpoints for interaction and status

---

## 🧰 Tech Stack

- Python 3.13
- Django 5
- Django REST Framework
- SQLite (default for simplicity)

---

## 🚀 Run Locally

**Clone the project:**
```bash
git clone https://github.com/YOUR_USERNAME/zombie_apocalypse.git  
cd zombie_apocalypse  
```
**Create a virtual environment and install dependencies:**
```bash
python -m venv .venv  
source .venv/bin/activate      # On Windows: .venv\Scripts\activate  
pip install -r requirements.txt  
```
**Run migrations and start the server:**
```bash
python manage.py migrate  
python manage.py runserver  
```
Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📡 API Endpoints (examples)

| Method | Endpoint | Description |
|---------|-----------|-------------|
| `GET` | `/api/shelter/status/` | Get current shelter status |
| `POST` | `/api/shelter/next_day/` | Advance one day and trigger a random event |

---

## 🧠 Game Logic

Each day consumes food and has a chance of a random event:
- **Attack:** Reduces defense, may cause survivor loss  
- **Find Food:** Increases food supply  
- **Disease:** Decreases survivors  
- **Quiet:** Nothing happens  

The goal is simple: **survive as many days as possible.**

---

## 💡 Future Plans

- Add more event types  
- Add images or icons for events  
- Implement a leaderboard system  
- Add front-end integration (React or Vue)

---

## 🧑‍💻 Author

Created by **Lorenzo Paniccia**  
✨ _“Survive. Adapt. Shine.”_
