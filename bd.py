import pandas as pd
import sqlite3 as sq

#Definir las rutas
csv_path = "cleaned_database.csv"
bd_path = "energy_database.db"
sql_query_path = "bd.sql"

#Conectar/crear archivo .db
conn = sq.connect(bd_path)
cursor = conn.cursor()

#Crear tablas
with open(sql_query_path, "r", encoding="utf-8", errors="ignore") as file:
    sql_statements = file.read()
cursor.executescript(sql_statements)

#csv a dataframe
df = pd.read_csv(csv_path)

#Extraer y preparar datos

#Countries
countries = df["Country"].unique().tolist()
countries = [(i,country) for i,country in enumerate(countries)]
countries_query = f"INSERT INTO countries VALUES(?{(',?')*(len(countries[0])-1)})"
cursor.executemany(countries_query,countries)

#Group Technology
renewable_dict = {}
for index, value in enumerate(df["RE or Non-RE"].unique().tolist()):
    renewable_dict[value] = not index
group_technology = [(i,tuple[0],renewable_dict[tuple[1]]) for i, tuple in enumerate(df.groupby("Group Technology").value_counts(["RE or Non-RE"]).index.to_list())]
group_technology_query = f"INSERT INTO group_technology VALUES(?{(',?')*(len(group_technology[0])-1)})"
cursor.executemany(group_technology_query,group_technology)

#Technology
group_technology_dict = {}
for row in cursor.execute("SELECT * FROM group_technology"):
    group_technology_dict[row[1]] = row[0]
technology = [(i,tuple[0],group_technology_dict[tuple[1]])for i, tuple in enumerate(df.groupby("Technology").value_counts(["Group Technology"]).index.to_list())]
technology_query = f"INSERT INTO technology VALUES(?{(',?')*(len(technology[0])-1)})"
cursor.executemany(technology_query,technology)

#Sub-Technology
technology_dict = {}
for row in cursor.execute("SELECT * FROM technology"):
    technology_dict[row[1]] = row[0]
sub_technology = [(i,tuple[0],technology_dict[tuple[1]])for i, tuple in enumerate(df.groupby("Sub-Technology").value_counts(["Technology"]).index.to_list())]
sub_technology_query = f"INSERT INTO sub_technology VALUES(?{(',?')*(len(sub_technology[0])-1)})"
cursor.executemany(sub_technology_query,sub_technology)

#Producer Type
producer_type = [(i,type) for i,type in enumerate(df["Producer Type"].unique().tolist())]
producer_type_query = f"INSERT INTO producer_type VALUES(?,?)"
cursor.executemany(producer_type_query,producer_type)

#Energy Data
df.drop(["Unnamed: 0","RE or Non-RE","Group Technology","Technology"],inplace=True,axis=1)
countries_dict = {}
for row in cursor.execute("SELECT * FROM countries"):
    countries_dict[row[1]]=row[0]

sub_technology_dict = {}
for row in cursor.execute("SELECT * FROM sub_technology"):
    sub_technology_dict[row[1]]=row[0]

producer_type_dict = {}
for row in cursor.execute("SELECT * FROM producer_type"):
    producer_type_dict[row[1]]=row[0]

data = []
for i in range(len(df)):
    row = df.iloc[i].to_list()
    data.append((i, countries_dict[row[0]], sub_technology_dict[row[1]], producer_type_dict[row[2]], int(row[3]), row[4], row[5], row[6], row[7], row[8]))
data_query = f"INSERT INTO energy_data VALUES(?{(',?')*(len(data[0])-1)})"
cursor.executemany(data_query,data)
conn.commit()
conn.close()