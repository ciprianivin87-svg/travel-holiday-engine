import os
import requests
from datetime import datetime

TEQUILA_SEARCH_URL = "https://api.tequila.kiwi.com/v2/search"

def search_low_cost_flights(departure_date, return_date, fly_from="IT", max_price=100, limit=5):
    """
    Interroga l'API Voli usando le credenziali Travelpayouts / Kiwi.
    """
    api_key = os.getenv("TRAVELPAYOUTS_API_TOKEN") or os.getenv("KIWI_API_KEY")
    marker = os.getenv("TRAVELPAYOUTS_MARKER", "784148")
    
    if not api_key:
        print("⚠️  [flight_fetcher] Variabile 'TRAVELPAYOUTS_API_TOKEN' non trovata.")
        return []

    # Formattazione date per l'API (DD/MM/YYYY)
    date_from = datetime.strptime(departure_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    date_to = datetime.strptime(return_date, "%Y-%m-%d").strftime("%d/%m/%Y")

    headers = {
        "apikey": api_key,
        "accept": "application/json"
    }

    params = {
        "fly_from": fly_from,
        "date_from": date_from,
        "date_to": date_from,
        "return_from": date_to,
        "return_to": date_to,
        "flight_type": "round",
        "curr": "EUR",
        "price_to": max_price,
        "max_stopovers": 0,
        "sort": "price",
        "limit": limit
    }

    try:
        response = requests.get(TEQUILA_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        flights = []
        for item in data.get("data", []):
            raw_link = item.get("deep_link", "")
            # Iniezione automatica del Marker ID di Travelpayouts nell'URL se non già presente
            affiliate_link = f"{raw_link}&marker={marker}" if raw_link and "marker=" not in raw_link else raw_link

            flight_info = {
                "city_from": item.get("cityFrom"),
                "airport_from": item.get("flyFrom"),
                "city_to": item.get("cityTo"),
                "country_to": item.get("countryTo", {}).get("name"),
                "airport_to": item.get("flyTo"),
                "price": item.get("price"),
                "deep_link": affiliate_link,
                "airline": item["route"][0].get("airline") if item.get("route") else "N/A",
            }
            flights.append(flight_info)

        return flights

    except requests.exceptions.RequestException as e:
        print(f"❌ [flight_fetcher] Errore chiamata API: {e}")
        return []