import json
import requests
from bs4 import BeautifulSoup   # Scraping HTML
import re
import datetime

# PATH
#path = "/home/fran/Escritorio/Proyecto2/salida.txt"
#file = open(path, "w+")

def date1(dd, mm, yyyy):                            # yyyy-MM-dd
    if dd < 10 and mm < 10:
        return str("%i-0%i-0%i" % (yyyy, mm, dd))

    if dd > 10 and mm < 10:
        return str("%i-0%i-%i" % (yyyy, mm, dd))

    if dd < 10 and mm >= 10:
        return str("%i-%i-0%i" % (yyyy, mm, dd))

    if dd > 10 and mm >= 10:
        return str("%i-%i-%i" % (yyyy, mm, dd))

def date2(dd, mm, yyyy):                            # dd-MM-yyyy
    if dd < 10 and mm < 10:
        return str("0%i-0%i-%i" % (dd, mm, yyyy))

    if dd > 10 and mm < 10:
        return str("%i-0%i-%i" % (dd, mm, yyyy))

    if dd < 10 and mm >= 10:
        return str("0%i-%i-%i" % (dd, mm, yyyy))

    if dd > 10 and mm >= 10:
        return str("%i-%i-%i" % (dd, mm, yyyy))

def data_url(fecha1, fecha2):
    return str("http://www.movistarplus.es/programacion-tv/" + fecha1 + "/?v=json&verticalScroll=true&isMobile=true&date=Tue+Dec+06+2016+00%3A00%3A00+GMT%2B0000+(Coordinated+Universal+Time)&calculada=Tue+Dec+06+2016+00%3A00%3A00+GMT%2B0000+(Coordinated+Universal+Time)&fecha=" + fecha2)

# url with .json
#url = "http://www.movistarplus.es/programacion-tv/" + fecha1 + "/?v=json&verticalScroll=true&isMobile=true&date=Tue+Dec+06+2016+00%3A00%3A00+GMT%2B0000+(Coordinated+Universal+Time)&calculada=Tue+Dec+06+2016+00%3A00%3A00+GMT%2B0000+(Coordinated+Universal+Time)&fecha=" + fecha2

def download_epg(url):
    DATA_FILE = requests.get(url).json()
    DATA = json.loads(json.dumps(DATA_FILE["data"]))

    return DATA

# Download de data .json
#DATA_FILE = requests.get(url).json()
# Parsing the first category
#DATOS = json.loads(json.dumps(DATA_FILE["data"]))

# Get all the Channels-ID
#for x in DATOS:
#    print(x)

def get_epg_channel(channel_code, DATA):
    CHANNEL = json.loads(json.dumps(DATA[channel_code]))
    CHANNEL_SHOWS = json.loads(json.dumps(CHANNEL["PROGRAMAS"]))

    return CHANNEL_SHOWS

#print(get_epg_channel("MV1-CODE", download_epg(data_url(date1(25,4,2019),date2(25,4,2019)))))

# Parsing into the Channel
#CANAL = json.loads(json.dumps(DATOS["MV1-CODE"]))
# Parsing into the shows
#CANAL_EVENTOS = json.loads(json.dumps(CANAL["PROGRAMAS"]))

def collecting_shows(epg_channel):
    for show in epg_channel:
        if show['TEMPORADA'] != '':
            segmento = show['TITULO'].split(" " + show['TEMPORADA'] + ": ")
            print("TITULO: %s" % segmento[0])

            if len(show['TEMPORADA']) == 4:
                print("TEMPORADA: %s" % show['TEMPORADA'][2:3])
            else:
                print("TEMPORADA: %s" % show['TEMPORADA'][2:4])

            print("EPISODIO: %s" % segmento[1])

        else:
            print("TITULO: %s" % show['TITULO'])

        print("GENERO: %s" % show['GENERO'])
        print("INICIO: %s" % show['HORA_INICIO'])
        print("FIN: %s" % show['HORA_FIN'])
        print("DURACION: %i min." % show['DURACION'])

        if show['ESTRENO']:
            print("ESTRENO: Si")
        
        print("URL: %s" % show['URL'])

        # Parsing the HTML content
        page = requests.get(show['URL'])
        soup = BeautifulSoup(page.text, 'html.parser')

        # Scraping Sinopsis from URL
        sinopsis = soup.find('div', {"class": "text show-more-height"})
        sinopsis_content = sinopsis.find('p')
        clear_sinopsis = str(sinopsis_content).replace('<p>', '')
        clear_sinopsis = clear_sinopsis.replace('</p>', '')
        print("SINOPSIS: %s" % clear_sinopsis)

        # Scraping Languages and Subtitles
        language = soup.find(string=re.compile("Idioma:"))
        subtitles = soup.find(string=re.compile("Subtítulos:"))
        print(language)
        print(subtitles)

        # Scraping Quality
        content = soup.find('ul', {'class': 'list-info-movie'})
        quality = content.findAll('li')
        
        if len(quality) == 1:
            try:
                quality_clear = re.search('alt="(.+?)" src=', str(quality)).group(1)
            except AttributeError:
                quality_clear = ''
            print(quality_clear)
        
        # Scraping Moral
        content = soup.find('div', {'class': 'moral'})

        try:
            moral = re.search('alt="(.+?)" src=', str(content)).group(1)
        except AttributeError:
            moral = ''

        print("Calificación: %s" % moral)
        print("")

for x in range(25, 27):
    print("EPG DAY %i:" % x)
    collecting_shows(get_epg_channel("FOXGE-CODE", download_epg(data_url(date1(x,4,2019),date2(x,4,2019)))))

    print("Grabbing finished succesfully\n")'''

#file.close()