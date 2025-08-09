# Descripción de los Archivos del Proyecto

A continuación se presenta una descripción detallada de los principales archivos que conforman este repositorio, empleados durante el desarrollo del proyecto.

---

## 📂 Datos

- **`IRENA_Stats_extract_2025 H2(Country) (1).csv`**  
  Base de datos original provista por la **Agencia Internacional de Energías Renovables (IRENA)**, que contiene información relacionada con la inversión, generación y capacidad instalada de energías renovables y no renovables en **235 países**.

---

## 📓 Notebooks

- **`Preprocesamiento_base_de_datos.ipynb`**  
  Contiene el análisis exploratorio inicial y los procesos de limpieza de la base de datos.  
  Incluye la propuesta de **normalización de datos**, la cual sirvió como base para la aplicación de consultas SQL.

- **`SQL_Queries_Proyecto.ipynb`**  
  Implementa las consultas SQL diseñadas sobre la base de datos normalizada, con el objetivo de extraer información relevante para el análisis.

---

## 🗂 Diagramas

- **`normalized_data_base (2).png`**  
  Esquema visual del diseño de la base de datos normalizada aplicado a los datos originales.  
  Este diagrama fue desarrollado con la herramienta [drawdb.app](https://drawdb.app).

---

## 💻 Scripts de Python

- **`bd.py`**  
  Script que crea la base de datos **`energy_database.bd`** a partir del script SQL **`bd.sql`**. Posteriormente, inserta los datos procesados desde el *DataFrame* original utilizando **Pandas** y **SQLite**.

- **`queries.py`** y **`graphics.py`**  
  Contienen las consultas SQL para la recuperación de datos de interés y la generación de visualizaciones a partir de los resultados.

- **`dashboard.py`**  
  Implementa un tablero interactivo desarrollado con **Streamlit**, permitiendo explorar y visualizar los resultados del análisis.

---

## 📌 Notas Finales
Este conjunto de archivos conforma el flujo completo del proyecto:  
1. **Adquisición y preprocesamiento de datos**  
2. **Normalización y modelado de base de datos**  
3. **Consultas SQL y análisis**  
4. **Visualización interactiva** mediante un *dashboard*.
