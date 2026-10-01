from datetime import date, timedelta
import holidays

def get_upcoming_holiday_bridges(country_code="IT", year=None, min_days=3, max_days=5):
    """
    Identifica i weekend lunghi e i ponti festivi per un dato paese e anno.
    
    :param country_code: Codice ISO del paese (es. 'IT' per l'Italia)
    :param year: Anno di riferimento (default: anno corrente)
    :param min_days: Numero minimo di giorni consecutivi di vacanza
    :param max_days: Numero massimo di giorni complessivi della finestra
    :return: Lista di dizionari contenenti le finestre di viaggio individuate
    """
    if year is None:
        year = date.today().year

    # Ottiene i giorni festivi nazionali per il paese specificato
    national_holidays = holidays.country_holidays(country_code, years=year)
    
    travel_windows = []
    
    # Analizziamo le festività dell'anno
    for holiday_date, name in sorted(national_holidays.items()):
        # Consideriamo solo le festività da oggi in poi
        if holiday_date < date.today():
            continue
            
        weekday = holiday_date.weekday() # 0 = Lunedì, 3 = Giovedì, 4 = Venerdì, etc.
        
        start_date = None
        end_date = None
        vacation_days_needed = 0

        # Caso A: La festività cade di Lunedì (Weekend lungo: Sabato - Lunedì)
        if weekday == 0:
            start_date = holiday_date - timedelta(days=2) # Sabato
            end_date = holiday_date                        # Lunedì
            vacation_days_needed = 0

        # Caso B: La festività cade di Venerdì (Weekend lungo: Venerdì - Domenica)
        elif weekday == 4:
            start_date = holiday_date                      # Venerdì
            end_date = holiday_date + timedelta(days=2)   # Domenica
            vacation_days_needed = 0

        # Caso C: La festività cade di Giovedì (Ponte: Giovedì - Domenica, 1 giorno di ferie)
        elif weekday == 3:
            start_date = holiday_date                      # Giovedì
            end_date = holiday_date + timedelta(days=3)   # Domenica
            vacation_days_needed = 1                       # Venerdì

        # Caso D: La festività cade di Martedì (Ponte: Sabato - Martedì, 1 giorno di ferie)
        elif weekday == 1:
            start_date = holiday_date - timedelta(days=3) # Sabato
            end_date = holiday_date                       # Martedì
            vacation_days_needed = 1                      # Lunedì

        if start_date and end_date:
            total_days = (end_date - start_date).days + 1
            travel_windows.append({
                "holiday_name": name,
                "holiday_date": holiday_date.strftime("%Y-%m-%d"),
                "departure_date": start_date.strftime("%Y-%m-%d"),
                "return_date": end_date.strftime("%Y-%m-%d"),
                "total_days": total_days,
                "ferie_needed": vacation_days_needed
            })

    return travel_windows


if __name__ == "__main__":
    # Test del modulo
    print("--- RICERCA PONTI E WEEKEND LUNGHI IN ITALIA ---")
    windows = get_upcoming_holiday_bridges(country_code="IT")
    for w in windows:
        print(f"\n🎉 Festività: {w['holiday_name']} ({w['holiday_date']})")
        print(f"   🛫 Partenza: {w['departure_date']} | 🛬 Rientro: {w['return_date']}")
        print(f"   ⏱️ Giorni totali: {w['total_days']} | 🏖️ Giorni di ferie richiesti: {w['ferie_needed']}")