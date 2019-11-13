LOAD DATA
    INFILE '/var/lib/mysql-files/weather-data/temperature_newyork.csv'
    INTO TABLE newyork
    FIELDS TERMINATED BY ';'
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;