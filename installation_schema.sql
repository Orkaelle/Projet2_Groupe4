    DROP SEQUENCE ID_ROUTE;
	DROP SEQUENCE ID_TRIP;
    CREATE SEQUENCE ID_ROUTE
    START WITH 1
    INCREMENT BY 1
    MAXVALUE 9999
    NOCYCLE
    NOCACHE
    NOORDER;
	CREATE SEQUENCE ID_TRIP
    START WITH 1
    INCREMENT BY 1
    MAXVALUE 999999
    NOCYCLE
    NOCACHE
    NOORDER;
    ALTER TABLE CITY DROP PRIMARY KEY CASCADE;
    DROP TABLE CITY CASCADE CONSTRAINTS;
    CREATE TABLE CITY (
        ID_CITY NUMBER (5),
        CITY_NAME VARCHAR2(200),
        CONSTRAINT INSEE_CITY_PK PRIMARY KEY (ID_CITY)
    );
    ALTER TABLE DEPARTEMENT DROP PRIMARY KEY CASCADE;
    DROP TABLE DEPARTEMENT CASCADE CONSTRAINTS;
    CREATE TABLE DEPARTEMENT (
        ID_DEPARTEMENT NUMBER (3),
        DEPT_NAME VARCHAR2 (200),
        CITY_ID_PREF NUMBER (5),
        CONSTRAINT ID_DEPARTEMENT_PK PRIMARY KEY (ID_DEPARTEMENT),
        CONSTRAINT CITY_ID_FK FOREIGN KEY(CITY_ID_PREF)  REFERENCES CITY (ID_CITY) 
    );
    ALTER TABLE STATION DROP PRIMARY KEY CASCADE;
    DROP TABLE STATION CASCADE CONSTRAINTS;
    CREATE TABLE STATION (
        ID_STATION NUMBER (8),
        CODE_LINE NUMBER (8),
        STATION_NAME VARCHAR2 (200),
        STATION_COMMUNE VARCHAR2 (200),
        LON NUMBER (17,15),
        LAT NUMBER (17,15),
        CITY_ID_PREF NUMBER (5),
        CONSTRAINT ID_STATION_PK PRIMARY KEY (ID_STATION, CODE_LINE),
        CONSTRAINT CITY_ID_ST_FK FOREIGN KEY(CITY_ID_PREF)  REFERENCES CITY (ID_CITY) 
    );
    ALTER TABLE ROUTE DROP PRIMARY KEY CASCADE;
    DROP TABLE ROUTE CASCADE CONSTRAINTS;
    CREATE TABLE ROUTE (
        ID_ROUTE NUMBER (5),
        DEPART_CITY VARCHAR2 (200),
        ARRIVAL_CITY VARCHAR2 (200),
        CONSTRAINT ID_ROUTE_PK PRIMARY KEY (ID_ROUTE)
        
    );
    ALTER TABLE TRIP DROP PRIMARY KEY CASCADE;
    DROP TABLE TRIP CASCADE CONSTRAINTS; 
    CREATE TABLE TRIP (
        ID_TRIP NUMBER (6),
        DEPART_STATION NUMBER (8),
        ARRIVAL_STATION NUMBER (8),
        DEPARTURE_DATETIME DATE,
        ARRIVAL_DATETIME DATE,
        DURATION NUMBER (10),
        CO2 NUMBER (10,4),
        TYPE_TRIP VARCHAR2(2),
        LINE_CODE NUMBER (8), 
        CONSTRAINT ID_TRIP_PK PRIMARY KEY (ID_TRIP),
        CONSTRAINT STATION_ID_FK FOREIGN KEY(DEPART_STATION, LINE_CODE)  REFERENCES STATION (ID_STATION, CODE_LINE),
        CONSTRAINT STATION_FK FOREIGN KEY(ARRIVAL_STATION, LINE_CODE)  REFERENCES STATION (ID_STATION, CODE_LINE)

    );