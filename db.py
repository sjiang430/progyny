import mysql.connector
import logging

from datetime import datetime
from mysql.connector import errorcode
from schema import TABLES
from os import getenv


def save_quote(quotes):
    cnx = _get_connection()
    cursor = cnx.cursor()

    try:
        insert_quote_query = "INSERT IGNORE INTO quote (coin_id, current_price, last_updated) VALUES (%s, %s, %s)"
        data = []
        for q in quotes:
            data.append((q['id'], q['current_price'], datetime.strptime(q['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ")))

        cursor.executemany(insert_quote_query, data)
        cnx.commit()
    except mysql.connector.Error as err:
        logging.fatal('error saving quote %s', err.msg)

    cursor.close()
    cnx.close()


def save_trade(record, amount):
    cnx = _get_connection()
    cursor = cnx.cursor()

    try:
        insert_coin_query = "INSERT INTO trade (coin_id, price, amount) VALUES (%s, %s, %s)"
        data = (record['id'], record['current_price'], amount)
        cursor.execute(insert_coin_query, data)
        cnx.commit()
    except mysql.connector.Error as err:
        logging.fatal('error saving trade %s', err.msg)


def get_trade_history(coin_id):
    cnx = _get_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM trade where coin_id = %s", [coin_id])
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return result


def init_tables():
    cnx = _get_connection()
    cursor = cnx.cursor()
    for table_name in TABLES:
        table_description = TABLES[table_name]

        try:
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno != errorcode.ER_TABLE_EXISTS_ERROR:
                logging.fatal('failed to create table %s %s', table_name, err.msg)

    cursor.close()
    cnx.close()


def _get_connection():
    cnx = mysql.connector.connect(
        user=getenv("DB_USERNAME"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST"),
        database=getenv("DB_DATABASE"),
        port=int(getenv("DB_PORT")),
    )
    return cnx


