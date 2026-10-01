import os
from dotenv import load_dotenv

load_dotenv()

from src.calendar_engine import get_upcoming_holiday_bridges
from src.flight_fetcher import get_cheapest_flight
from src.ai_enricher import generate_destination_summary
from src.publisher import build_markdown_report, build_html_newsletter

def run_full_pipeline():
    print("=" * 60)
    print("🚀 ESECUZIONE PIPELINE COMPLETA: TRAVEL DEAL ENGINE")
    print("=" * 60)

    # 1. Recupera il prossimo ponte festivo
    bridges = get_upcoming_holiday_bridges(country_code="IT")
    if not bridges:
        print("❌ Nessun ponte festivo trovato.")
        return

    bridge = bridges[0]
    print(f"\n📌 Ponte Selezionato: {bridge['holiday_name']} ({bridge['departure_date']} ➔ {bridge['return_date']})")

    # Definizione aeroporto di partenza e destinazione
    origin = "BRI"      # Bari (puoi cambiarlo con TRN, MXP, FCO, ecc.)
    destination = "BUD" # Budapest

    # 2. Ricerca volo reale tramite Travelpayouts API
    print(f"✈️ Ricerca voli in corso tramite Travelpayouts API ({origin} ➔ {destination})...")
    flight = get_cheapest_flight(
        origin=origin,
        destination=destination,
        depart_date=bridge['departure_date'],
        return_date=bridge['return_date']
    )

    # Fallback in caso di mancanza di dati temporanei dall'API
    if not flight:
        print("⚠️ Nessun volo restituito dall'API. Utilizzo offerta indicativa di fallback.")
        marker = os.getenv("TRAVELPAYOUTS_MARKER", "784148")
        flight = {
            "city_from": "Bari",
            "airport_from": origin,
            "city_to": "Budapest",
            "airport_to": destination,
            "price": 65,
            "airline": "Wizz Air / Ryanair",
            "deep_link": f"https://tp.media/r?marker={marker}&p=4114&u=https%3A%2F%2Fwww.aviasales.com"
        }
    else:
        print(f"✅ Volo trovato: {flight['price']}€ con {flight['airline']}")

    # 3. Generazione Guida Gemini AI
    print("🤖 Generazione contenuti AI con Gemini...")
    guide_text = generate_destination_summary(
        city_name=flight['city_to'],
        country_name="Ungheria",
        holiday_name=bridge['holiday_name'],
        total_days=bridge['total_days']
    )

    deal_payload = {
        "bridge_info": bridge,
        "flight": flight,
        "guide_text": guide_text
    }

    # 4. Generazione Output (Markdown e HTML)
    os.makedirs("output", exist_ok=True)

    markdown_content = build_markdown_report(deal_payload)
    html_content = build_html_newsletter(deal_payload)

    with open("output/newsletter.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

    with open("output/newsletter.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("\n✅ ESECUZIONE COMPLETATA CON SUCCESSO!")
    print("📁 Generati i file:")
    print("   • output/newsletter.md")
    print("   • output/newsletter.html")
    print("=" * 60)

if __name__ == "__main__":
    run_full_pipeline()