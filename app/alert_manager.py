import psutil
import requests
import time
from datetime import datetime

# Configuration
API_URL = "http://localhost:8001/alerts/"
CHECK_INTERVAL = 30  # vérification toutes les 30 secondes

# Seuils d'alerte
THRESHOLDS = {
    "cpu": {"warning": 70, "critical": 90},
    "memory": {"warning": 70, "critical": 90},
    "disk": {"warning": 80, "critical": 95}
}

def send_alert(title, description, level, source):
    """Envoyer une alerte à l'API FastAPI"""
    try:
        response = requests.post(API_URL, json={
            "title": title,
            "description": description,
            "level": level,
            "source": source
        })
        if response.status_code == 200:
            print(f"✅ Alerte envoyée : {title}")
        else:
            print(f"❌ Erreur envoi alerte : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur connexion API : {e}")

def check_cpu():
    """Vérifier l'utilisation CPU"""
    cpu = psutil.cpu_percent(interval=1)
    print(f"CPU : {cpu}%")
    if cpu >= THRESHOLDS["cpu"]["critical"]:
        send_alert(
            title=f"CPU Critique : {cpu}%",
            description=f"Utilisation CPU critique détectée : {cpu}%",
            level="critical",
            source="Alert Manager"
        )
    elif cpu >= THRESHOLDS["cpu"]["warning"]:
        send_alert(
            title=f"CPU Élevé : {cpu}%",
            description=f"Utilisation CPU élevée détectée : {cpu}%",
            level="warning",
            source="Alert Manager"
        )

def check_memory():
    """Vérifier l'utilisation mémoire"""
    memory = psutil.virtual_memory().percent
    print(f"Mémoire : {memory}%")
    if memory >= THRESHOLDS["memory"]["critical"]:
        send_alert(
            title=f"Mémoire Critique : {memory}%",
            description=f"Utilisation mémoire critique détectée : {memory}%",
            level="critical",
            source="Alert Manager"
        )
    elif memory >= THRESHOLDS["memory"]["warning"]:
        send_alert(
            title=f"Mémoire Élevée : {memory}%",
            description=f"Utilisation mémoire élevée détectée : {memory}%",
            level="warning",
            source="Alert Manager"
        )

def check_disk():
    """Vérifier l'utilisation disque"""
    disk = psutil.disk_usage('/').percent
    print(f"Disque : {disk}%")
    if disk >= THRESHOLDS["disk"]["critical"]:
        send_alert(
            title=f"Disque Critique : {disk}%",
            description=f"Utilisation disque critique détectée : {disk}%",
            level="critical",
            source="Alert Manager"
        )
    elif disk >= THRESHOLDS["disk"]["warning"]:
        send_alert(
            title=f"Disque Élevé : {disk}%",
            description=f"Utilisation disque élevée détectée : {disk}%",
            level="warning",
            source="Alert Manager"
        )

def main():
    print("🚀 Alert Manager démarré")
    print(f"⏱️  Vérification toutes les {CHECK_INTERVAL} secondes")
    print(f"📡 API URL : {API_URL}")
    print("─" * 40)
    
    while True:
        print(f"\n🕐 Vérification : {datetime.now().strftime('%H:%M:%S')}")
        check_cpu()
        check_memory()
        check_disk()
        print("─" * 40)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
