#!/usr/bin/env python
# -*- coding: utf-8 -*-
#        **
#       //\\
# o==[=//==\\====>
#     **    **
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Autor:_<<Gabriel Oliveros>>_
#
# Rasca la web de worldometer Coronavirus y muestra las cifras por país.
# El resultado lo guarda en un archivo '.csv'
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import requests,csv,re,string,time
from bs4 import BeautifulSoup
from os import remove

def traducir():
    '''
    Traduce al Castellano cada uno de los países de la página excepto los barcos
    '''
    global pais
    for clave,valor in dicc.items():
        if clave==pais:
            pais=valor
    return pais

def remove_punctuation (text):
    '''
    Elimina las comas y otros signos (+) de cada cifra recogida
    '''
    return re.sub('[%s]' % re.escape(string.punctuation), '', text)


# En caso de existir, borra el archivo previo donde se guardarán los datos
try:
    remove('covid19.csv')
except FileNotFoundError:
    pass

print('Bienvenido(a), a continuación se procederá al escaneo \n')


header= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
url= 'http://www.worldometers.info/coronavirus/'
r= requests.get(url,headers=header).content
  
print('Escaneando Worldometer Covid-19')
print('Por favor espere...\n')

soup=BeautifulSoup(r,'lxml')
tabla= soup.find(id='main_table_countries_today').find('tbody')

# Listado de países según idioma. Se usa para la posterior traducción
ingles=['USA','Spain','Italy','France','Germany','UK','Iran','Turkey','Belgium',
        'Brazil','Canada','Netherlands','Switzerland','Russia','Portugal',
        'Austria','Ireland','Israel','India','Sweden','Peru','S. Korea','Japan',
        'Chile','Ecuador','Poland','Romania','Norway','Denmark','Australia',
        'Pakistan','Czechia','Saudi Arabia','Mexico','Philippines','UAE',
        'Indonesia','Malaysia','Serbia','Ukraine','Panama','Belarus','Qatar',
        'Singapore','Dominican Republic','Luxembourg','Finland','Colombia',
        'Thailand','Argentina','South Africa','Egypt','Greece','Algeria',
        'Moldova','Morocco','Croatia','Iceland','Bahrain','Hungary','Iraq',
        'Kuwait','New Zealand','Estonia','Uzbekistan','Kazakhstan',
        'Azerbaijan','Slovenia','Bangladesh','Armenia','Bosnia and Herzegovina',
        'Lithuania','Hong Kong','North Macedonia','Oman','Slovakia','Cameroon',
        'Cuba','Afghanistan','Tunisia','Bulgaria','Cyprus','Diamond Princess',
        'Andorra','Latvia','Lebanon','Ivory Coast','Ghana','Costa Rica','Niger',
        'Burkina Faso','Albania','Uruguay','Kyrgyzstan','Channel Islands',
        'Bolivia','Djibouti','Honduras','Nigeria','Guinea','Jordan','Malta',
        'Taiwan','San Marino','Réunion','Palestine','Mauritius','Senegal',
        'Georgia','Montenegro','Vietnam','Isle of Man','DRC','Sri Lanka','Kenya',
        'Mayotte','Venezuela','Guatemala','Faeroe Islands','Paraguay','El Salvador',
        'Martinique','Mali','Guadeloupe','Brunei','Rwanda','Gibraltar','Jamaica',
        'Cambodia','Congo','Trinidad and Tobago','Madagascar','Monaco','Aruba',
        'Tanzania','French Guiana','Ethiopia','Bermuda','Togo','Somalia','Gabon',
        'Liechtenstein','Barbados','Myanmar','Cayman Islands','Liberia',
        'Cabo Verde','Equatorial Guinea','Zambia','Libya','Macao','Guinea-Bissau',
        'Haiti','Saint Martin','Benin','Eritrea','Syria','Sudan','Mongolia',
        'Mozambique','Antigua and Barbuda','Zimbabwe','Chad','Maldives','Angola',
        'Laos','Belize','New Caledonia','Malawi','Nepal','Dominica','Fiji','Namibia',
        'Saint Lucia','Eswatini','Curaçao','Grenada','Saint Kitts and Nevis',
        'Botswana','Sierra Leone','CAR','St. Vincent Grenadines','Falkland Islands',
        'Greenland','Montserrat','Seychelles','Suriname','Turks and Caicos','MS Zaandam',
        'Gambia','Nicaragua','Vatican City','Timor-Leste','Mauritania','St. Barth',
        'Western Sahara','Burundi','Bhutan','Sao Tome and Principe','South Sudan',
        'Anguilla','British Virgin Islands','Caribbean Netherlands','Papua New Guinea',
        'Saint Pierre Miquelon','Yemen','China','Guyana','French Polynesia','Uganda',
        'Bahamas','Tuvalu', 'Wallis & Futuna', 'Nauru','Niue','Tokelau','Saint Helena','Holy See']
castellano=['Estados Unidos','España','Italia','Francia','Alemania','Reino Unido',
         'Irán','Tuquía','Bélgica','Brasil','Canadá','Países Bajos','Suiza','Rusia',
         'Portugal','Austria','Irlanda','Israel','India','Suecia','Perú','Corea del Sur',
         'Japón','Chile','Ecuador','Polonia','Rumania','Noruega','Dinamarca','Australia',
         'Pakistán','Chequia','Arabia Saudita','México','Filipinas',
         'Emiratos Árabes Unidos','Indonesia','Malasia','Serbia','Ucrania','Panamá',
         'Bielorrusia','Katar','Singapur','República Dominicana','Luxemburgo','Finlandia',
         'Colombia','Tailandia','Argentina','Sudáfrica','Egipto','Grecia','Argelia',
         'Moldavia','Marruecos','Croacia','Islandia','Bahrein','Hungría','Irak','Kuwait',
         'Nueva Zelanda','Estonia','Uzbekistán','Kazajistán','Azerbaiyán','Eslovenia',
         'Bangladesh','Armenia','Bosnia y Herzegovina','Lituania','Hong Kong',
         'Macedonia del norte','Omán','Eslovaquia','Camerún','Cuba','Afganistán','Túnez',
         'Bulgaria','Chipre','Diamond Princess','Andorra','Letonia','Líbano',
         'Costa de Marfil','Ghana','Costa Rica','Níger','Burkina Faso','Albania','Uruguay',
         'Kirguistán','Islas del Canal','Bolivia','Djibouti','Honduras','Nigeria','Guinea',
         'Jordán','Malta','Taiwán','San Marino','Reunión','Palestina','Mauricio','Senegal',
         'Georgia','Montenegro','Vietnam','Isla del hombre','Rep. Democrática del Congo',
         'Sri Lanka','Kenia','Mayotte','Venezuela','Guatemala','Islas Feroe','Paraguay',
         'El Salvador','Martinica','Mali','Guadalupe','Brunei','Ruanda','Gibraltar',
         'Jamaica','Camboya','Congo','Trinidad y Tobago','Madagascar','Mónaco','Aruba',
         'Tanzania','Guayana Francesa','Etiopía','islas Bermudas','Togo','Somalia','Gabón',
         'Liechtenstein','Barbados','Myanmar','Islas Caimán','Liberia','Cabo Verde',
         'Guinea Ecuatorial','Zambia','Libia','Macao','Guinea-Bissau','Haití',
         'Saint Martin','Benin','Eritrea','Siria','Sudán','Mongolia','Mozambique',
         'Antigua y Barbuda','Zimbabue','Chad','Maldivas','Angola','Laos','Belice',
         'Nueva Caledonia','Malawi','Nepal','Dominica','Fiyi','Namibia','Santa Lucía',
         'Eswatini','Curazao','Granada','San Cristóbal y Nieves','Botsuana','Sierra Leona',
         'Rep. Centroafricana','San Vicente Granadinas','Islas Malvinas','Groenlandia','Montserrat',
         'Seychelles','Surinam','Turcas y Caicos','MS Zaandam','Gambia','Nicaragua',
         'Ciudad del Vaticano','Timor-Leste','Mauritania','San Bartolomé','Sahara Occidental',
         'Burundi','Bután','Santo Tomé y Príncipe','Sudán del Sur','Anguila',
         'Islas Vírgenes Británicas','Caribe neerlandés','Papúa Nueva Guinea',
         'San Pedro Miquelón','Yemen','China','Guyana','Polinesia Francesa','Uganda','Vista Santa']

dicc=dict(zip(ingles,castellano))

# Clasificadores por continente
africa=['South Africa','Ivory Coast','Burkina Faso','Equatorial Guinea','Cabo Verde',
        'Guinea-Bissau','Sierra Leone','Western Sahara','Sao Tome and Principe','South Sudan',
        'Egypt','Morocco','Algeria','Ghana','Cameroon','Tunisia','Djibouti','Niger','Nigeria',
        'Guinea','Réunion','Senegal','Mauritius','DRC','Mayotte','Kenya','Mali','Tanzania',
        'Somalia','Rwanda','Congo','Madagascar','Gabon','Ethiopia','Liberia','Togo','Sudan',
        'Zambia','Uganda','Libya','Eritrea','Mozambique','Benin','Chad','Zimbabwe','Angola',
        'Eswatini','Botswana','Malawi','Namibia','CAR','Seychelles','Gambia','Mauritania',
        'Burundi','Saint Helena' ]        
america=['Trinidad and Tobago','Sint Maarten','Cayman Islands','Saint Martin',
         'Antigua and Barbuda','Saint Lucia','Saint Kitts and Nevis','St. Vincent Grenadines',
         'Turks and Caicos','St. Barth','Caribbean Netherlands','British Virgin Islands',
         'Saint Pierre & Miquelon','French Guiana','Falkland Islands','Dominican Republic',
         'Costa Rica','El Salvador','USA','Canada','Mexico','Panama','Cuba','Honduras',
         'Guatemala','Jamaica','Martinique','Guadeloupe','Aruba','Bermuda','Barbados','Bahamas',
         'Haiti','Belize','Dominica','Curaçao','Grenada','Greenland','Montserrat','Nicaragua',
         'Anguilla','Brazil','Peru','Chile','Ecuador','Colombia','Argentina','Bolivia','Uruguay',
         'Venezuela','Paraguay','Suriname','Guyana', 'Saint Barthelemy']
asia=['Timor-Leste','S. Korea','Saudi Arabia','Hong Kong', 'Sri Lanka','Turkey','China','Iran',
      'India','Israel','Japan','Pakistan','UAE','Singapore','Indonesia','Philippines','Qatar',
      'MalaysiaThailand','Bangladesh','Kuwait','Bahrain','Kazakhstan','Uzbekistan','Iraq',
      'Azerbaijan','Armenia','Oman','Afghanistan','Cyprus','Lebanon','Kyrgyzstan','Palestine',
      'Taiwan','Jordan','Georgia','Vietnam','Brunei','Cambodia','Myanmar','Maldives','Macao',
      'Syria','Mongolia','Nepal','Laos','Bhutan','Yemen']
europa=['Vatican City','Bosnia and Herzegovina','North Macedonia','Channel Islands','San Marino',
        'Isle of Man','Faeroe Islands''Norway','Czechia','Spain','Italy','France','Germany','UK',
        'Russia','Belgium','Netherlands','Switzerland','Portugal','Ireland','Austria','Sweden',
        'Poland','Romania','Denmark','Serbia','Ukraine','Belarus','Finland','Luxembourg','Moldova',
        'Greece','Hungary','Croatia','Iceland','Estonia','Slovenia','Lithuania','Slovakia',
        'Bulgaria','Latvia','Andorra','Albania','Malta','Montenegro','Gibraltar','Monaco',
        'Liechtenstein','Holy See']
oceania=['Australia','New Zealand','French Polynesia','New Caledonia','Fiji','Papua New Guinea',
         'Tuvalu', 'Wallis & Futuna', 'Nauru','Niue','Tokelau']
barco=['Diamond Princess','MS Zaandam'] #Casos que se encuentran en barcos


continente=''
pais=''
casos=''
recuperados=''
fallecidos=''
activos=''
casos_millon=''
muertes_millon=''
pruebas=''
poblacion=''

# Creación del archivo '.csv' y llenado de la tabla
with open('covid19.csv','w',newline='') as csv_file:
    writer= csv.writer(csv_file)
    writer.writerow(['País','Continente','Contagiados','Recuperados','Fallecidos',
                     'Activos','Casos/millónHab','Muertes/millónHab','Pruebas',
                     'Población'])
    for fila in tabla.find_all('tr'):
        nroCelda=0
        for celda in fila.find_all('td'):
            if nroCelda==1:
                pais=celda.text
                if pais in africa:
                    continente='África'
                if pais in america:
                    continente='América'
                if pais in asia:
                    continente='Asia'
                if pais in europa:
                    continente='Europa'
                if pais in oceania:
                    continente='Oceanía'
                if pais in barco:
                    continente='Barco'
                traducir()
            if nroCelda==2:
                casos=remove_punctuation(celda.text)
            if nroCelda==4:
                fallecidos=remove_punctuation(celda.text)
            if nroCelda==6:
                recuperados=remove_punctuation(celda.text)
            if nroCelda==7:
                activos=remove_punctuation(celda.text)
            if nroCelda==9:
                casos_millon=remove_punctuation(celda.text)
            if nroCelda==10:
                muertes_millon=remove_punctuation(celda.text)
            if nroCelda==12:
                pruebas=remove_punctuation(celda.text)
            if nroCelda==14:
                poblacion=remove_punctuation(celda.text)
            nroCelda+=1
        writer.writerow([pais,continente,casos,recuperados,fallecidos,activos,
                         casos_millon,muertes_millon,pruebas,poblacion])
        # NOTA: writer no permite colocar el continente antes que país.
        # De hacerlo así los datos quedarán truncados.

print('Escaneo completado.')
print('El archivo está listo para ser utilizado: "covid19.csv"','\n')
