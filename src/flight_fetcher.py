import os
import requests

def get_cheapest_flight(origin="BRI", destination="BUD", depart_date=None, return_date=None):
    """
    Cerca il volo più economico tramite la Travelpayouts / Aviasales Data API.
    """
    token = os.getenv("TRAVELPAYOUTS_API_TOKEN")
    marker = os.getenv("TRAVELPAYOUTS_MARKER", "784148")
    
    if not token:
        print("⚠️ TRAVELPAYOUTS_API_TOKEN non trovato nelle variabili d'ambiente.")
        return None

    url = "https://api.travelpayouts.com/v1/prices/cheap"
    
    headers = {
        "x-access-token": token
    }
    
    params = {
        "origin": origin,
        "destination": destination,
        "currency": "EUR"
    }

    # Se le date sono fornite nel formato YYYY-MM-DD, estraiamo l'anno-mese per l'endpoint
    if depart_date:
        params["depart_date"] = depart_date[:7]
    if return_date:
        params["return_date"] = return_date[:7]

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()

        if data.get("success") and destination in data.get("data", {}):
            destination_deals = data["data"][destination]
            
            # Selezioniamo la prima offerta disponibile
            offer_key = list(destination_deals.keys())[0]
            deal = destination_deals[offer_key]
            
            # Costruzione deeplink affiliato per la ricerca specifica su Aviasales
            formatted_depart = depart_date.replace("-", "")[2:] if depart_date else ""
            formatted_return = return_date.replace("-", "")[2:] if return_date else ""
            
            search_url = f"https://www.aviasales.com/search/{origin}{formatted_depart}{destination}{formatted_return}1"
            deep_link = f"https://tp.media/r?marker={marker}&p=4114&u={requests.utils.quote(search_url)}"

            return {
                "city_from": origin,
                "airport_from": origin,
                "city_to": destination,
                "airport_to": destination,
                "price": deal.get("price"),
                "airline": deal.get("airline", "Multi-compagnia"),
                "deep_link": deep_link
            }
        else:
            print(f"ℹ️ Nessun volo trovato tramite API per la tratta {origin} -> {destination}")
    except Exception as e:
        print(f"❌ Errore durante la chiamata a Travelpayouts API: {e}")

    return None