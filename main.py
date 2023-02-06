import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime as dt
from datetime import time
from PIL import Image
import folium
from streamlit_folium import st_folium

# Usamos todo el ancho en lugar de la parte central de la pagina
st.set_page_config(page_title="Afa-nalytics",
                   layout='wide',
                   initial_sidebar_state='auto')

# Borramos el "Made with streamlit" del footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Borramos el hamburger menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)



# DATE_COLUMN = 'date/time'
DATA_URL = ('data/clubes.csv')

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    data['fecha_fundacion'] = data['fecha_fundacion'].apply(pd.to_datetime)
    data["fecha"] = pd.to_datetime(data["fecha_fundacion"])
    data['fundacion_dia'] = data["fecha"].dt.day
    data['fundacion_mes'] = data["fecha"].dt.month
    data['fundacion_anio'] = data["fecha"].dt.year
    return data


#Cargamos el DF
data = load_data()


def density_graph(data, categoria_menu, variable, x_axis_label, y_axis_label):

    x = x_axis_label+":Q"
    y = y_axis_label+":Q"
    # color = categoria+':N'

    # ISIN sólo permite pasar listas. Si pasamos un string, tira un error.
    # Verificamos que categoria_menu tenga al menos dos elementos (list), sino, lo convertirmos a list con un elemento
    if not isinstance(categoria_menu, list): categoria_menu = [categoria_menu]


    df_1 = data.loc[data['categoria'].isin(categoria_menu)]
    df_1 = df_1[[variable, 'categoria']]
    c = alt.Chart(df_1).transform_density(
        variable,
        as_=[x_axis_label, y_axis_label],
        groupby=['categoria']
    ).mark_area().encode(
        x= x,
        y= y,
        color = alt.Color('categoria:N',
                          legend=alt.Legend(orient='bottom'))
    ).configure_mark(
    opacity=0.2,
    color='red',
    )

    return c


def density_graph_club(club, data, data_club, categoria, variable, x_axis_label, y_axis_label):
    x = x_axis_label + ":Q"
    y = y_axis_label + ":Q"
    # color = categoria+':N'
    # st.text('club:' + str(type(club)))
    # st.text('data:' + str(type(data)))
    # st.text('data_club:' + str(type(data_club)))
    # st.text('categoria:' + str(type(categoria)))
    # st.text('variable:' + str(type(variable)))
    # st.text('x_axis_label:' + str(type(x)))
    # st.text('y_axis_label:' + str(type(y)))
    # df_1 = data.loc[data['categoria'].isin(categoria_menu)]
    # df_1 = df_1[[variable, 'categoria']]
    c = alt.Chart(data).transform_density(
        variable,
        as_=[x_axis_label, y_axis_label],
        groupby=['categoria']
    ).mark_area().encode(
        x=x,
        y=y,
        color= alt.Color('categoria:N',
                          legend=alt.Legend(orient='bottom'))
    )
    # El configure del gráfico se pasó al codigo de donde se llama la funcion
    # https://stackoverflow.com/questions/50662831/layered-or-facet-bar-plot-with-label-values-in-altair

    #     .configure_mark(
    #     opacity=0.2,
    #     color='red'
    # )
    club_value = data_club[variable].values[0]
    st.caption("Valor para el club:"+str(club_value))
    club_line = alt.Chart(pd.DataFrame({'Linea roja: Club': [club_value]})).mark_rule(color='red').encode(x='Linea roja: Club', strokeWidth=alt.value(5))
    # media_line = (
    #     alt.Chart(data_club[variable].values[0])
    #         .transform_quantile(variable, as_=['prob', 'value'])
    #         .mark_rule()
    #         .encode(
    #         x='mean(value):Q',
    #         color=alt.value('red')
    #     )
    # )

    return c, club_line

variables_plot_dict = {'capacidad_estadio':'Capacidad del Estadio',
                      'socios':'Cantidad de Socios',
                      'titulos_primera':'Títulos en Primera',
                      'titulos_internacionales':'Titulos Internacionales',
                      # 'cuota_social':'Cuota Social',
                      'ingresos_socios':'Ingresos provenientes de los socios',
                      # 'valor_entradas_promedio':'Valor de la entrada (promedio)',
                      'ingresos_entradas':'Ingresos por venta de entradas',
                      'entradas_vendidas':'Cantidad de entradas vendidas',
                      'ingresos_tv':'Ingresos por televisación',
                      'ingresos_comerciales':'Ingresos comerciales',
                      'ingresos_totales':'Ingresos totales',
                      'sueldo_dt':'Sueldo DT',
                      'sueldos_plantel':'Sueldos del Plantel',
                      'egresos_generales':'Egresos generales',
                      'egresos_totales':'Egresos totales',
                      'balance_anual':'Balance anual'}


st.title('AFA-nalytics')
st.markdown('CAMPEONES DEL MUNDO   :star: :star: :star:')

# Definimos las tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["GENERAL", "CLUB POR CLUB", "CLUBES TOP", "GUERRA DE CLUBES", "TIMELINE", "ABOUT"])



with tab1:
    st.container()
    st.subheader('Algunos datos de los clubes de Buenos Aires y CABA')

    categoria_ms_values = data['categoria'].unique()
    # area_ms_values = data['area'].unique()

    categoria_ms = st.multiselect(
        'Seleccione la categoria',
        categoria_ms_values,
        default='Liga Profesional'
    )
    # area_ms = st.multiselect(
    #     'Seleccione área',
    #     area_ms_values,
    #     default='PBA'
    # )


    # Generamos la grilla con 3 columnas para los gráficos
    col11, col12, col13 = st.columns(3)
    number_plot = 0

    for variable in variables_plot_dict:
        if number_plot<=4:
            with col11:
                st.subheader(variables_plot_dict[variable], anchor=None)
                st.altair_chart(density_graph(data, categoria_ms, variable, variables_plot_dict[variable], 'Densidad'), use_container_width=True)
        if 5 <= number_plot <=9:
            with col12:
                st.subheader(variables_plot_dict[variable], anchor=None)
                st.altair_chart(density_graph(data, categoria_ms, variable, variables_plot_dict[variable], 'Densidad'), use_container_width=True)
        if number_plot>=10:
            with col13:
                st.subheader(variables_plot_dict[variable], anchor=None)
                st.altair_chart(density_graph(data, categoria_ms, variable, variables_plot_dict[variable], 'Densidad'), use_container_width=True)
        number_plot = number_plot + 1

with tab2:
    st.container()
    st.subheader('Información por club')
    col21, col22, col23 = st.columns([1, 2, 2])
    with col21:
        club_sb_values = data['nombre_coloquial'].unique()

        # Menú desplegable clubes
        club_sb = st.selectbox(
            'Seleccione el club',
            club_sb_values,
            # default='Estudiantes (LP)'
        )

        # Escudo del club
        url = data.loc[data['nombre_coloquial']==club_sb]['imagen-url'].values[0]
        st.image(url, width=100)

        club_data = data.loc[data['nombre_coloquial']==club_sb]

        # Separador de miles
        club_data  = club_data.applymap(lambda x: f'{x:,d}' if isinstance(x, int) else x)
        txt_fundacion  = '**- Fecha fundación:** ' + str(club_data['fundacion_dia'].values[0]) + "/" + str(club_data['fundacion_mes'].values[0]) + "/" + str(club_data['fundacion_anio'].values[0])
        txt_barrio = '**- Barrio:** ' + club_data['barrio_localidad'].values[0]
        txt_socios = '**- Socios:** ' + str(club_data['socios'].values[0])
        txt_estadio = '**- Estadio:** ' + club_data['nombre_estadio'].values[0]
        txt_categoria = '**- Categoría:** ' + club_data['categoria'].values[0]
        txt_titulos_primera = '**- Títulos en primera:** ' + str(club_data['titulos_primera'].values[0])
        txt_titulos_internacionales = '**- Títulos internacionales:** ' + str(club_data['titulos_internacionales'].values[0])
        st.markdown(txt_fundacion)
        st.markdown(txt_barrio)
        st.markdown(txt_socios)
        st.markdown(txt_estadio)
        st.markdown(txt_categoria)
        st.markdown(txt_titulos_primera)
        st.markdown(txt_titulos_internacionales)

        st.map(club_data)

    # Filramos el DF para obtener info de toda la categoría, para graficar la densidad
    data_cat = data.loc[data['categoria'] == club_data['categoria'].values[0]]
    # nombre de la categoria
    categoria = club_data['categoria'].values[0]

    number_plot = 0
    for variable in variables_plot_dict:
        if number_plot <= 7:
            with col22:
                st.subheader(variables_plot_dict[variable], anchor=None)
                c, media_line = density_graph_club(club_sb, data_cat, club_data, categoria, variable, variables_plot_dict[variable],
                                   'Densidad')
                # grafico = c + media_line
                graph_club_altair = alt.layer(c, media_line).configure_mark(opacity=0.2,color='red')

                st.altair_chart(graph_club_altair, use_container_width=True)
        if 7 < number_plot <= 18:
            with col23:
                st.subheader(variables_plot_dict[variable], anchor=None)
                c, media_line = density_graph_club(club_sb, data_cat, club_data, categoria, variable, variables_plot_dict[variable],
                                   'Densidad')
                # grafico = c + media_line
                graph_club_altair = alt.layer(c, media_line).configure_mark(opacity=0.2,color='red')

                st.altair_chart(graph_club_altair, use_container_width=True)
        number_plot = number_plot + 1

def rename_columns(data, col1, col2, variables_plot_dict):
    # st.text(variables_plot_dict[col2])
    # st.text(variables_plot_dict[col2])
    data.rename(columns={col1: 'Club',
                         col2: variables_plot_dict[col2],},
                inplace=True)
    return data


with tab3:
    col31, col32,col33, col34 = st.columns(4)
    top_variables = ['capacidad_estadio', 'socios', 'titulos_primera', 'titulos_internacionales', 'entradas_vendidas', 'sueldo_dt', 'sueldos_plantel', 'balance_anual']
    number_plot = 0
    df_top_format = data.copy()
    # Separador de miles.
    df_top_format = df_top_format.applymap(lambda x: f'{x:,d}' if isinstance(x, int) else x)
    for var in top_variables:
        if number_plot<=1:
            with col31:
                st.subheader(variables_plot_dict[var])
                df_top = df_top_format.sort_values(by=var, ascending=False).head(5)
                df_top = df_top[['nombre_coloquial', var]]
                top_df = rename_columns(df_top, 'nombre_coloquial',var,variables_plot_dict)
                # CSS to inject contained in a string
                hide_table_row_index = """
                            <style>
                            thead tr th:first-child {display:none}
                            tbody th {display:none}
                            </style>
                            """
                # Inject CSS with Markdown
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                # Display a static table
                st.table(top_df)
        if 2<= number_plot <= 3:
            with col32:
                st.subheader(variables_plot_dict[var])
                df_top = df_top_format.sort_values(by=var, ascending=False).head(5)
                df_top = df_top[['nombre_coloquial', var]]
                top_df = rename_columns(df_top, 'nombre_coloquial', var, variables_plot_dict)
                # CSS to inject contained in a string
                hide_table_row_index = """
                            <style>
                            thead tr th:first-child {display:none}
                            tbody th {display:none}
                            </style>
                            """
                # Inject CSS with Markdown
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                # Display a static table
                st.table(top_df)
        if 4<= number_plot <= 5:
            with col33:
                st.subheader(variables_plot_dict[var])
                df_top = df_top_format.sort_values(by=var, ascending=False).head(5)
                df_top = df_top[['nombre_coloquial', var]]
                top_df = rename_columns(df_top, 'nombre_coloquial', var, variables_plot_dict)
                # CSS to inject contained in a string
                hide_table_row_index = """
                            <style>
                            thead tr th:first-child {display:none}
                            tbody th {display:none}
                            </style>
                            """
                # Inject CSS with Markdown
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                # Display a static table
                st.table(top_df)
        if 6<= number_plot <= 9:
            with col34:
                st.subheader(variables_plot_dict[var])
                df_top = df_top_format.sort_values(by=var, ascending=False).head(5)
                df_top = df_top[['nombre_coloquial', var]]
                top_df = rename_columns(df_top, 'nombre_coloquial', var, variables_plot_dict)

                # CSS to inject contained in a string
                hide_table_row_index = """
                            <style>
                            thead tr th:first-child {display:none}
                            tbody th {display:none}
                            </style>
                            """
                # Inject CSS with Markdown
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                # Display a static table
                st.table(top_df)
        number_plot = number_plot +1


with tab4:
    with st.container():
        st.subheader('Comparación entre clubes')
        col41, col42  = st.columns([1,2])
        with col41:
            # Menú desplegable clubes a y b
            club_guerra1 = st.selectbox(
                'Seleccione el club A',
                club_sb_values,
                key = 'sb_guerra_a'
            )
            # Convertimos el array a list para borrar el elemento seleccionado en el primer selectbox
            # (para evitar seleccionar los mismos clubes)
            club_sb_b = club_sb_values.tolist()
            club_sb_b.remove(club_guerra1)

            club_guerra2 = st.selectbox(
                'Seleccione el club B',
                club_sb_b,
                # default='Estudiantes (LP)',
                key='sb_guerra_b'
            )
            df_guerra = data.loc[(data['nombre_coloquial']==club_guerra1) | (data['nombre_coloquial']==club_guerra2)]
            df_guerra = df_guerra[
                ['nombre_coloquial', 'capacidad_estadio', 'socios', 'division', 'titulos_primera', 'titulos_internacionales',
                 'entradas_vendidas', 'ingresos_totales', 'sueldo_dt', 'sueldos_plantel', 'balance_anual']]

            # Transformamos el DF para mostrarlo
            df_guerra.set_index('nombre_coloquial')
            df_guerra = df_guerra.melt(id_vars='nombre_coloquial',
                                       value_vars = [
                                                      'capacidad_estadio', 'socios', 'division', 'titulos_primera',
                                                      'titulos_internacionales', 'entradas_vendidas',
                                                      'ingresos_totales', 'sueldo_dt', 'sueldos_plantel',
                                                      'balance_anual'
                                                      ],
                                       value_name = 'cantidad')

            df_guerra = df_guerra.pivot(index = 'variable' ,
                                        columns = 'nombre_coloquial',
                                        values = 'cantidad').reset_index()

            df_guerra = df_guerra.replace({"variable": variables_plot_dict})
            df_guerra.set_index('variable')

            # Separador de miles.
            df_guerra = df_guerra.applymap(lambda x: f'{x:,d}' if isinstance(x, int) else x)
            with col42:
                st.table(df_guerra)

with tab5:
    st.subheader('En construcción - Evolución de los clubes en la zona PBA y CABA')
    year_min = data['fundacion_anio'].min()
    year_max = data['fundacion_anio'].max()

    gap_years = st.slider(
        'Seleccione el rango de fechas',
        int(year_min),
        int(year_max),
        (int(year_min), int(year_max)),
        int(1))
    # st.text(gap_years)
    #
    df_geo = data.loc[((data['fundacion_anio']>=gap_years[0]) & (data['fundacion_anio']<=gap_years[1])) & (data['lat']!=0) ]
    # mapa de streamlit. No se le puede agregar info al popup
    # st.map(df_geo)


    map = folium.Map(location=[df_geo['lat'].mean(),
                               df_geo['lon'].mean()],
                     zoom_start=10,
                     control_scale=True)

    for index, location_info in df_geo.iterrows():
        link_google_base = 'https://www.google.com/maps/search/'
        link_lat_lon = str(location_info["lat"]) + ',' + str(location_info["lon"]) +'/@' + str(location_info["lat"]) + ',' + str(location_info["lon"]) + 'z13'
        link_google_url = link_google_base + link_lat_lon
        link_google_maps = '- Club: ' + location_info["nombre_club"] + '<br>- Año: ' + str(location_info["fundacion_anio"]) + '<br> - ' + '<a href =' + link_google_url + ' target="_blank"> Google Maps </a>'

        iframe = folium.IFrame(link_google_maps)
        popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Marker([location_info["lat"],
                       location_info["lon"]],
                      popup=popup,
                      ).add_to(map)



    st_data = st_folium(map, width='100%')




with tab6:
    # st.header("About")
    about = '''Desarrollado por [Mato](https://matog.github.io/cv/), con la base gentimente cedida por [@unknown.datasets](https://linktr.ee/unknow.datasets)

Todo corre sobre [Streamlit](https://www.streamlit.io), un framework de Python para desarrollar dashboards, 
y como paquetes adicionales sólo utiliza [Pandas](https://pandas.pydata.org/) para procesar la info, 
[Altair](https://altair-viz.github.io/) para graficarla y [Folium](https://python-visualization.github.io/folium/)
para los mapas.

El código está disponible en [Github](https://github.com/matog/afa-analitics). También existe una versión en docker, 
que prontó estará disponible para descargar'''
    st.markdown(about)

