import os
import requests

def build_markdown_report(deal_payload):
    bridge = deal_payload["bridge_info"]
    flight = deal_payload["flight"]
    guide = deal_payload["guide_text"]

    md = f"""# ✈️ Offerta Ponte: {bridge['holiday_name']}
**Periodo:** {bridge['departure_date']} - {bridge['return_date']} ({bridge['total_days']} giorni)

## 🛫 Volo Consigliato
- **Da:** {flight['city_from']} ({flight['airport_from']})
- **A:** {flight['city_to']} ({flight['airport_to']})
- **Prezzo:** {flight['price']}€
- **Compagnia:** {flight['airline']}
- **Prenota qui:** [Link Offerta]({flight['deep_link']})

## 🗺️ Guida di Viaggio
{guide}
"""
    return md


def build_html_newsletter(deal_payload):
    bridge = deal_payload["bridge_info"]
    flight = deal_payload["flight"]
    guide = deal_payload["guide_text"]

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #0066cc; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
        .card {{ border: 1px solid #ddd; padding: 20px; margin-top: 20px; border-radius: 8px; }}
        .btn {{ display: inline-block; background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 15px; }}
        .price {{ font-size: 24px; color: #28a745; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>✈️ Travel Deal Engine</h1>
        <p>Il tuo prossimo ponte festivo ti aspetta!</p>
    </div>
    
    <div class="card">
        <h2>🎉 {bridge['holiday_name']}</h2>
        <p><strong>Dal {bridge['departure_date']} al {bridge['return_date']}</strong> ({bridge['total_days']} giorni)</p>
        <hr>
        <h3>🛫 Volo Economico Trovato</h3>
        <p>{flight['city_from']} ({flight['airport_from']}) ➔ <strong>{flight['city_to']} ({flight['airport_to']})</strong></p>
        <p>Compagnia: {flight['airline']}</p>
        <p class="price">A partire da {flight['price']}€ A/R</p>
        <a href="{flight['deep_link']}" class="btn" target="_blank">Vedi e Prenota Volo</a>
    </div>

    <div class="card">
        <h3>🗺️ Cosa Fare e Vedere</h3>
        <div>{guide.replace('\n', '<br>')}</div>
    </div>
</body>
</html>"""
    return html


def send_email_campaign(html_content, subject):
    api_key = os.getenv("BREVO_API_KEY")
    sender_email = os.getenv("SENDER_EMAIL", "ciprianivin87@gmail.com")
    sender_name = os.getenv("SENDER_NAME", "Travel Deal Engine")

    if not api_key:
        print("⚠️ BREVO_API_KEY non trovata nelle variabili d'ambiente. Email non inviata.")
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

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
            print(f"❌ Errore Brevo ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Eccezione invio email: {e}")

    return False