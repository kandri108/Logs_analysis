import gzip
import logging
import os
from pathlib import Path

"""
Read from data all files
in: data [directory]
out: list of rows
"""

logger = logging.getLogger(__name__)


def is_gzip(file_path):
    # Un fichier gzip commence toujours par les octets 1f 8b
    with open(file_path, 'rb') as f:
        return f.read(2) == b'\x1f\x8b'


def to_rows(path: str):

    data_dir = Path(path)
    rows = []

    try:
        files = sorted(os.listdir(data_dir))

    except FileNotFoundError:
        logger.error(path + " : dossier introuvable")
        return rows

    except PermissionError:
        logger.error(path + " : permission refusée")
        return rows

    for file in files:

        file_path = path + '/' + file

        if not os.path.isfile(file_path):
            continue

        try:
            if is_gzip(file_path):
                f = gzip.open(file_path, mode='rt', errors='replace')
            else:
                f = open(file_path, errors='replace')

            with f:
                lines = f.readlines()

            rows.extend(lines)
            logger.info(file + " : " + str(len(lines)) + " lignes lues")

        except PermissionError:
            logger.error(file + " : permission refusée")

        except gzip.BadGzipFile:
            logger.error(file + " : fichier gzip corrompu")

        except OSError as e:
            logger.error(file + " : erreur de lecture (" + str(e) + ")")

    return rows


if __name__ == '__main__':
    data = to_rows('./data')

    if data:
        print(len(data))
        print(data[:10])