import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import queries
import graphics


color = "#D7D0D0"
#-----------------------------------------------------------------
page_title = "Transición Energética"
main_title = "Transición Energética en Paises de Sudamérica"
boton1 = "Introducción"
boton2 = "Energía por País"
boton3 = "Línea de tiempo"
# boton4 = "Modelo"
column_1_size = 0.25
def space(str):
    return (25 - len(str))//2
TITULO_HOME = "TRANSICIÓN ENERGÉTICA Y OBJETIVOS DE DESARROLLO SOSTENIBLE EN SUDAMÉRICA" 
TEXTO_HOME = """Este dashboard interactivo presenta un análisis comparativo de la evolución de la dependencia energética de fuentes fósiles en seis países sudamericanos: Colombia, Brasil, Chile, Argentina, Uruguay y Perú, en el período comprendido entre 2015 y 2025. El propósito central es evaluar el impacto de la adopción de los Objetivos de Desarrollo Sostenible (ODS) —especialmente el ODS 7 (energía asequible y no contaminante) y el ODS 13 (acción por el clima)— en las políticas públicas de transición energética de estos países.

Para ello, se utilizaron datos oficiales de la Agencia Internacional de Energías Renovables (IRENA), que permiten medir el consumo energético final por tipo de tecnología. A través de visualizaciones dinámicas y comparativas, este tablero facilita la comprensión de los avances, rezagos y retos que enfrenta la región en su camino hacia una matriz energética más limpia, justa y sostenible."""
TEXTO_EXPLICANDO_1 = "Evaluar y comparar el impacto de la adopción de los ODS en las políticas de transición energética en países sudamericanos como Colombia, Brasil, Chile, Argentina, Uruguay y Perú entre 2015 y 2024. A partir de una base de datos confiable y actualizada, se aplicarán técnicas avanzadas de análisis de datos."
TEXTO_EXPLICANDO_2 = "TEXTO EXPLICANDO 2"
TEXTO_EXPLICANDO_3 = "TEXTO EXPLICANDO 3"
TEXTO_EXPLICANDO_4 = "TEXTO EXPLICANDO 4"
#-----------------------------------------------------------------
column_2_size = 1-column_1_size
#-----------------------------------------------------------------

st.set_page_config(page_title=page_title,page_icon=":chart_with_upwards_trend:",layout="wide")
st.markdown("""
    <style>
            body {
                background-color: #D7D0D0;
                color: #000000
            }
            .stApp {
                background-color: #D7D0D0;
                color: #000000
            }
    </style>
""",unsafe_allow_html=True)
#------------------------------------------------------------------
data_col_dict = {'Generación de energía (GWh)':'electricity_generation_gwh',
                 'Capacidad instalada (MW)':'electricity_installed_mw'}

axis_labels_dict = {'Generación de energía (GWh)':['Producción de energía renovable', 'Producción de energía no renovables'],
                      'Capacidad instalada (MW)':['Capacidad instalada en renovables', 'Capacidad instalada en no renovables']}

titles_dict = {'Generación de energía (GWh)':'Producción de energía por pais en año',
                      'Capacidad instalada (MW)':'Capacidad instalada por pais en año'}


if "data_col_dict" not in st.session_state:
    st.session_state["data_col_dict"] = data_col_dict
if "axis_labels_dict" not in st.session_state:
    st.session_state["axis_labels_dict"] = axis_labels_dict
if "titles_dict" not in st.session_state:
    st.session_state["titles_dict"] = titles_dict

if "countries" not in st.session_state:
    countries = ["ARGENTINA", "COLOMBIA","BRAZIL","URUGUAY","PERU","CHILE"]
    st.session_state["countries"] = countries

view = {}
view[boton1] = False
view[boton2] = False
view[boton3] = False
# view[boton4] = False

if "view" not in st.session_state:
    st.session_state["view"] = view


def btn_handle(btn):
    for button in st.session_state["view"]:
        st.session_state["view"][button] = False
    st.session_state["view"][btn] = True


t1, t2 = st.columns([column_1_size,column_2_size])
t2.markdown("")
t2.markdown("")

t1.title(main_title)
t1.markdown("")
t1.button(label=" "*space(boton1)+boton1+" "*space(boton1),key=boton1, on_click=btn_handle, args=(boton1,))
t1.markdown("")
t1.button(label=" "*space(boton2)+boton2+" "*space(boton2),key=boton2, on_click=btn_handle, args=(boton2,))
t1.markdown("")
t1.button(label=" "*space(boton3)+boton3+" "*space(boton3),key=boton3, on_click=btn_handle, args=(boton3,))
# t1.markdown("")
# t1.button(label=" "*space(boton4)+boton4+" "*space(boton4),key=boton4, on_click=btn_handle, args=(boton4,))


#---------------------------------------------------------------

if st.session_state["view"][boton1]:
    t2.markdown(f"""
            <div style="text-align: center;">
                <h1>{TITULO_HOME}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    t2_1_1, t2_1_2 = t2.columns([0.5,0.5])

    t2_1_1.markdown(f"""
            <div style="text-align: left; color:#000000">
                <p>{TEXTO_HOME}</p>
            </div>
        """, unsafe_allow_html=True)
    
    t2_1_2.image("./img_home.png",use_container_width=True)


    t2.markdown(f"""
            <div style="text-align: center;">
                <h3>Objetivo General</h3>
                <p>{TEXTO_EXPLICANDO_1}</p>
            </div>
        """, unsafe_allow_html=True)
    

    #-------------------------------------------------------------------


if st.session_state["view"][boton2]:

    t2.markdown("## Comparación de energías para un año dado")
    t2.markdown("")
    t2.markdown("")
    t2_1, t2_2 = t2.columns([0.5,0.5])

    t2_1_1, t2_1_2 = t2_1.columns([0.5, 0.5])

    #t2_2_1.image("./grafica2.jpg",use_container_width=True)
    year = t2_1_1.number_input(label="Seleccione el año",min_value=2000, max_value=2023)
    #t2_2_2.image("./grafica2.jpg",use_container_width=True)
    column = t2_1_2.selectbox(label="Seleccione columna",options=[clave for clave in st.session_state["data_col_dict"]])

    country = t2_2.selectbox(label="Seleccione pais a detallar", 
                            options=['Argentina', 'Brazil', 'Uruguay', 'Chile', 'Peru', 'Colombia'])
    
    data_col = st.session_state["data_col_dict"][column]
    axis_labels = st.session_state["axis_labels_dict"][column]
    title = st.session_state["titles_dict"][column]
    fig_1, ax_1 = plt.subplots()
    fig_1 = graphics.plot_countries_data(year, data_col, axis_labels, title)
    #fig_1 = graphics.plot_energy_use_countries(year)
    t2_1.pyplot(fig_1)

    fig_2, ax_2 = plt.subplots()
    fig_2 = graphics.plot_renewables_data_details(country, year, data_col, column, title)
    #fig_2 = graphics.plot_renewables_details(country, year)
    t2_2.pyplot(fig_2)


if st.session_state["view"][boton3]:
    
    t2.markdown("## Datos historicos del uso de energia")
    t2.markdown("")
    t2.markdown("")
    t2_1, t2_2 = t2.columns([0.5,0.5])

    t2_1_1, t2_1_2 = t2_1.columns([0.5, 0.5])

    column = t2_1_1.selectbox(label="Seleccione columna",
                            options=[clave for clave in st.session_state["data_col_dict"]])
    
    type = t2_1_2.selectbox(label="Seleccione el tipo de energía", options=["renovables", "no renovables"])

    country = t2_2.selectbox(label="Seleccione pais a detallar", 
                            options=['Argentina', 'Brazil', 'Uruguay', 'Chile', 'Peru', 'Colombia'])

    data_col = st.session_state["data_col_dict"][column]
    fig_1, ax_1 = plt.subplots()
    if column == "Generación de energía (GWh)":
        title =f"Historico de generación de energías {type}"
    elif column == "Capacidad instalada (MW)":
        title = f"Historico de capacidad instalada en energías {type}"
    
    if type == "renovables":
        fig_1 = graphics.plot_historic_renewable_data(data_col, title, column)
    elif type == "no renovables":
        fig_1 = graphics.plot_historic_non_renewable_data(data_col, title, column)
    
    t2_1.pyplot(fig_1)

    if column == "Generación de energía (GWh)":
        title =f"Historico de generación de energías {type} en {country}"
    elif column == "Capacidad instalada (MW)":
        title = f"Historico de capacidad instalada en energías {type} en {country}"

    if type == "renovables":
        fig_2 = graphics.plot_historic_renewabledata_country(country, data_col, title, column)
    elif type == "no renovables":
        fig_2 = graphics.plot_historic_non_renewabledata_country(country, data_col, title, column)

    t2_2.pyplot(fig_2)

# if st.session_state["view"][boton4]:
#     pass

#     #t2.image("./grafica1.png",use_container_width=True)
