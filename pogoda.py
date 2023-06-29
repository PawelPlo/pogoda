import os
import pickle
import requests
import datetime
from datetime import timedelta




def zwrot_prognozy(opad):
    opad = float(opad)
    if opad == 0:
        print("W dniu {} nie będzie padało.".format(searched_date_in))
    if opad > 0:
        print("W dniu {} spadnie {} mm deszczu".format(searched_date_in, opad))

baza_danych = {}


if "baza_danych.txt" not in os.listdir():
    open("baza_danych.txt", "w").close()

else:
    pass

with open("baza_danych.txt", "r") as plik:
    for linia in plik:
        linia = linia.split()
        data, opad = linia
        baza_danych[data] = opad





print("-------- SPRAWDŹ CZY BĘDZIE PADAŁO W WARSZAWIE ---------\n")




while True:
    date_today = datetime.datetime.now().date()
    date_tomorrow = date_today + timedelta(1)
    date_today = datetime.datetime.now().date().strftime('%Y-%m-%d')
    date_today = str(date_today).strip()
    date_tomorrow = str(date_tomorrow).strip()
    print(f"Dzisiejsza data:{date_today}\n")
    searched_date_in=input('''Wciśni "ENTER" jeśli chcesz prognozę na jutro. 
Jeśli chcesz prognozę na inny dzień, wpisz date w formacie YYYY-MM-DD: ''')
    if not searched_date_in:
        searched_date_in = date_tomorrow
    if searched_date_in in baza_danych:
        opad=baza_danych[searched_date_in]
        zwrot_prognozy(opad)
        zapytanie = input("Czy chcesz sprawdzić inną datę ? (odp: T/N): ").strip()
        zapytanie = zapytanie.lower()
        if zapytanie == "n":
            break
        if zapytanie == "t":
            continue


    params = {
        "latitude": 52,
        "longitude": -21,
        "hourly": "rain",
        "timezone": "Europe/London",
        "daily": "rain_sum",
        "start_date": str(searched_date_in),
        "end_date": str(searched_date_in)
}
    url = "https://api.open-meteo.com/v1/forecast"

    resp = requests.get(url,params=params)

    if resp.ok:
        opad = resp.json()["daily"]["rain_sum"][0]
        zwrot_prognozy(opad)
        zapytanie = input("Czy chcesz sprawdzić inną datę ? (odp: T/N): ").strip()
        zapytanie = zapytanie.lower()
        baza_danych[searched_date_in] = resp.json()["daily"]["rain_sum"][0]
        with open("baza_danych.txt", "w") as plik:
            for data, opad in baza_danych.items():
                plik.write(f"{data} {opad}\n")
        if zapytanie == "n":
            break
        if zapytanie == "t":
            continue
    if not resp.ok:
        print("Wpisałeś datę w złym formacie, lub nie ma prognozy na tą datę!\n")
        print(resp.text)
        zapytanie = input("Czy chcesz spróbować raz jeszcze? (odp: T/N): ").strip()
        zapytanie = zapytanie.lower()
        if zapytanie == "n":
            break
        if zapytanie == "t":
            continue

