import cx_Oracle


# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur=conn.cursor()
reqst = open('installation_schema.sql', 'r', encoding='utf-8')
full_reqst = reqst.read()
queries = full_reqst.split(';')
for query in queries:
    try:
        cur.execute(query)
    except Exception as error:
        print(error)
        
#   print(query)
conn.commit()
reqst.close()
cur.close()
conn.close()
print("Data Base Installed")

# # Sequence creation
# creation_sequence_route = """
#     CREATE SEQUENCE id_route
#     START WITH 1
#     INCREMENT BY 1
#     MAXVALUE 9999
#     NOCYCLE
#     NOCACHE
#     NOORDER
# """
# creation_sequence_trip = """
#     CREATE SEQUENCE id_trip
#     START WITH 1
#     INCREMENT BY 1
#     MAXVALUE 999999
#     NOCYCLE
#     NOCACHE
#     NOORDER
# """
# # Tables creation
# creation_table_city = """
#    CREATE TABLE city (
#         id_city NUMBER (5),
#         city_name VARCHAR2(200),
#         CONSTRAINT insee_city_PK PRIMARY KEY (id_city)
#     )
# """

# creation_table_departement = """
#     CREATE TABLE departement (
#         id_departement NUMBER (2),
#         dept_name VARCHAR2 (200),
#         city_id_pref NUMBER (5),
#         CONSTRAINT id_departement_PK PRIMARY KEY (id_departement),
#         CONSTRAINT city_id_FK FOREIGN KEY(city_id_pref)  REFERENCES city (id_city) 
#     )
# """

# creation_table_station = """
#     CREATE TABLE station (
#         id_station NUMBER (8),
#         station_name VARCHAR2 (200),
#         lon NUMBER (17,15),
#         lat NUMBER (17,15),
#         city_id_pref NUMBER (5),
#         CONSTRAINT id_station_PK PRIMARY KEY (id_station),
#         CONSTRAINT city_id_st_FK FOREIGN KEY(city_id_pref)  REFERENCES city (id_city) 
#     )
# """

# creation_table_route = """
#     CREATE TABLE route (
#         id_route NUMBER (5),
#         depart_city VARCHAR2 (200),
#         arrival_city VARCHAR2 (200),
#         CONSTRAINT id_route_PK PRIMARY KEY (id_route)
        
#     )
# """

# creation_table_trip = """
#     CREATE TABLE trip (
#         id_trip NUMBER (6),
#         departure_datetime DATE,
#         arrival_datetime DATE,
#         duration NUMBER (10),
#         co2 NUMBER (10,4),
#         depart_station NUMBER (8),
#         arrival_station NUMBER (8),
#         route_id NUMBER (5),
#         CONSTRAINT id_trip_PK PRIMARY KEY (id_trip),
#         CONSTRAINT route_id_FK FOREIGN KEY(route_id)  REFERENCES route (id_route),
#         CONSTRAINT station_id_FK FOREIGN KEY(depart_station)  REFERENCES station (id_station),
#         CONSTRAINT station_FK FOREIGN KEY(arrival_station)  REFERENCES station (id_station)

#     )
# """
# drop_sequence = """
#     DROP SEQUENCE id_route
# """
# create_sequence ="""
#     CREATE SEQUENCE id_route
#     START WITH 1
#     INCREMENT BY 1
#     MAXVALUE 9999
#     NOCYCLE
#     NOCACHE
#     NOORDER
# """
# alter_table_city = """
#     ALTER TABLE city DROP PRIMARY KEY CASCADE
# """

# drop_table_city ="""
#     DROP TABLE city CASCADE CONSTRAINTS
# """
# cur.execute(creation_table_city)
# print("Table CITY created")
# cur.execute(creation_table_departement)
# print("Table DEPARTEMENT created")
# cur.execute(creation_table_station)
# print("Table STATION created")
# cur.execute(creation_sequence_route)
# print("Sequence ROUTE created")
# cur.execute(creation_sequence_trip)
# print("Sequence TRIP created")
# cur.execute(creation_table_route)
# print("Table ROUTE created")
# cur.execute(creation_table_trip)
# print("Table TRIP created")
# cur.execute(drop_sequence)
# print("Sequence id_route Droped")
# cur.execute(create_sequence)
# print("Sequence id_route created")
# cur.execute(alter_table_city)
# print("Table CITY altred")
# cur.execute(drop_table_city)
# print("Table CITY droped")
