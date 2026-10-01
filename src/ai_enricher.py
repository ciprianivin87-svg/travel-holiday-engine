import os
import time
import google.generativeai as genai

def generate_destination_summary(city_name, country_name, holiday_name, total_days):
    """
    Genera la guida di viaggio tramite Gemini con gestione del retry in caso di 503.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ GEMINI_API_KEY non trovata. Utilizzo guida di fallback.")
        return build_fallback_guide(city_name, holiday_name, total_days)

    genai.configure(api_key=api_key)
    
    # Utilizziamo il modello stabile gemini-3.8-flash
    model = genai.GenerativeModel("gemini-3.8-flash")

    prompt = f"""
    Crea una guida di viaggio breve, accattivante ed entusiasmante per una newsletter di viaggi.
    
    Destinazione: {city_name}, {country_name}
    Occasione: {holiday_name}
    Durata soggiorno: {total_days} giorni
    
    Includi:
    - Un'introduzione d'impatto sul perché visitare {city_name} durante {holiday_name}.
    - 3 attrazioni o attività imperdibili da fare in {total_days} giorni.
    - Un consiglio culinario tipico della zona.
    
    Usa formattazione HTML pulita (paragrafi <p>, elenchi <ul> e <li>, grassetti <strong>). Non includere i tag <html> o <body>.
    """

    # Tentativi automatici con pausa (backoff)
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"⚠️ Tentativo {attempt}/{max_retries} fallito per Gemini ({e})...")
            if attempt < max_retries:
                time.sleep(3) # Attendi 3 secondi prima di riprovare

    print("❌ Tutti i tentativi con Gemini sono falliti. Utilizzo guida di fallback.")
    return build_fallback_guide(city_name, holiday_name, total_days)


def build_fallback_guide(city_name, holiday_name, total_days):
    return f"""
    <p>Preparati a vivere un'esperienza fantastica a <strong>{city_name}</strong> durante il ponte di <strong>{holiday_name}</strong>!</p>
    <p>Con <strong>{total_days} giorni</strong> a disposizione avrai il tempo ideale per esplorare i luoghi più iconici del centro storico, scoprire la cultura locale e assaggiare le specialità culinarie tipiche.</p>
    <ul>
        <li><strong>Giro del Centro Storico:</strong> Passeggia tra le attrazioni principali ed i monumenti simbolo.</li>
        <li><strong>Enogastronomia Locale:</strong> Scopri i piatti tradizionali nei ristoranti caratteristici.</li>
        <li><strong>Relax e Atmosfera:</strong> Goditi lo spirito festivo della città durante questo ponte.</li>
    </ul>
    """