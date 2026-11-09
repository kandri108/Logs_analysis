import logging
import requests
"""
    in : ip
    out : location (country) of the ip
"""

URL_TPINFO = 'https://ipinfo.io'

logger = logging.getLogger(__name__)

# Dictionnaire {ip: pays} pour ne pas chercher deux fois la même IP
cache = {}

def get_location(ip):
    try:
        response = requests.get(URL_TPINFO + '/' + ip + '/json', timeout=5)
    except requests.exceptions.RequestException as e:
        logger.error(ip + " : erreur réseau (" + str(e) + ")")
        return None

    if response.status_code != 200:
        logger.error(ip + " : réponse HTTP " + str(response.status_code))
        return None

    return response.json()

def get_country(ip):
    if ip in cache:
        return cache[ip]

    country = 'Inconnu'

    if ip == '127.0.0.1':
        country = 'Local'
    else:
        data = get_location(ip)
        if data and 'country' in data:
            country = data['country']

    cache[ip] = country
    return country

def count_by_country(records, status):
    """Compte le nombre de tentatives par pays pour un statut donné."""
    counts = {}
    for r in records:
        if r['status'] == status:
            country = get_country(r['ip'])
            if country in counts:
                counts[country] += 1
            else:
                counts[country] = 1
    return counts

if __name__ == "__main__":
    print(get_location('31.156.193.220'))
    print(get_country('8.8.8.8'))
    print(get_country('127.0.0.1'))
    print(get_country('192.168.1.10'))
