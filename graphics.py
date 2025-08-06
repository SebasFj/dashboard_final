import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import queries

def plot_countries_data(year, data_col, axis_labels, title):
    renewables = queries.get_renewable_data_countries(year, data_col)
    non_renewables = queries.get_non_renewable_data_countries(year, data_col)
    energy_usage = pd.merge(renewables, non_renewables, on='name', suffixes=('_renewable', '_non_renewable'))
    energy_usage['total_energy'] = energy_usage['total_renewable'] + energy_usage['total_non_renewable']

    fig, ax = plt.subplots(figsize=(10, 6))

    non_renewables_percentage = energy_usage['total_non_renewable']/energy_usage['total_energy']*100
    renewables_percentage = non_renewables_percentage + energy_usage['total_renewable']/energy_usage['total_energy']*100

    ax_1 = sns.barplot(data=energy_usage, x='name', y=renewables_percentage, label=axis_labels[0], color='#ffaaff')
    ax_2 = sns.barplot(data=energy_usage, x='name', y=non_renewables_percentage, label=axis_labels[1], color='#aa22ff')

    ax_1.bar_label(container=ax_1.containers[0], 
                labels=[f'{val:.2f}%' for val in (renewables_percentage-non_renewables_percentage)],
                fontsize=10)

    ax_2.bar_label(ax_2.containers[1],label_type='center',
                labels=[f'{val:.2f}%' for val in non_renewables_percentage],
                fontsize=10)

    ax.set_title(f'{title} {year}')
    ax.set_xlabel('País')
    ax.set_ylabel('Porcentaje Energía generada (%)')
    #ax.xticks(rotation=90)
    return fig

def plot_energy_use_countries(year):
    renewables = queries.renewable_use_countries(year)
    non_renewables = queries.non_renewables_use_countries(year)
    energy_usage = pd.merge(renewables, non_renewables, on='name', suffixes=('_renewable', '_non_renewable'))
    energy_usage['total_energy_production_gwh'] = energy_usage['total_renewable_gwh'] + energy_usage['total_non_renewable_gwh']

    fig, ax = plt.subplots(figsize=(10, 6))

    non_renewables_percentage = energy_usage['total_non_renewable_gwh']/energy_usage['total_energy_production_gwh']*100
    renewables_percentage = non_renewables_percentage + energy_usage['total_renewable_gwh']/energy_usage['total_energy_production_gwh']*100

    ax_1 = sns.barplot(data=energy_usage, x='name', y=renewables_percentage, label='Uso de renovables', color='#ffaaff')
    ax_2 = sns.barplot(data=energy_usage, x='name', y=non_renewables_percentage, label='Uso de no renovables', color='#aa22ff')

    ax_1.bar_label(container=ax_1.containers[0], 
                labels=[f'{val:.2f}%' for val in (renewables_percentage-non_renewables_percentage)],
                fontsize=10)

    ax_2.bar_label(ax_2.containers[1],label_type='center',
                labels=[f'{val:.2f}%' for val in non_renewables_percentage],
                fontsize=10)

    ax.set_title(f'Producción de energía por país en {year}')
    ax.set_xlabel('País')
    ax.set_ylabel('Porcentaje Energía generada (%)')
    #ax.xticks(rotation=90)
    return fig

def plot_renewables_data_details(country, year, data_col, axis_label, title):
    data = queries.renewables_data_details(country, year, data_col)
    nulls_index = data[data['total_renewables'].isna()].index
    data.drop(nulls_index, inplace=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))

    percentages = data['total_renewables']/(data['total_renewables'].sum())*100

    sns.color_palette("pastel")
    ax = sns.barplot(data=data, x='group_technology', y='total_renewables', color='#ffaaff')
    ax.bar_label(ax.containers[0], fontsize=10)
    ax.bar_label(ax.containers[0], label_type='center', 
                labels=[f'{val:.2f}%' for val in percentages], 
                fontsize=10)
    ax.set_title(f'{title} {year}, pais: {country}')
    ax.set_xlabel('Tecnología')
    ax.set_ylabel(axis_label)
    ax.set_xticks(ticks=data['group_technology'].values, labels=data['group_technology'].values, rotation=90)
    ax.set_yscale('log')
    return fig

def plot_renewables_details(country, year):
    data = queries.renewables_details(country, year)
    nulls_index = data[data['total_generation_gwh'].isna()].index
    data.drop(nulls_index, inplace=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))

    percentages = data['total_generation_gwh']/(data['total_generation_gwh'].sum())*100

    sns.color_palette("pastel")
    ax = sns.barplot(data=data, x='group_technology', y='total_generation_gwh', label='Producción en renovables', color='#ffaaff')
    ax.bar_label(ax.containers[0], fontsize=10)
    ax.bar_label(ax.containers[0], label_type='center', 
                labels=[f'{val:.2f}%' for val in percentages], 
                fontsize=10)
    ax.set_title(f'Producción de energía renovable en {country} para el año {year}')
    ax.set_xlabel('Tecnología')
    ax.set_ylabel('Proudcción de energía (GWh))')
    ax.set_xticks(ticks=data['group_technology'].values, labels=data['group_technology'].values, rotation=90)
    ax.set_yscale('log')
    return fig

def plot_historic_renewable_data(data_col, title, axis_label):
    historic_data = queries.historic_renewable_data(data_col)
    countries = queries.get_countries_names()

    renew_dict = {}
    for country in countries['name']:
        country_df = historic_data[historic_data['name'] == country][['year','total_renewable']]
        country_df.set_index('year', inplace=True)
        country_df.rename(columns={'total_renewable':country}, inplace=True)
        renew_dict[country] = country_df
        

    data_renewable = pd.DataFrame()
    for country in renew_dict.keys():
        data_renewable = pd.concat([data_renewable, renew_dict[country]], axis=1)
    
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(data=data_renewable, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel("Año")
    ax.set_ylabel(axis_label)
    return fig

def plot_historic_non_renewable_data(data_col, title, axis_label):
    historic_data = queries.historic_non_renewables_data(data_col)
    countries = queries.get_countries_names()

    renew_dict = {}
    for country in countries['name']:
        country_df = historic_data[historic_data['name'] == country][['year','total_non_renewable']]
        country_df.set_index('year', inplace=True)
        country_df.rename(columns={'total_non_renewable':country}, inplace=True)
        renew_dict[country] = country_df
        
    data_renewable = pd.DataFrame()
    for country in renew_dict.keys():
        data_renewable = pd.concat([data_renewable, renew_dict[country]], axis=1)
    
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(data=data_renewable, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel("Año")
    ax.set_ylabel(axis_label)
    return fig

def plot_historic_renewabledata_country(country, data_col, title, axis_label):

    country_data = queries.historic_renewabledata_country(country, data_col)

    tech_dict = {}

    for tech in country_data['group_technology'].unique():
        tech_df = country_data[country_data['group_technology'] == tech][['year','total_renewables']]
        tech_df.set_index('year', inplace=True)
        tech_df.rename(columns={'total_renewables':tech}, inplace=True)
        print(f"Total filas para {tech}: {tech_df.shape[0]}")
        tech_dict[tech] = tech_df
    
    data_renewable = pd.DataFrame()
    for tech in tech_dict.keys():
        data_renewable = pd.concat([data_renewable, tech_dict[tech]], axis=1)
    
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(data=data_renewable, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel("Año")
    ax.set_ylabel(axis_label)
    return fig

def plot_historic_non_renewabledata_country(country, data_col, title, axis_label):

    country_data = queries.historic_non_renewabledata_country(country, data_col)

    tech_dict = {}

    for tech in country_data['group_technology'].unique():
        tech_df = country_data[country_data['group_technology'] == tech][['year','total_non_renewables']]
        tech_df.set_index('year', inplace=True)
        tech_df.rename(columns={'total_non_renewables':tech}, inplace=True)
        print(f"Total filas para {tech}: {tech_df.shape[0]}")
        tech_dict[tech] = tech_df
    
    data_renewable = pd.DataFrame()
    for tech in tech_dict.keys():
        data_renewable = pd.concat([data_renewable, tech_dict[tech]], axis=1)
    
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(data=data_renewable, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel("Año")
    ax.set_ylabel(axis_label)
    return fig

    

    

