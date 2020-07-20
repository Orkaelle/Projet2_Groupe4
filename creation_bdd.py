import cx_Oracle


# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)

cur=conn.cursor()


# Tables creation

creation_table_city = """
    CREATE TABLE city (
        id_city INTEGER PRIMARY KEY,
        city_name TEXT
    );
"""

creation_table_departement = """
    CREATE TABLE departement (
        id_departement INTEGER(2) PRIMARY KEY,
        dept_name TEXT,
        city_id_pref INTEGER,
        FOREIGN KEY (city_id_pref) REFERENCES city (id_city)
    );
"""

creation_table_station = """
    CREATE TABLE station (
        id_station INTEGER PRIMARY KEY,
        station_name TEXT,
        station_city TEXT,
        lon REAL,
        lat REAL, 
        FOREIGN KEY (station_city) REFERENCES city(city_name),
    );
"""

creation_table_route = """
    CREATE TABLE route (
        id_route INTEGER AUTOINCREMENT PRIMARY KEY,
        departure_city TEXT,
        arrival_city TEXT,
        FOREIGN KEY (departure_city) REFERENCES departement(prefecture),
        FOREIGN KEY (arrival_city) REFERENCES departement(prefecture)
    );
"""

creation_table_trip = """
    CREATE TABLE trip (
        id_trip INTEGER AUTOINCREMENT PRIMARY KEY,
        trip_route INTEGER,
        departure_station TEXT,
        arrival_station TEXT,
        departure_datetime DATETIME,
        arrival_datetime DATETIME,
        duration REAL,
        co2_emission INTEGER,
        FOREIGN KEY (trip_route) REFERENCES route(id_route),
        FOREIGN KEY (departure_station) REFERENCES station(station_name),
        FOREIGN KEY (arrival_station) REFERENCES station(station_name),
    );
"""

