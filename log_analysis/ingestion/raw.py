"""
Read from data all files
in: data [directory]
out: list of rows
"""

import gzip
import logging
import os

logger = logging.getLogger(__name__)


def to_rows(path: str):

    rows = []

    try:
        files = sorted(os.listdir(path))

    except FileNotFoundError:
        logger.error(path + " : dossier introuvable")
        return rows

    except PermissionError:
        logger.error(path + " : permission refusée")
        return rows

    for file in files:

        file_path = path + '/' + file

        # On ignore les dossiers (par exemple auth.tar)
        if not os.path.isfile(file_path):
            continue

        try:
            # Un fichier qui finit par .gz est compressé : on l'ouvre avec gzip
            if file.endswith('.gz'):
                with gzip.open(file_path, mode='rt', encoding='utf-8', errors='replace') as f:
                    lines = f.readlines()
            else:
                with open(file_path, encoding='utf-8', errors='replace') as f:
                    lines = f.readlines()

            rows.extend(lines)
            logger.info(file + " : " + str(len(lines)) + " lignes lues")

        except PermissionError:
            logger.error(file + " : permission refusée")

        except gzip.BadGzipFile:
            logger.error(file + " : fichier gzip corrompu")

        except EOFError:
            logger.error(file + " : fichier gzip incomplet")

        except OSError as e:
            logger.error(file + " : erreur de lecture (" + str(e) + ")")

    return rows


if __name__ == '__main__':
    data = to_rows('./data')

    if data:
        print(len(data))
        print(data[:10])