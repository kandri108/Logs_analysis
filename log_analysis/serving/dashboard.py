"""
    in : list of records (from extract_tansforme.extract)
    out : 3 graphs (PNG) in output/
"""

import logging
from pathlib import Path
import matplotlib.pyplot as plt
from processing import extract_tansforme, geo_location

logger = logging.getLogger(__name__)


def draw_bar(counts, title, xlabel, ylabel, file_name):
    # On garde les 10 plus grands nombres
    pairs = []
    for name in counts:
        pairs.append((counts[name], name))
    pairs.sort(reverse=True)

    names = []
    values = []
    for pair in pairs[:10]:
        names.append(pair[1])
        values.append(pair[0])

    plt.figure(figsize=(10, 6))
    plt.bar(names, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

    try:
        plt.savefig('output/' + file_name)
    except OSError as e:
        logger.error(file_name + " : erreur d'enregistrement (" + str(e) + ")")

    plt.close()


def build_dashboard(records):
    Path('output').mkdir(exist_ok=True)

    failed_by_country = geo_location.count_by_country(records, 'Failed')
    draw_bar(failed_by_country, 'Tentatives échouées par pays',
             'Pays', 'Nombre de tentatives', 'failed_by_country.png')

    success_by_user = extract_tansforme.count_by_user(records, 'Success')
    draw_bar(success_by_user, 'Connexions réussies par utilisateur',
             'Utilisateur', 'Nombre de connexions', 'success_by_user.png')

    invalid_by_user = extract_tansforme.count_by_user(records, 'Invalid')
    draw_bar(invalid_by_user, 'Tentatives avec Invalid user',
             'Utilisateur', 'Nombre de tentatives', 'invalid_users.png')


if __name__ == "__main__":
    from ingestion import raw
    rows = raw.to_rows('./data')
    records = extract_tansforme.extract(rows)
    build_dashboard(records)
    print("Graphiques enregistrés dans le dossier output/")