import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image


# Usamos todo el ancho en lugar de la parte central de la pagina
st.set_page_config(layout="wide")




# DATE_COLUMN = 'date/time'
DATA_URL = ('data/clubes.csv')

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    return data


#Cargamos el DF
data = load_data()


def density_graph(data, categoria_menu, variable, x_axis_label, y_axis_label):
    x = x_axis_label+":Q"
    y = y_axis_label+":Q"
    # color = categoria+':N'

    # ISIN sólo permite pasas listas. Si pasamos un string, tira un error.
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
        color = 'categoria:N'
    ).configure_mark(
    opacity=0.2,
    color='red'
    )
    return c


def density_graph_club(club, data, data_club, categoria, variable, x_axis_label, y_axis_label):
    x = x_axis_label + ":Q"
    y = y_axis_label + ":Q"
    # color = categoria+':N'

    # df_1 = data.loc[data['categoria'].isin(categoria_menu)]
    # df_1 = df_1[[variable, 'categoria']]
    c = alt.Chart(data).transform_density(
        variable,
        as_=[x_axis_label, y_axis_label],
        groupby=['categoria']
    ).mark_area().encode(
        x=x,
        y=y,
        color='categoria:N'
    )
    # El configure se pasó al codigo de donde se llama la funcion
    # https://stackoverflow.com/questions/50662831/layered-or-facet-bar-plot-with-label-values-in-altair

    #     .configure_mark(
    #     opacity=0.2,
    #     color='red'
    # )
    club_value = data_club[variable].values[0]
    st.caption("Valor para el club:"+str(club_value))
    club_line = alt.Chart(pd.DataFrame({'a': [club_value]})).mark_rule(color='red').encode(x='a')
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


st.title('FUTBOL O MUERTE!')
# Definimos las tabs
tab1, tab2, tab3, tab4 = st.tabs(["GENERAL", "CLUB POR CLUB", "CLUBES TOP", "ABOUT"])



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
                st.text(number_plot)
                st.subheader(variables_plot_dict[variable], anchor=None)
                st.altair_chart(density_graph(data, categoria_ms, variable, variables_plot_dict[variable], 'Densidad'), use_container_width=True)
        if 5 <= number_plot <=9:
            with col12:
                st.text(number_plot)
                st.subheader(variables_plot_dict[variable], anchor=None)
                st.altair_chart(density_graph(data, categoria_ms, variable, variables_plot_dict[variable], 'Densidad'), use_container_width=True)
        if number_plot>=10:
            with col13:
                st.text(number_plot)
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

        txt_fundacion  = '**- Fecha fundación:** ' + club_data['fecha_fundacion'].values[0]
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

with tab3:
    col31, col32,col33 = st.columns(3)
    # with col31:
    #     st.subheader('Clubes con mas títulos locales')
    #     titulos_primera = data['titulos_primera'].max()
    #     titulos_primera_club = data['titulos_primera'].max().['nombre_coloquial']
    #     st.text(titulos_primera)
    #     st.text(titulos_primera_club)


with tab4:
    # st.header("About")
    about = '''Desarrollado por [Mato](https://matog.github.io/cv/), con la base gentimente cedida por [@unknown.datasets](https://linktr.ee/unknow.datasets)

Todo corre sobre [Streamlit](https://www.streamlit.io), un framework de Python para desarrollar dashboards, y utiliza [Pandas](https://pandas.pydata.org/) para procesar la info y [Altair](https://altair-viz.github.io/) para graficarla.

El código está disponible en [Github](https://github.com/matog/futbol-streamlit)'''
    st.markdown(about)

