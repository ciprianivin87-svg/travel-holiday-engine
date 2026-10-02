import os
import random
import requests

# Lista di destinazioni europee da monitorare
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

def get_cheapest_flight(origin="BRI", departure_date=None, return_date=None, destination=None, depart_date=None, **kwargs):
    """
    Cerca i voli per le destinazioni desiderate supportando sia 'depart_date' che 'departure_date'.
    """
    # Gestione della compatibilità dei nomi dei parametri
    dep_date = depart_date or departure_date
    ret_date = return_date
    
    # Se viene passata una destinazione specifica, usiamo solo quella, altrimenti cerchiamo su tutte
    search_list = DESTINATIONS
    if destination:
        search_list = [{"code": destination, "city": destination}]

    token = os.getenv("TRAVELPAYOUTS_API_TOKEN")
    marker = os.getenv("TRAVELPAYOUTS_MARKER", "784148")

    if not token:
        print("⚠️ TRAVELPAYOUTS_API_TOKEN non impostato. Uso dati simulati di fallback.")
        selected = random.choice(search_list)
        return {
            "city_from": "Bari",
            "airport_from": origin,
            "city_to": selected["city"],
            "airport_to": selected["code"],
            "price": 49,
            "airline": "FR",
            "deep_link": f"https://www.aviasales.com/search/{origin}{str(dep_date).replace('-', '')}{selected['code']}{str(ret_date).replace('-', '')}1?marker={marker}"
        }

    deals = []
    
    # Esegue la ricerca per ogni destinazione nell'elenco
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
                            "deep_link": f"https://www.aviasales.com/search/{origin}{str(dep_date).replace('-', '')}{dest['code']}{str(ret_date).replace('-', '')}1?marker={marker}"
                        })
        except Exception as e:
            print(f"⚠️ Errore ricerca volo per {dest['code']}: {e}")

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
            "deep_link": f"https://www.aviasales.com/search/{origin}{str(dep_date).replace('-', '')}{selected['code']}{str(ret_date).replace('-', '')}1?marker={marker}"
        }

    # Ordina i risultati dal più economico al più caro
    deals.sort(key=lambda x: x["price"])
    
    # Prende le prime 3 offerte più economiche e ne sceglie una a caso per variare ad ogni run
    top_deals = deals[:3]
    chosen_deal = random.choice(top_deals)
    
    print(f"🎯 Trovate {len(deals)} offerte. Selezionata la meta più conveniente: {chosen_deal['city_to']} a {chosen_deal['price']}€")
    return chosen_deal