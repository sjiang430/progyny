import logging


def init_logging():
    logging.basicConfig(filename='storage/logs/app.log', level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    logging.getLogger().addHandler(ch)

