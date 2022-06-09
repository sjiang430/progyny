"""Crypto Interview Assessment Module."""
import time

from crypto_trader import trade
from dotenv import find_dotenv, load_dotenv
from logger import init_logging
from db import init_tables


load_dotenv(find_dotenv(raise_error_if_not_found=True))
init_logging()
init_tables()

# Start Here
while 1:
    trade()
    time.sleep(60)



