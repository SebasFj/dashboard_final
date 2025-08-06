import pandas as pd
import numpy as np
import sqlite3

def get_countries_names():
    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    c_query = "SELECT name FROM countries;"
    cur.execute(c_query)
    countries = pd.DataFrame(cur.fetchall())
    countries.columns = [i[0] for i in cur.description]

    conn.close()
    return countries

def get_non_renewable_data_countries(year, data_col):
    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = f"""
    SELECT c.name, SUM(ed.{data_col}) AS total_non_renewable
    FROM energy_data ed
    INNER JOIN countries c ON ed.country_id = c.country_id
    WHERE ed.sub_tech_id IN
    (
    SELECT st.sub_technology_id
    FROM sub_technology st
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = FALSE
    )
    AND ed.year = {year}
    GROUP BY c.country_id
    """
    cur.execute(query)
    non_renewables = pd.DataFrame(cur.fetchall())
    non_renewables.columns = [i[0] for i in cur.description]
    conn.close()
    return non_renewables

def get_renewable_data_countries(year, data_col):
    
    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = f"""
    SELECT c.name, SUM(ed.{data_col}) AS total_renewable
    FROM energy_data ed
    INNER JOIN countries c ON ed.country_id = c.country_id
    WHERE ed.sub_tech_id IN
    (
    SELECT st.sub_technology_id
    FROM sub_technology st
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = TRUE
    )
    AND ed.year = {year}
    GROUP BY c.country_id
    """

    print(query)
    cur.execute(query)
    renewables = pd.DataFrame(cur.fetchall())
    renewables.columns = [i[0] for i in cur.description]
    conn.close()
    return renewables
    

def renewable_use_countries(year):
    
    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    query = f"""
    SELECT c.name, SUM(ed.electricity_generation_gwh) AS total_renewable_gwh
    FROM energy_data ed
    INNER JOIN countries c ON ed.country_id = c.country_id
    WHERE ed.sub_tech_id IN
    (
    SELECT st.sub_technology_id
    FROM sub_technology st
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = TRUE
    )
    AND ed.year = {year}
    GROUP BY c.country_id
    """
    cur.execute(query)
    renewables = pd.DataFrame(cur.fetchall())
    renewables.columns = [i[0] for i in cur.description]
    conn.close()
    return renewables

def non_renewables_use_countries(year):

    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = f"""
    SELECT c.name, SUM(ed.electricity_generation_gwh) AS total_non_renewable_gwh
    FROM energy_data ed
    INNER JOIN countries c ON ed.country_id = c.country_id
    WHERE ed.sub_tech_id IN
    (
    SELECT st.sub_technology_id
    FROM sub_technology st
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = FALSE
    )
    AND ed.year = {year}
    GROUP BY c.country_id
    """
    cur.execute(query)
    non_renewables = pd.DataFrame(cur.fetchall())
    non_renewables.columns = [i[0] for i in cur.description]
    conn.close()
    return non_renewables

def renewables_data_details(country, year, data_col):
    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = f"""
    SELECT gt.name as group_technology, SUM(ed.{data_col}) AS total_renewables
    FROM energy_data ed
    INNER JOIN sub_technology st ON ed.sub_tech_id = st.sub_technology_id
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = TRUE
    AND ed.year = {year}
    AND ed.country_id IN (SELECT country_id FROM countries WHERE name = '{country}')
    GROUP BY gt.name;
    """
    cur.execute(query)
    country_data = pd.DataFrame(cur.fetchall())
    country_data.columns = [i[0] for i in cur.description]
    
    conn.close()
    return country_data

def non_renewables_data_details(country, year, data_col):
    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = f"""
    SELECT gt.name as group_technology, SUM(ed.{data_col}) AS total_non_renewables
    FROM energy_data ed
    INNER JOIN sub_technology st ON ed.sub_tech_id = st.sub_technology_id
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = FALSE
    AND ed.year = {year}
    AND ed.country_id IN (SELECT country_id FROM countries WHERE name = '{country}')
    GROUP BY gt.name;
    """
    cur.execute(query)
    country_data = pd.DataFrame(cur.fetchall())
    country_data.columns = [i[0] for i in cur.description]
    
    conn.close()
    return country_data

def renewables_details(country, year):
    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = f"""
    SELECT gt.name as group_technology, SUM(ed.electricity_generation_gwh) AS total_generation_gwh
    FROM energy_data ed
    INNER JOIN sub_technology st ON ed.sub_tech_id = st.sub_technology_id
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = TRUE
    AND ed.year = {year}
    AND ed.country_id IN (SELECT country_id FROM countries WHERE name = '{country}')
    GROUP BY gt.name;
    """
    cur.execute(query)
    country_data = pd.DataFrame(cur.fetchall())
    country_data.columns = [i[0] for i in cur.description]
    
    conn.close()
    return country_data

def historic_renewable_data(data_col):
    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = f"""
    SELECT ed.year, c.name, SUM(ed.{data_col}) AS total_renewable
    FROM energy_data ed
    INNER JOIN countries c ON ed.country_id = c.country_id
    WHERE ed.sub_tech_id IN
    (
    SELECT st.sub_technology_id
    FROM sub_technology st
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = TRUE
    )
    AND ed.year BETWEEN 2008 AND 2023
    GROUP BY ed.year, c.country_id
    ORDER BY ed.year ASC;
    """
    cur.execute(query)
    renewables = pd.DataFrame(cur.fetchall())
    renewables.columns = [i[0] for i in cur.description]

    conn.close()
    return renewables

def historic_non_renewables_data(data_col):
    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = f"""
    SELECT ed.year, c.name, SUM(ed.{data_col}) AS total_non_renewable
    FROM energy_data ed
    INNER JOIN countries c ON ed.country_id = c.country_id
    WHERE ed.sub_tech_id IN
    (
    SELECT st.sub_technology_id
    FROM sub_technology st
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = FALSE
    )
    AND ed.year BETWEEN 2008 AND 2023
    GROUP BY ed.year, c.country_id
    ORDER BY ed.year ASC;
    """
    cur.execute(query)
    non_renewables = pd.DataFrame(cur.fetchall())
    non_renewables.columns = [i[0] for i in cur.description]
    
    conn.close()
    return non_renewables

def historic_renewabledata_country(country, data_col):

    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query_c = f"""
    SELECT ed.year, gt.name as group_technology, SUM(ed.{data_col}) AS total_renewables
    FROM energy_data ed
    INNER JOIN sub_technology st ON ed.sub_tech_id = st.sub_technology_id
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = TRUE
    AND ed.year BETWEEN 2008 AND 2023
    AND ed.country_id IN (SELECT country_id FROM countries WHERE name = '{country}')
    GROUP BY gt.name, ed.year;
    """
    cur.execute(query_c)
    country_data = pd.DataFrame(cur.fetchall())
    country_data.columns = [i[0] for i in cur.description]

    conn.close()
    return country_data

def historic_non_renewabledata_country(country, data_col):

    db_path = './energy_database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query_c = f"""
    SELECT ed.year, gt.name as group_technology, SUM(ed.{data_col}) AS total_non_renewables
    FROM energy_data ed
    INNER JOIN sub_technology st ON ed.sub_tech_id = st.sub_technology_id
    INNER JOIN technology t ON st.technology_id = t.technology_id
    INNER JOIN group_technology gt ON t.group_technology_id = gt.group_technology_id
    WHERE gt.renewable = FALSE
    AND ed.year BETWEEN 2008 AND 2023
    AND ed.country_id IN (SELECT country_id FROM countries WHERE name = '{country}')
    GROUP BY gt.name, ed.year;
    """
    cur.execute(query_c)
    country_data = pd.DataFrame(cur.fetchall())
    country_data.columns = [i[0] for i in cur.description]

    conn.close()
    return country_data