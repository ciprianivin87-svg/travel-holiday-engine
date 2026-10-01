import os
from dotenv import load_dotenv

load_dotenv()

from src.calendar_engine import get_upcoming_holiday_bridges
from src.ai_enricher import generate_destination_summary
from src.publisher import build_markdown_report, build_html_newsletter

def run_full_pipeline():
    print("=" * 60)
    print("🚀 ESECUZIONE PIPELINE COMPLETA: TRAVEL DEAL ENGINE")
    print("=" * 60)

    # 1. Recupera il prossimo ponte
    bridges = get_upcoming_holiday_bridges(country_code="IT")
    if not bridges:
        print("❌ Nessun ponte festivo trovato.")
        return

    bridge = bridges[0] # Prendiamo il primo ponte utile
    print(f"\n📌 Ponte Selezionato: {bridge['holiday_name']} ({bridge['departure_date']} ➔ {bridge['return_date']})")

    # 2. Dati Volo (Dato reale o Mock di fallback per il test)
    flight = {
        "city_from": "Bari",
        "airport_from": "BRI",
        "city_to": "Budapest",
        "airport_to": "BUD",
        "price": 75,
        "airline": "Wizz Air",
        "deep_link": f"https://www.kiwi.com/deep?marker={os.getenv('TRAVELPAYOUTS_MARKER', '784148')}"
    }

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

    # 4. Creazione Output (Markdown e HTML)
    os.makedirs("output", exist_ok=True)

    markdown_content = build_markdown_report(deal_payload)
    html_content = build_html_newsletter(deal_payload)

    with open("output/newsletter.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

    with open("output/newsletter.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("\n✅ ESECUZIONE COMPLETATA CON SUCCESSO!")
    print("📁 Generati i file:")
    print("   • output/newsletter.md (Per Telegram/Social)")
    print("   • output/newsletter.html (Per Newsletter Email)")
    print("=" * 60)

if __name__ == "__main__":
    run_full_pipeline()