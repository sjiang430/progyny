TABLES = {
    'quote': (
        "CREATE TABLE `quote` ("
        "  `record_id` int(11) NOT NULL AUTO_INCREMENT, "
        "  `coin_id` varchar(32) NOT NULL, "
        "  `current_price` FLOAT NOT NULL, "
        "  `last_updated` TIMESTAMP NOT NULL, "
        "  PRIMARY KEY (`record_id`), "
        "  CONSTRAINT UNIQUE `unique_quote` (`coin_id`,`last_updated`)"
        ")"),

    'trade_history': (
        "CREATE TABLE `trade` ("
        "  `trade_id` int(11) PRIMARY KEY AUTO_INCREMENT,"
        "  `coin_id` varchar(32) NOT NULL,"
        "  `price` FLOAT NOT NULL,"
        "  `amount` int(11) NOT NULL,"
        "  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
        ")")
}


