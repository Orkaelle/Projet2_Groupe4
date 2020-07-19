    DROP SEQUENCE id_route;
	DROP SEQUENCE id_trip;
    CREATE SEQUENCE id_route
    START WITH 1
    INCREMENT BY 1
    MAXVALUE 9999
    NOCYCLE
    NOCACHE
    NOORDER;
	CREATE SEQUENCE id_trip
    START WITH 1
    INCREMENT BY 1
    MAXVALUE 999999
    NOCYCLE
    NOCACHE
    NOORDER;
    ALTER TABLE city DROP PRIMARY KEY CASCADE;
    DROP TABLE city CASCADE CONSTRAINTS;
    CREATE TABLE city (
        id_city NUMBER (5),
        city_name VARCHAR2(200),
        CONSTRAINT insee_city_PK PRIMARY KEY (id_city)
    );
    ALTER TABLE departement DROP PRIMARY KEY CASCADE;
    DROP TABLE departement CASCADE CONSTRAINTS;
    CREATE TABLE departement (
        id_departement NUMBER (2),
        dept_name VARCHAR2 (200),
        city_id_pref NUMBER (5),
        CONSTRAINT id_departement_PK PRIMARY KEY (id_departement),
        CONSTRAINT city_id_FK FOREIGN KEY(city_id_pref)  REFERENCES city (id_city) 
    );
    ALTER TABLE station DROP PRIMARY KEY CASCADE;
    DROP TABLE station CASCADE CONSTRAINTS;
    CREATE TABLE station (
        id_station NUMBER (8),
        station_name VARCHAR2 (200),
        lon NUMBER (17,15),
        lat NUMBER (17,15),
        city_id_pref NUMBER (5),
        CONSTRAINT id_station_PK PRIMARY KEY (id_station),
        CONSTRAINT city_id_st_FK FOREIGN KEY(city_id_pref)  REFERENCES city (id_city) 
    );
    ALTER TABLE route DROP PRIMARY KEY CASCADE;
    DROP TABLE route CASCADE CONSTRAINTS;
    CREATE TABLE route (
        id_route NUMBER (5),
        depart_city VARCHAR2 (200),
        arrival_city VARCHAR2 (200),
        CONSTRAINT id_route_PK PRIMARY KEY (id_route)
        
    );
    ALTER TABLE trip DROP PRIMARY KEY CASCADE;
    DROP TABLE trip CASCADE CONSTRAINTS; 
    CREATE TABLE trip (
        id_trip NUMBER (6),
        departure_datetime DATE,
        arrival_datetime DATE,
        duration NUMBER (10),
        co2 NUMBER (10,4),
        depart_station NUMBER (8),
        arrival_station NUMBER (8),
        route_id NUMBER (5),
        CONSTRAINT id_trip_PK PRIMARY KEY (id_trip),
        CONSTRAINT route_id_FK FOREIGN KEY(route_id)  REFERENCES route (id_route),
        CONSTRAINT station_id_FK FOREIGN KEY(depart_station)  REFERENCES station (id_station),
        CONSTRAINT station_FK FOREIGN KEY(arrival_station)  REFERENCES station (id_station)

    );