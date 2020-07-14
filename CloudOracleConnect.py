import cx_Oracle


# create connection to cloud oracle data base 
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
# create cursor 
cur=conn.cursor()
#create first request
reqst_create = """
CREATE TABLE ville (
    ID_VILLE VARCHAR2(50),
    VILLE_NAME VARCHAR2(100),
    CODE_POSTAL NUMBER (5)
)
"""
# execute request
cur.execute(reqst_create)
print("Table Created")