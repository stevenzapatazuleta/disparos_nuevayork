# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import streamlit as st
import pydeck as pdk 
import plotly.express as px
import plotly.graph_objects as go
import base64

st.set_page_config(layout='wide')
st.markdown("<h1 style ='text-align: center;color:#1687CE;'> Historico de disparos en Nueva York 🗽🔫</h1>",unsafe_allow_html=True)

@st.cache(persist=True)
def load_data(url):
    df = pd.read_csv(url)
    df['OCCUR_DATE'] =pd.to_datetime(df['OCCUR_DATE'])
    df['OCCUR_TIME'] =pd.to_datetime(df['OCCUR_TIME'],format='%H:%M:%S')
    df['YEAR']=df['OCCUR_DATE'].dt.year
    df['HOUR']=df['OCCUR_TIME'].dt.hour
    df['YEARMONTH']=df['OCCUR_DATE'].dt.strftime('%Y%m')
    df.columns = df.columns.map(str.lower)
    
    return df
    
def get_table_download_link(df):
    csv = df.to_csv(index =False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href

df=load_data('NYPD_Shooting_Incident_Data__Historic_.csv')

#---------------------------------------------------------------------
#indicadores

# Dividir el layout en cinco partes
c1, c2, c3, c4, c5 = st.columns((1,1,1,1,1))

## Primer markdown
c1.markdown("<h3 style='text-align: left; color: Gray;'> Top Sexo </h3>", unsafe_allow_html=True)

#cual es el sexo que mas se presenta en los atacantes y victimas
# Organizar data
top_perp_name = df['perp_sex'].value_counts().index[0].capitalize()
top_perp_num = (round((df['perp_sex'].value_counts()/df['perp_sex'].value_counts().sum()),2)*100)[0]
top_vic_name = df['vic_sex'].value_counts().index[0].capitalize()
top_vic_num = (round((df['vic_sex'].value_counts()/df['vic_sex'].value_counts().sum()),2)*100)[0]

# Enviar a streamlit en un texto
c1.text('Atacante: '+str(top_perp_name)+', '+str(top_perp_num)+'%')
c1.text('Víctima: '+str(top_vic_name)+', '+str(top_vic_num)+'%')

## Segundo markdown
c2.markdown("<h3 style='text-align: left; color: Gray;'> Top Raza </h3>", unsafe_allow_html=True)

# Organizar data
top_perp_name = df['perp_race'].value_counts().index[0].capitalize()
top_perp_num = (round((df['perp_race'].value_counts()/df['perp_race'].value_counts().sum()),2)*100)[0]
top_vic_name = df['vic_race'].value_counts().index[0].capitalize()
top_vic_num = (round((df['vic_race'].value_counts()/df['vic_race'].value_counts().sum()),2)*100)[0]

# Enviar a streamlit
c2.text('Atacante: '+str(top_perp_name)+', '+str(top_perp_num)+'%')
c2.text('Víctima: '+str(top_vic_name)+', '+str(top_vic_num)+'%')

## Tercer markdown
c3.markdown("<h3 style='text-align: left; color: Gray;'> Top Edad </h3>", unsafe_allow_html=True)

# Organizar data
top_perp_name = df['perp_age_group'].value_counts().index[0].capitalize()
top_perp_num = (round((df['perp_age_group'].value_counts()/df['perp_age_group'].value_counts().sum()),2)*100)[0]
top_vic_name = df['vic_age_group'].value_counts().index[0].capitalize()
top_vic_num = (round((df['vic_age_group'].value_counts()/df['vic_age_group'].value_counts().sum()),2)*100)[0]

# Enviar a streamlit
c3.text('Atacante: '+str(top_perp_name)+', '+str(top_perp_num)+'%')
c3.text('Víctima: '+str(top_vic_name)+', '+str(top_vic_num)+'%')

## Cuarto markdown
c4.markdown("<h3 style='text-align: left; color: Gray;'> Top Barrio</h3>", unsafe_allow_html=True)

# Organizar data
top_perp_name = df['boro'].value_counts().index[0].capitalize()
top_perp_num = (round((df['boro'].value_counts()/df['boro'].value_counts().sum()),2)*100)[0]

# Enviar a streamlit
c4.text('Barrio: '+str(top_perp_name)+', '+str(top_perp_num)+'%')

## Quinto markdown
c5.markdown("<h3 style='text-align: left; color: Gray;'> Top Hora</h3>", unsafe_allow_html=True)

# Organizar data
top_perp_name = df['hour'].value_counts().index[0]
top_perp_num = (round((df['hour'].value_counts()/df['hour'].value_counts().sum()),2)*100)[0]

# Enviar a streamlit
c5.text('Hora: '+str(top_perp_name)+', '+str(top_perp_num)+'%')

#-------------------------------

c1, c2 = st.columns((1,1)) #dividir el dashboard en 2 partes y el tamaño
c1.markdown("<h3 style ='text-align: center;color:black;'> Donde han ocurrido disparos en Nueva York</h3>",unsafe_allow_html=True)

year = c1.slider('Año en el que ocurrio el suceso', 2006, 2020)
c1.map(df[df['year']==year][['latitude','longitude']])

c2.markdown("<h3 style ='text-align: center;color:black;'>¿A que horas ocurren disparos en Nueva York?</h3>",unsafe_allow_html=True)
hour = c2.slider('hora en la que ocurrio el suceso', 0, 23)
df2= df[df['hour']==hour]

c2.write(pdk.Deck(
        map_style = 'mapbox://styles/mapbox/light-v9',
        initial_view_state ={ 
             'latitude':df['latitude'].mean(),
             'longitude': df['longitude'].mean(),
             'zoom': 9.5,
             'pitch': 50
             }, # centrar la vision del mapa
         
        layers = [pdk.Layer(
        'HexagonLayer',
        data=df2[['latitude','longitude']],
        get_position=['longitude','latitude'],
        radius=100,
        extruded= True,
        elevation_scale =4,
        elevation_rage =[0,1000])] # la forma geometrica en como van a salir los datos
         ))
#write - se manda el mapa
#-----------------

st.markdown("<h3 style ='text-align: center;color:black;'>¿como ha sido la evolucion de disparos por barrio en Nueva York?</h3>",unsafe_allow_html=True)

df3=df.groupby(['yearmonth','boro'])[['incident_key']].count().reset_index().rename(columns={'incident_key':'disparos'})

fig= px.line(df3, x='yearmonth',y='disparos',color='boro',width=1200,height=450)
# Editar gráfica
fig.update_layout(
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',
    template = 'simple_white',
    xaxis_title="<b>Año/mes<b>",
    yaxis_title='<b>Cantidad de incidentes<b>',
    legend_title_text='',
    legend=dict(orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.8))

st.plotly_chart(fig) #enviar una figura 
#------------
c4,c5,c6,c7 = st.columns((1,1,1,1))

c4.markdown("<h3 style ='text-align: center;color:black;'>¿que edad tienen los atacantes?</h3>",unsafe_allow_html=True)

df2= df.groupby(['perp_age_group'])[['incident_key']].count().reset_index().rename(columns={'incident_key':'disparos'})

df2['perp_age_group']=df2['perp_age_group'].replace({'940':'N/A','224':'N/A',
                                                     '1020':'N/A','UNKNOWN':'N/A'})
df2['perp_age_group2']=df2['perp_age_group'].replace({'<18':'1','18-24':'2','25-44':'3',
                                                      '45-64':'4','65+':'5','N/A':'6'})

df2=df2.sort_values('perp_age_group2')

fig= px.bar(df2,x='disparos',y='perp_age_group',orientation='h',width=340,height=310)

fig.update_layout(
    xaxis_title="<b>atacante<b>",
    yaxis_title="<b>Edades<b>",
    template = 'simple_white',
    plot_bgcolor='rgba(0,0,0,0)')

c4.plotly_chart(fig)

#-------------------
# Definir título
c5.markdown("<h3 style='text-align: center; color: black;'> ¿Qué edad tienen los víctimas? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby(['vic_age_group'])[['incident_key']].count().reset_index().rename(columns = {'incident_key':'disparos'})

# Crear categoría para organizar el orden de las edades
df2['vic_age_group2'] = df2['vic_age_group'].replace({'<18':'1',
                              '18-24':'2',
                              '25.44':'3',
                              '45-64':'4',
                              '65+':'5',
                              'UNKNOWN': '6'})

# Cambiar UNKNOWN por un nombre más corto
df2['vic_age_group'] = df2['vic_age_group'].replace({
                              'UNKNOWN': 'N/A'})

# Aplicar orden al DataFrame
df2= df2.sort_values('vic_age_group2')

# Hacer gráfica
fig = px.bar(df2, x="disparos", y="vic_age_group", orientation='h', width=340,  height=310)
fig.update_layout(xaxis_title="<b>Víctima<b>",
                  yaxis_title="<b><b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')

# Enviar gráfica a streamlit
c5.plotly_chart(fig)

################ ---- Tercera Gráfica

# Definir título
c6.markdown("<h3 style='text-align: center; color: Black;'> ¿Cuál es el sexo del atacante? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby('perp_sex')[['incident_key']].count().reset_index().sort_values('incident_key', ascending = False)

# Hacer gráfica
fig = px.pie(df2, values = 'incident_key', names="perp_sex",
             width=340, height=310)

# Adicionar detalles a la gráfica
fig.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))

# Enviar gráfica a streamlit
c6.plotly_chart(fig)

################ ---- Cuarta Gráfica

# Definir título
c7.markdown("<h3 style='text-align: center; color: Black;'> ¿Cuál es el sexo de la víctima? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
df2 = df.groupby('vic_sex')[['incident_key']].count().reset_index().sort_values('incident_key', ascending = False)

# Hacer gráfica
fig = px.pie(df2, values = 'incident_key', names="vic_sex",
             width=340, height=310)

# Adicionar detalles a la gráfica
fig.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))

# Enviar gráfica a streamlit
c7.plotly_chart(fig)


#---------------------------------------------------------------------

# Definir título
#toma todo el espacio
st.markdown("<h3 style='text-align: center; color: Black;'> Evolución de disparos por año en las horas con más y menos sucesos </h3>", unsafe_allow_html=True)

# Organizar DataFrame
#las horas donde mas y menos disparos sucedieron
df2 = df[df['hour'].isin([23,9])].groupby(['year','hour'])[['incident_key']].count().sort_values('incident_key', ascending = False).reset_index() 
df2['hour'] = df2['hour'].astype('category') #necesario para que lo tome el numero como una categoria y no un rango

# Hacer gráfica
fig = px.bar(df2, x='year', y='incident_key', color ='hour', barmode='group', width=1600, height=450)

# Adicionar detalles a la gráfica
fig.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        legend_title_text = 'Hora',
        xaxis_title="<b>Año<b>",
        yaxis_title="<b>Cantidad de disparos<b>")

# Enviar gráfica a streamlit
st.plotly_chart(fig)

# Hacer un checkbox
if st.checkbox('Obtener datos por fecha y barrio', False): #por defecto tiene valor de false(si nadie lo ha cambiado sea falso)
    
    # Código para generar el DataFrame
    df2 = df.groupby(['occur_date','boro'])[['incident_key']].count().reset_index().rename(columns ={'boro':'Barrio','occur_date':'Fecha','incident_key':'Cantidad'})
    df2['Fecha'] = df2['Fecha'].dt.date
    
    # Código para convertir el DataFrame en una tabla plotly resumen
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df2.columns), #encabezado(nombre de las columnas))
        fill_color='lightgrey', #color del fondo
        line_color='darkslategray'),  #color de la linea
        #informacion de cada una de las columnas
        cells=dict(values=[df2.Fecha, df2.Barrio, df2.Cantidad],fill_color='white',line_color='lightgrey'))
       ])
    fig.update_layout(width=500, height=450)

# Enviar tabla a streamlit
    st.write(fig) #cuando es una tabla figura 
    
# Generar link de descarga
    st.markdown(get_table_download_link(df2), unsafe_allow_html=True)