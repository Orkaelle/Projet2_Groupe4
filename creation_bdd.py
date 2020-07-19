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
        
conn.commit()
reqst.close()
cur.close()
conn.close()
print("Data Base Installed")

