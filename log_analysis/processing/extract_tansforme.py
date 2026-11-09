import logging
import re
"""
    in : list of rows
    out : datetime, ip, user, failed, invalid user for sshd service, success
"""
logger = logging.getLogger(__name__)
pattern = re.compile(r'(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<server>\w+)\s+(?P<service>\w+)\[\d+\]:\s+(?P<message>.+)')
# Pour trouver l'adresse IP dans le message
IP_PATTERN = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
# Pour trouver le nom d'utilisateur : "for root from" ou "Invalid user admin from"
USER_PATTERN = re.compile(r'(for|user) (?P<user>\S*) from')

def classify_event(message):
    
    lowered = message.lower()
    if "accepted password" in lowered or "accepted publickey" in lowered:
        return "Success"
    if "failed password" in lowered:
        return "Failed"
    if "invalid user" in lowered:
        return "Invalid"
    return None

def extract_from_row(row):
    """Analyse une ligne : renvoie un dict, ou None si ce n'est pas une tentative sshd."""
    match = re.search(pattern, row)
    if not match:
        return None

    if match['service'] != 'sshd':
        return None

    message = match['message']
    status = classify_event(message)
    if status is None:
        return None

    ips = IP_PATTERN.findall(message)
    if not ips:
        logger.warning("IP introuvable : " + message)
        return None

    user_match = re.search(USER_PATTERN, message)
    user = ''
    if user_match:
        user = user_match['user']
    if user == '':
        user = '(vide)'

    return {
        'month': match['month'],
        'day': match['day'],
        'time': match['time'],
        'ip': ips[0],
        'user': user,
        'status': status,
    }

def extract(rows):
    """Analyse toutes les lignes et garde seulement les tentatives sshd."""
    records = []
    for row in rows:
        parsed = extract_from_row(row)
        if parsed is not None:
            records.append(parsed)

    logger.info(str(len(records)) + " tentatives sshd extraites")
    return records

def count_by_user(records, status):
    """Compte le nombre de tentatives par utilisateur pour un statut donné."""
    counts = {}
    for r in records:
        if r['status'] == status:
            user = r['user']
            if user in counts:
                counts[user] += 1
            else:
                counts[user] = 1
    return counts

def count_by_ip(records):
    """{ip: {'Success': n, 'Failed': n, 'Invalid': n}}"""
    counts = {}
    for r in records:
        ip = r['ip']
        if ip not in counts:
            counts[ip] = {'Success': 0, 'Failed': 0, 'Invalid': 0}
        counts[ip][r['status']] += 1
    return counts

if __name__ == "__main__":
    from ingestion import raw

    rows = raw.to_rows('./data')
    records = extract(rows)

    print("Tentatives sshd :", len(records))
    print("Succès par utilisateur :", count_by_user(records, 'Success'))
    print("Nombre d'utilisateurs invalides :", len(count_by_user(records, 'Invalid')))
    print("Nombre d'IP différentes :", len(count_by_ip(records)))
    print(records[:3])
