import os
from dotenv import load_dotenv

load_dotenv()

from src.calendar_engine import get_upcoming_holiday_bridges
from src.ai_enricher import generate_destination_summary

def run_step3_test():
    print("=" * 60)
    print("🚀 TEST INTEGRATO STEP 3: CALENDAR + GEMINI AI")
    print("=" * 60)

    bridges = get_upcoming_holiday_bridges(country_code="IT")
    if not bridges:
        print("Nessun ponte trovato.")
        return

    test_bridge = bridges[0]
    print(f"\n📌 Ponte Selezionato: {test_bridge['holiday_name']} ({test_bridge['departure_date']} -> {test_bridge['return_date']})")

    # Esempio di destinazione di test
    destinazione = "Budapest"
    paese = "Ungheria"

    print(f"🤖 Generazione guida turistica AI per {destinazione}...")
    ai_text = generate_destination_summary(
        city_name=destinazione,
        country_name=paese,
        holiday_name=test_bridge['holiday_name'],
        total_days=test_bridge['total_days']
    )

    print("\n--- RISULTATO ---")
    print(ai_text)
    print("=" * 60)

if __name__ == "__main__":
    run_step3_test()