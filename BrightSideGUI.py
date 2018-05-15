import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from geopy.geocoders import Nominatim
import urllib.request
import json
import time

root = Tk()
root.title("Serwis Pogodowy")
root.iconbitmap('iconopenweathermapsmall.ico')

mainWindow = Frame(root)
mainWindow.pack()


def callback():
    geolokalizator = Nominatim()
    #labelDane.configure(text = miasto.get() + ' ' + ulica.get())
    #print(lokalizacja)
    miastoGet = str(miasto.get())
    ulicaGet = str(ulica.get())
    lokalizacja = geolokalizator.geocode(ulicaGet + " " + miastoGet)
    szerokoscGeo = lokalizacja.latitude
    dlugoscGeo = lokalizacja.longitude
    labelLokalizacja.configure(text = lokalizacja.address + '\n' + 'szerokość: ' + str(szerokoscGeo) + ' długość: ' + str(dlugoscGeo))
    def pobierzCodeID():
        plik = open('codeid.txt','r')
        codeid = plik.readline()
        return codeid
    pobierzCodeID()
    codeid = pobierzCodeID()
    urlgeo = str("http://api.openweathermap.org/data/2.5/weather?lat=" + str(szerokoscGeo) + "&lon=" + str(
        dlugoscGeo) + "&appid=" + str(codeid) + "&lang=pl&units=metric")
    # odczytanie pliku json zawartego pod linkiem urlgeo
    plikjson = urllib.request.urlopen(urlgeo)
    jsonstring = plikjson.read()
    parsuj_json = json.loads(jsonstring)
    # zapis danych z pliku JSON do odpowiednich zmiennych
    pogoda = parsuj_json["weather"][0]["main"]
    pogodaPL = parsuj_json["weather"][0]["description"]
    zachmurzenie = parsuj_json["clouds"]["all"]
    cisnienie = parsuj_json["main"]["pressure"]
    temperatura = parsuj_json["main"]["temp"]
    temperaturaMin = parsuj_json["main"]["temp_min"]
    temperaturaMax = parsuj_json["main"]["temp_max"]
    wilgotnosc = parsuj_json["main"]["humidity"]
    wiatrPredkosc = parsuj_json["wind"]["speed"]
    wiatrKierunek = parsuj_json["wind"]["deg"]
    wschodSlonca = parsuj_json["sys"]["sunrise"]
    zachodSlonca = parsuj_json["sys"]["sunset"]
    labelPogoda.configure(text='Pogoda: ' + pogodaPL + '\n' + 'Zachmurzenie: ' + str(zachmurzenie) + '%' + '\n' + 'Ciśnienie: ' + str(cisnienie) + ' hPa' + '\n'
                          + 'Temp: ' + str(temperatura) + ' C' + '\n'
                          + 'TempMin: ' + str(temperaturaMin) + ' C' + '\n'
                          + 'TempMax: ' + str(temperaturaMax) + ' C' + '\n'
                          + 'Wilgotność: ' + str(wilgotnosc) + ' %' + '\n'
                          + 'Wiatr: ' + str(wiatrPredkosc) + ' m/s' + '\n'
                          + 'Kierunek wiatru: ' + str(wiatrKierunek) + ' st.' + '\n'
                          + 'Wschód: ' + str(time.ctime(wschodSlonca)) + '\t' + 'Zachód: ' + str(time.ctime(zachodSlonca)) + '\n')

    #return szerokoscGeo, dlugoscGeo


def saveCodeID():
    nameOfEntryCodeID = tk.StringVar
    windowSaveCodeID = Toplevel()#tk.Toplevel(root)
    windowSaveCodeID.title('CodeID')
    windowSaveCodeID.grab_set()
    #windowSaveCodeID.wait_window()
    windowSaveCodeID.configure(width = 400, height = 60)
    def czytajCodeID():
        plik = open('codeid.txt', 'r')
        codeID = plik.readline()
        plik.close()
        #nameOfEntryCodeID.set(codeID)
        #print(codeID)
        return codeID
        #return entryCodeID.configure(text = codeID)
        #print(nameOfEntryCodeID)
    czytajCodeID()
    codeID = czytajCodeID()
    #codeID = czytajCodeID(self)
    #print(nameOfEntryCodeID)

    def zapiszCodeIDdoPliku():
        plik = open('codeid.txt', 'w')
        plik.write(entryCodeID.get())
        plik.close()
        entryCodeID.configure(state = 'disabled')
    ttk.Label(master = windowSaveCodeID, text = 'Wpisz CodeID: ').grid(column = 0, row = 0)
    entryCodeID = ttk.Entry(master = windowSaveCodeID, width = 40, textvariable = codeID, state = 'normal')
    #nameOfEntryCodeID.set('codeID')
    entryCodeID.insert(0, codeID)
    entryCodeID.grid(column = 1, row = 0, padx = 3, pady = 6)
    entryCodeID.setvar()
    zamknijCodeID = ttk.Button(master = windowSaveCodeID, text = 'Zamknij', command = lambda: windowSaveCodeID.destroy())
    zamknijCodeID.grid(column = 0, row = 1, sticky = (E))
    edytujCodeID = ttk.Button(master = windowSaveCodeID, text = 'Edytuj', command = lambda: entryCodeID.configure(state = 'normal'))
    edytujCodeID.grid(column = 1, row = 1, sticky = (E))
    zapiszCodeID = ttk.Button(master = windowSaveCodeID, text = 'Zapisz', command = zapiszCodeIDdoPliku)#lambda: entryCodeID.configure(state = 'disabled'))
    zapiszCodeID.grid(column = 2, row = 1, sticky = (E))


def closeapp():
    root.quit()


def aboutapp():
    messagebox.showinfo('O programie', 'Serwis Pogodowy\nProgram oparty jest o serwis\nopenweathermap.org\nWymagane jest wygenerowanie własnego codeid\n'
                        'Autor: Pat O\'Kinah' )

miasto = tk.StringVar()
ulica = tk.StringVar()

menuBar = Menu(root)
root.config(menu=menuBar)

menuPlik = Menu(menuBar, tearoff = 0)
menuPlik.add_command(label = 'Add CodeID', command = saveCodeID)
menuPlik.add_separator()
menuPlik.add_command(label = 'Zamknij', command = closeapp)
menuBar.add_cascade(label = 'Plik', menu = menuPlik)

menuInfo = Menu(menuBar, tearoff = 0)
menuInfo.add_command(label = 'O programie', command = aboutapp)
menuBar.add_cascade(label = 'Info', menu = menuInfo)

labelMiasto = ttk.Label(master = mainWindow, text = "Miasto: ")
labelMiasto.grid(column = 1, row = 1, sticky = (W,E))
labelUlica = ttk.Label(master = mainWindow, text = "Ulica: ")
labelUlica.grid(column = 3, row = 1, sticky = (W,E))

zakladki = ttk.Notebook(master = mainWindow)
zakladkaPogDzis = ttk.Frame(zakladki)
zakladki.add(zakladkaPogDzis, text = 'Aktualnie')
zakladki.grid(columnspan = 5, row = 3, padx = 3, pady = 6, sticky = (W, E))
#zakladki.pack(expand =1, fill = 'both')

labelDane = ttk.Label(master = mainWindow, text = ' ')
labelDane.grid(columnspan = 5, row = 4,  padx = 3, pady = 6, sticky = (W,E))

labelLokalizacja = ttk.Label(master=zakladkaPogDzis, text = ' ')
labelLokalizacja.grid(columnspan = 5, row = 4, padx = 3, pady = 6, sticky = (W,E))

labelPogoda = ttk.Label(master=zakladkaPogDzis, text = ' ')
labelPogoda.grid(columnspan = 5, row = 5, padx = 3, pady = 6, sticky = (W,E))

entryMiasto = ttk.Entry(master = mainWindow, textvariable = miasto, width = 20)
entryMiasto.grid(column = 2, row = 1, padx = 3, pady = 6, sticky = (W, E))

entryUlica = ttk.Entry(master = mainWindow, textvariable = ulica, width = 30)
entryUlica.grid(column = 4, row = 1, padx = 3, pady = 6, sticky = (W, E))

batonOK = ttk.Button(master = mainWindow, text = "OK", width = 10, command = callback)
batonOK.grid(columnspan = 5, row = 2, padx = 3, pady = 6, sticky = (W, E))

root.mainloop()