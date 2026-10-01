import os
from google import genai

def generate_destination_summary(city_name, country_name, holiday_name, total_days):
    """
    Genera un'introduzione e consigli di viaggio per una destinazione
    in occasione di uno specifico ponte festivo.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  [ai_enricher] GEMINI_API_KEY non trovata nelle variabili d'ambiente.")
        return f"Scopri {city_name} durante il ponte di {holiday_name}!"

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Sei un copywriter esperto di viaggi per una newsletter di offerte low-cost.
    Scrivi una descrizione breve, ingaggiante ed entusiasta (massimo 120 parole) per invitare a visitare {city_name} ({country_name}) durante il ponte di {holiday_name} per una durata di {total_days} giorni.

    Includi:
    - Un titolo accattivante con emoji.
    - 2-3 cose imperdibili da vedere/fare in {total_days} giorni.
    - Un consiglio per il cibo tipico da assaggiare.
    
    Usa un tono fresco e accattivante, perfetto per una newsletter.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",  # Oppure "gemini-1.5-flash" / "gemini-2.0-flash"
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"❌ [ai_enricher] Errore durante la generazione Gemini: {e}")
        return f"Un'ottima opportunità per visitare {city_name} durante il ponte di {holiday_name}!"

if __name__ == "__main__":
    # Test del modulo
    print("--- TEST GEMINI AI ENRICHER ---")
    summary = generate_destination_summary(
        city_name="Praga",
        country_name="Repubblica Ceca",
        holiday_name="Immacolata Concezione",
        total_days=4
    )
    print("\nRisultato generato da Gemini:\n")
    print(summary)