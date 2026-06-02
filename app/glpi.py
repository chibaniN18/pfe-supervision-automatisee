import requests

GLPI_URL = "http://192.168.211.40/glpi"
GLPI_TOKEN = "ay7N5GXNjH7jvhhUZzNf9Y95MM9cpEre5a5unv90"
GLPI_APP_TOKEN = "NXL65lQN9H99uZN0G758uVwjm4clrMB8RuwqdHUR"
def create_glpi_ticket(title, description, urgency=3):
    """Créer un ticket dans GLPI automatiquement"""
    try:
        # Initialiser la session GLPI
        session = requests.get(
            f"{GLPI_URL}/apirest.php/initSession",
            headers={
                "Authorization": f"user_token {GLPI_TOKEN}",
                "App-Token": GLPI_APP_TOKEN
            }
        )
        
        print(f"🔍 Session response: {session.status_code} - {session.json()}")
        
        response_data = session.json()
        
        if isinstance(response_data, list):
            print(f"❌ Erreur GLPI: {response_data}")
            return None
            
        session_token = response_data.get("session_token")
        
        if not session_token:
            print(f"❌ Pas de session_token: {response_data}")
            return None

        # Créer le ticket
        ticket = requests.post(
            f"{GLPI_URL}/apirest.php/Ticket",
            headers={
                "Session-Token": session_token,
                "App-Token": GLPI_APP_TOKEN,
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
