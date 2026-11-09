import logging
from pathlib import Path

from ingestion import raw
from processing import extract_tansforme
from serving import dashboard

# Les logs de tous les modules sont enregistrés dans storage/app.log
Path('storage').mkdir(exist_ok=True)

logging.basicConfig(
    filename='storage/app.log',
    level=logging.INFO,
    format='%(asctime)s|%(levelname)s|%(name)s|%(message)s',
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Démarrage du pipeline")

    try:
        data = raw.to_rows('./data')

        if data:
            records = extract_tansforme.extract(data)
            dashboard.build_dashboard(records)
            print("Terminé : graphiques dans output/, logs dans storage/app.log")
        else:
            logger.error("Aucune ligne lue dans ./data")
            print("Aucune ligne lue, voir storage/app.log")

    except Exception as e:
        logger.exception("Erreur inattendue : " + str(e))
        print("Erreur, voir storage/app.log")

    logger.info("Fin du pipeline")