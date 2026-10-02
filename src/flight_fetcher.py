import os
import random
import requests
import urllib.parse
from datetime import datetime

# Lista delle destinazioni europee monitorate da Bari (BRI)
DESTINATIONS = [
    {"code": "BUD", "city": "Budapest"},
    {"code": "PRG", "city": "Praga"},
    {"code": "VIE", "city": "Vienna"},
    {"code": "LON", "city": "Londra"},
    {"code": "BCN", "city": "Barcellona"},
    {"code": "PAR", "city": "Parigi"},
    {"code": "BER", "city": "Berlino"},
    {"code": "KRK", "city": "Cracovia"},
    {"code": "MAD", "city": "Madrid"}
]

def format_aviasales_url(origin, dest, departure_date, return_date, marker):
    """
    Formatta l'URL impostando in automatico:
    - Dominio italiano (aviasales.it)
    - Mercato Italia (&market=it)
    - Lingua Italiana (&locale=it)
    - Valuta Euro (&currency=EUR)
    - Tracciamento affiliazione Travelpayouts (&marker=...)
    """
    try:
        dep_dt = datetime.strptime(str(departure_date), "%Y-%m-%d")
        ret_dt = datetime.strptime(str(return_date), "%Y-%m-%d")
        dep_str = dep_dt.strftime("%d%m")  # Formato GGMM (es. 0512 per 5 Dicembre)
        ret_str = ret_dt.strftime("%d%m")  # Formato GGMM (es. 0812 per 8 Dicembre)
        search_path = f"{origin}{dep_str}{dest}{ret_str}1"
    except Exception:
        dep_clean = str(departure_date).replace('-', '')
        ret_clean = str(return_date).replace('-', '')
        search_path = f"{origin}{dep_clean}{dest}{ret_clean}1"

    # URL diretto su aviasales.it con paese, lingua e valuta forzati
    target_url = (
        f"https://www.aviasales.it/search/{search_path}"
        f"?marker={marker}&currency=EUR&locale=it&market=it"
    )
    return target_url

def get_cheapest_flight(origin="BRI", departure_date=None, return_date=None, destination=None, depart_date=None, **kwargs):
    """
    Cerca il volo più conveniente su Travelpayouts per le date specificate.
    Accetta sia departure_date sia depart_date per retrocompatibilità.
    """
    dep_date = depart_date or departure_date
    ret_date = return_date
    
    search_list = DESTINATIONS
    if destination:
        search_list = [{"code": destination, "city": destination}]

    token = os.getenv("TRAVELPAYOUTS_API_TOKEN")
    marker = os.getenv("TRAVELPAYOUTS_MARKER", "784148")

    # Se non c'è il token API, restituisce un volo generato di fallback
    if not token:
        print("⚠️ TRAVELPAYOUTS_API_TOKEN non impostato. Uso dati simulati di fallback.")
        selected = random.choice(search_list)
        return {
            "city_from": "Bari",
            "airport_from": origin,
            "city_to": selected["city"],
            "airport_to": selected["code"],
            "price": 49,
            "airline": "Ryanair / Wizz Air",
            "deep_link": format_aviasales_url(origin, selected["code"], dep_date, ret_date, marker)
        }

    deals = []
    
    for dest in search_list:
        url = "https://api.travelpayouts.com/v2/prices/week-matrix"
        params = {
            "currency": "EUR",
            "origin": origin,
            "destination": dest["code"],
            "show_to_affiliates": "true",
            "depart_date": dep_date,
            "return_date": ret_date,
            "token": token
        }
        
        try:
            res = requests.get(url, params=params, timeout=10)
            if res.status_code == 200:
                data = res.json().get("data", [])
                for item in data:
                    if item.get("depart_date") == dep_date and item.get("return_date") == ret_date:
                        deals.append({
                            "city_from": "Bari",
                            "airport_from": origin,
                            "city_to": dest["city"],
                            "airport_to": dest["code"],
                            "price": int(item.get("value", 999)),
                            "airline": item.get("gate", "Volo Diretto"),
                            "deep_link": format_aviasales_url(origin, dest["code"], dep_date, ret_date, marker)
                        })
        except Exception as e:
            print(f"⚠️ Errore ricerca volo per {dest['code']}: {e}")

    # Fallback nel caso in cui l'API non restituisca risultati per le date indicate
    if not deals:
        print("⚠️ Nessun volo trovato tramite API per le date selezionate. Generazione offerta di fallback.")
        selected = random.choice(search_list)
        return {
            "city_from": "Bari",
            "airport_from": origin,
            "city_to": selected["city"],
            "airport_to": selected["code"],
            "price": 55,
            "airline": "Wizz Air / Ryanair",
            "deep_link": format_aviasales_url(origin, selected["code"], dep_date, ret_date, marker)
        }

    # Ordina le offerte per prezzo e ne sceglie una tra le prime tre più economiche
    deals.sort(key=lambda x: x["price"])
    top_deals = deals[:3]
    chosen_deal = random.choice(top_deals)
    
    print(f"🎯 Trovate {len(deals)} offerte. Selezionata la meta più conveniente: {chosen_deal['city_to']} a {chosen_deal['price']}€")
    return chosen_deal