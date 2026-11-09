import logging
import requests

"""
    in : ip
    out : location (country) of the ip
"""

URL_TPINFO = 'https://ipinfo.io'

# Nombre maximum d'IP à géolocaliser (limite d'ipinfo sans compte)
MAX_IPS = 100

logger = logging.getLogger(__name__)

# Dictionnaire {ip: pays} pour ne pas chercher deux fois la même IP
cache = {}

# Devient True si ipinfo nous bloque (erreur 429)
blocked = False


def get_location(ip):
    global blocked

    if blocked:
        return None

    try:
        response = requests.get(URL_TPINFO + '/' + ip + '/json', timeout=5)
    except requests.exceptions.RequestException as e:
        logger.error(ip + " : erreur réseau (" + str(e) + ")")
        return None

    if response.status_code == 429:
        logger.error("ipinfo : trop de requêtes (429), géolocalisation arrêtée")
        blocked = True
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

    # 1. Nombre de tentatives par IP
    ip_counts = {}
    for r in records:
        if r['status'] == status:
            ip = r['ip']
            if ip in ip_counts:
                ip_counts[ip] += 1
            else:
                ip_counts[ip] = 1

    # 2. On garde les MAX_IPS IP qui ont le plus de tentatives
    top_ips = sorted(ip_counts, key=ip_counts.get, reverse=True)[:MAX_IPS]

    # 3. Nombre de tentatives par pays
    counts = {}
    for ip in ip_counts:
        if ip in top_ips:
            country = get_country(ip)
        else:
            country = 'Autres'

        if country in counts:
            counts[country] += ip_counts[ip]
        else:
            counts[country] = ip_counts[ip]

    return counts


if __name__ == "__main__":
    print(get_location('31.156.193.220'))
    print(get_country('8.8.8.8'))
    print(get_country('127.0.0.1'))
