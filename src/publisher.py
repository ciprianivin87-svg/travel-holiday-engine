import os
import requests

def send_email_campaign(html_content, subject):
    """
    Invia l'email tramite l'API REST v3 di Brevo.
    """
    api_key = os.getenv("BREVO_API_KEY")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_name = os.getenv("SENDER_NAME", "Travel Deal Engine")
    list_id = int(os.getenv("LIST_ID", "2")) # ID della lista iscritti su Brevo

    if not api_key or not sender_email:
        print("⚠️ Brevo non configurato: BREVO_API_KEY o SENDER_EMAIL mancanti nelle variabili d'ambiente.")
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    # Opzione A: Invio a una lista di contatti (Campaign Transazionale / Batch)
    # Se vuoi inviare a un singolo destinatario di prova (es. te stesso):
    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": sender_email, "name": "Iscritto Travel Deals"}],
        "subject": subject,
        "htmlContent": html_content
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code in [200, 201]:
            print("📬 Email inviata con successo tramite Brevo!")
            return True
        else:
            print(f"❌ Errore invio email Brevo ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Eccezione durante l'invio dell'email: {e}")

    return False