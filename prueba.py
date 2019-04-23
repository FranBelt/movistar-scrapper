import json
import requests
from bs4 import BeautifulSoup   # Scraping HTML
import re

# PATH
#path = "/home/fran/Escritorio/Proyecto2/salida.txt"
#file = open(path, "w+")

# Only for testing
dd = 25
mm = 4
yyyy = 2019

# Watch out with 1-9 days of the month, need adjustment
fecha1 = str(yyyy) + "-0" + str(mm) + "-" + str(dd) # yyyy-MM-dd
fecha2 = str(dd) + "0" + str(mm) + str(yyyy) # dd-mm-yyyy

# url with .json
url = "http://www.movistarplus.es/programacion-tv/" + fecha1 + "/?v=json&verticalScroll=true&isMobile=true&date=Tue+Dec+06+2016+00%3A00%3A00+GMT%2B0000+(Coordinated+Universal+Time)&calculada=Tue+Dec+06+2016+00%3A00%3A00+GMT%2B0000+(Coordinated+Universal+Time)&fecha=" + fecha2

# Download de data .json
DATA_FILE = requests.get(url).json()

# Parsing the first category
DATOS = json.loads(json.dumps(DATA_FILE["data"]))

# Get all the Channels-ID
#for x in DATOS:
#    print(x)

# Parsing into the Channel
CANAL = json.loads(json.dumps(DATOS["FOXGE-CODE"]))

# Parsing into the shows
CANAL_EVENTOS = json.loads(json.dumps(CANAL["PROGRAMAS"]))

# Showing all the shows
for element in CANAL_EVENTOS:
    if element['TEMPORADA'] != '':
        segmento = element['TITULO'].split(" " + element['TEMPORADA'] + ": ")
        print("TITULO: %s" % segmento[0])

        if len(element['TEMPORADA']) == 4:
            print("TEMPORADA: %s" % element['TEMPORADA'][2:3])
        else:
            print("TEMPORADA: %s" % element['TEMPORADA'][2:4])

        print("EPISODIO: %s" % segmento[1])

    else:
        print("TITULO: %s" % element['TITULO'])

    print("GENERO: %s" % element['GENERO'])
    print("INICIO: %s" % element['HORA_INICIO'])
    print("FIN: %s" % element['HORA_FIN'])
    print("DURACION: %i min." % element['DURACION'])

    if element['ESTRENO']:
        print("ESTRENO: Si")
    
    print("URL: %s" % element['URL'])

    # Parsing the HTML content
    page = requests.get(element['URL'])
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

    # Trying to scrap the content info, maybe in a second version
    ''' # Scraping Casting Team
    # Director
    content = soup.find('div', {'class': 'gi lap-one-half'})
    director = content.find('span', {'itemprop': 'name'})
    guionistas = content.findAll('span')
    
    try:
        director_clear = re.search('>(.+?)<', str(director)).group(1)
    except AttributeError:
        director_clear=''

    print("Director: %s" % director_clear)
    
    guionistas = list(guionistas)
    if len(guionistas) > 0:
        guionistas.remove(guionistas[0])
        print(str(guionistas))

    # Casting '''

    print("\n")

#file.close()