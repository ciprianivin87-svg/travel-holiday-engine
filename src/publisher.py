import os
from datetime import datetime

def build_markdown_report(deal_data):
    """
    Genera un report formattato in Markdown pronto per Telegram o Post Social.
    """
    bridge = deal_data['bridge_info']
    flight = deal_data['flight']
    guide_text = deal_data['guide_text']

    markdown_output = f"""
🚨 **NUOVA OFFERTA PONTE: {bridge['holiday_name'].upper()}** 🚨

🗓 **Date:** dal {bridge['departure_date']} al {bridge['return_date']} ({bridge['total_days']} giorni)
✈️ **Volo:** {flight['city_from']} ({flight['airport_from']}) ➔ {flight['city_to']} ({flight['airport_to']})
💰 **Prezzo A/R:** **{flight['price']}€**
🌐 **Compagnia:** {flight['airline']}

---

{guide_text}

---

🔗 **[PRENOTA ORA IL VOLO A {flight['price']}€]({flight['deep_link']})**

*Offerta verificata in tempo reale. Le tariffe possono variare rapidamente.*
"""
    return markdown_output.strip()


def build_html_newsletter(deal_data):
    """
    Genera un template HTML pulito per invii via e-mail.
    """
    bridge = deal_data['bridge_info']
    flight = deal_data['flight']
    guide_text = deal_data['guide_text']

    # Convertiamo i break di linea in paragrafi HTML
    formatted_guide = "".join([f"<p>{paragraph}</p>" for paragraph in guide_text.split("\n\n") if paragraph.strip()])

    html_output = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offerta Ponte: {bridge['holiday_name']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 20px; color: #333; }}
        .card {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
        .header {{ background-color: #0066cc; color: #ffffff; padding: 20px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .content {{ padding: 20px; font-size: 15px; line-height: 1.6; }}
        .flight-badge {{ background-color: #e6f2ff; border-left: 4px solid #0066cc; padding: 15px; margin: 15px 0; border-radius: 4px; }}
        .cta-button {{ display: block; width: 220px; margin: 25px auto; padding: 12px 20px; background-color: #ff5722; color: #ffffff; text-align: center; text-decoration: none; font-weight: bold; border-radius: 5px; font-size: 16px; }}
        .footer {{ text-align: center; font-size: 12px; color: #888888; padding: 15px; border-top: 1px solid #eeeeee; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h1>✈️ Offerta Ponte: {bridge['holiday_name']}</h1>
        </div>
        <div class="content">
            <div class="flight-badge">
                <strong>🗓 Date:</strong> {bridge['departure_date']} ➔ {bridge['return_date']} ({bridge['total_days']} giorni)<br>
                <strong>📍 Tratta:</strong> {flight['city_from']} ({flight['airport_from']}) ➔ {flight['city_to']} ({flight['airport_to']})<br>
                <strong>🏷️ Prezzo:</strong> {flight['price']}€ A/R ({flight['airline']})
            </div>

            <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">

            {formatted_guide}

            <a href="{flight['deep_link']}" class="cta-button" target="_blank">Vedi e Prenota Volo</a>
        </div>
        <div class="footer">
            Travel Deal Engine • Ricevi le migliori offerte per i tuoi ponti festivi.
        </div>
    </div>
</body>
</html>
"""
    return html_output


if __name__ == "__main__":
    # Test isolato del publisher con dati fittizi
    mock_deal = {
        "bridge_info": {
            "holiday_name": "Immacolata Concezione",
            "departure_date": "2026-12-05",
            "return_date": "2026-12-08",
            "total_days": 4
        },
        "flight": {
            "city_from": "Bari",
            "airport_from": "BRI",
            "city_to": "Budapest",
            "airport_to": "BUD",
            "price": 68,
            "airline": "Wizz Air",
            "deep_link": "https://www.kiwi.com/deep?marker=784148"
        },
        "guide_text": "Ponte dell'Immacolata a Budapest: Magia e Terme!\n\nGoditi 4 giorni rilassandoti alle Terme Széchenyi e passeggiando tra i mercatini natalizi."
    }

    print("--- TEST PUBLISHER MARKDOWN ---")
    print(build_markdown_report(mock_deal))