from fastapi import FastAPI
from .database import engine, Base
from .routers import alerts
import requests
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Système de Monitoring - API",
    description="API de gestion des alertes pour le projet PFE",
    version="1.0.0"
)

app.include_router(alerts.router)

# Configuration GLPI
GLPI_URL = "http://192.168.211.40/glpi"
GLPI_TOKEN = "ay7N5GXNjH7jvhhUZzNf9Y95MM9cpEre5a5unv90"  # ← remplace par ton token

def create_glpi_ticket(title, description, urgency=3):
    """Créer un ticket dans GLPI automatiquement"""
    try:
        # Initialiser la session GLPI
        session = requests.get(
            f"{GLPI_URL}/apirest.php/initSession",
            headers={
                "Authorization": f"user_token {GLPI_TOKEN}",
                "App-Token": GLPI_TOKEN
            }
        )
        session_token = session.json().get("session_token")

        # Créer le ticket
        ticket = requests.post(
            f"{GLPI_URL}/apirest.php/Ticket",
            headers={
                "Session-Token": session_token,
                "App-Token": GLPI_TOKEN,
                "Content-Type": "application/json"
            },
            json={
                "input": {
                    "name": title,
                    "content": description,
                    "urgency": urgency,
                    "priority": urgency,
                    "type": 1
                }
            }
        )
        print(f"✅ Ticket GLPI créé : {ticket.json()}")
        return ticket.json()

    except Exception as e:
        print(f"❌ Erreur création ticket GLPI : {e}")
        return None

@app.get("/")
def read_root():
    return {
        "message": "API de Monitoring opérationnelle",
        "version": "1.0.0",
        "endpoints": {
            "alerts": "/alerts",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }
