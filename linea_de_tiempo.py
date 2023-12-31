# -*- coding: utf-8 -*-
"""Linea de tiempo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U8F8kCwDCFcvR7MARYhF3ji7aXHzjGBm
"""

!pip install dash plotly

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Datos de ejemplo
proyectos = [
    {"nombre": "Implementación del módulo BEAS", "fecha_inicio": "2023-05-08", "fecha_fin": "2023-08-15", "completado": False, "categoria": "Implementación"},
    {"nombre": "Implementación del módulo WMS", "fecha_inicio": "2023-05-12", "fecha_fin": "2023-09-15", "completado": False, "categoria": "Implementación"},
    {"nombre": "Implementación del módulo de mantenimiento", "fecha_inicio": "2023-05-30", "fecha_fin": "2023-07-30", "completado": False, "categoria": "Implementación"},
    {"nombre": "Implementación del módulo CRM", "fecha_inicio": "2023-07-21", "fecha_fin": "2023-10-16", "completado": False, "categoria": "Implementación"},
    {"nombre": "Implementación del módulo Recursos Humanos", "fecha_inicio": "2023-09-08", "fecha_fin": "2023-10-16", "completado": False, "categoria": "Implementación"},
    {"nombre": "Parametrización del módulo de compras", "fecha_inicio": "2023-07-05", "fecha_fin": "2023-10-09", "completado": False, "categoria": "Parametrización"},
    {"nombre": "Parametrización del módulo de Logística", "fecha_inicio": "2023-07-05", "fecha_fin": "2023-10-09", "completado": False, "categoria": "Parametrización"},
    {"nombre": "Parametrización del módulo de Tesorería", "fecha_inicio": "2023-08-07", "fecha_fin": "2023-10-20", "completado": False, "categoria": "Parametrización"},
    {"nombre": "Implementación software LIMS", "fecha_inicio": "2023-06-21", "fecha_fin": "2023-10-13", "completado": False, "categoria": "Implementación"},
    {"nombre": "Implementación seguridad informática", "fecha_inicio": "2023-05-10", "fecha_fin": "2023-09-20", "completado": True, "categoria": "Implementación"},
    {"nombre": "Implementación de infraestructura en nube (AZURE)", "fecha_inicio": "2023-09-01", "fecha_fin": "2023-09-20", "completado": True, "categoria": "Implementación"},
    {"nombre": "Implementación SAP México", "fecha_inicio": "2023-09-15", "fecha_fin": "2024-01-26", "completado": False, "categoria": "Implementación"},
    {"nombre": "Implementación control de roles y perfiles de los sistemas de información de la compañía", "fecha_inicio": "2023-07-28", "fecha_fin": "2023-09-06", "completado": True, "categoria": "Implementación"},
    {"nombre": "Implementación control de roles y perfiles y seguridad del sistema de control y validación IMOMENTRICS", "fecha_inicio": "2023-08-23", "fecha_fin": "2023-09-15", "completado": True, "categoria": "Implementación"},
    {"nombre": "Implementación de PLASMANET", "fecha_inicio": "2023-04-28", "fecha_fin": "2023-12-15", "completado": False, "categoria": "Implementación"},
    {"nombre": "PLATAFORMA DE MESA DE AYUDA WEB", "fecha_inicio": "2023-06-09", "fecha_fin": "2023-06-20", "completado": True, "categoria": "Otras Actividades"},
    {"nombre": "REPOSITORIO WEB SISTEMA INTEGRADO DE GESTIÓN(SHAREPOINT)", "fecha_inicio": "2023-09-01", "fecha_fin": "2023-09-08", "completado": True, "categoria": "Otras Actividades"},
    {"nombre": "REPOSITORIO DOCUMENTAL DE LA DIRECCIÓN FINANCIERA Y CONTABLE", "fecha_inicio": "2023-09-01", "fecha_fin": "2023-09-14", "completado": True, "categoria": "Otras Actividades"},
    {"nombre": "IMPLEMENTACIÓN DE METODOLOGIA SCRUM PARA PROYECTOS", "fecha_inicio": "2023-05-01", "fecha_fin": "2023-12-31", "completado": True, "categoria": "Implementación"}
]

# Porcentaje de avance para cada proyecto (100% verde, de lo contrario amarillo)
porcentaje_avance = [43, 47, 85, 42, 36, 90, 100, 50, 93, 100, 100, 15, 100, 100, 20, 100, 100, 100, 100]
colores = ['green' if avance == 100 else '#FFC300' for avance in porcentaje_avance]

# Colores para las categorías
colores_categorias = {
    "Implementación": "rgb(31, 119, 180)",
    "Parametrización": "rgb(255, 127, 14)",
    "Otras Actividades": "rgb(44, 160, 44)",
    "Todos": "rgb(214, 39, 40)"
}

# Crear la aplicación Dash
app = dash.Dash(__name__)

server = app.server

# Diseño del dashboard
app.layout = html.Div([
    html.Div([
        html.H1('Línea de Tiempo de Proyectos', style={'color': 'white', 'text-align': 'center', 'font-family': 'Arial, sans-serif'}),
    ], style={'background': 'linear-gradient(to right, #001f3f, #0074CC)', 'padding': '20px', 'text-align': 'center'}),
    dcc.Graph(id='timeline-graph'),
    dcc.RadioItems(
        id='categoria-selector',
        options=[
            {'label': 'Todos', 'value': 'Todos'},
            {'label': 'Implementación', 'value': 'Implementación'},
            {'label': 'Parametrización', 'value': 'Parametrización'},
            {'label': 'Otras Actividades', 'value': 'Otras Actividades'}
        ],
        value='Todos',
        labelStyle={'display': 'inline-block'}
    ),
    html.A('Abrir en pantalla completa', href='javascript:void(0);', id='fullscreen-button', target='_blank', style={'color': 'white', 'background-color': '#333', 'padding': '10px', 'border-radius': '10px', 'text-align': 'center', 'margin-top': '20px', 'display': 'block', 'font-family': 'Arial, sans-serif'})
])

# Callback para abrir en pantalla completa
@app.callback(
    Output('fullscreen-button', 'href'),
    Input('fullscreen-button', 'n_clicks')
)
def open_in_fullscreen(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        return 'URL_DE_LA_PAGINA_DE_VISUALIZACION_COMPLETA'

# Callback para actualizar la línea de tiempo
@app.callback(
    Output('timeline-graph', 'figure'),
    Input('timeline-graph', 'relayoutData'),
    Input('categoria-selector', 'value')
)
def update_timeline_graph(relayoutData, categoria_seleccionada):
    # Filtrar proyectos por categoría seleccionada
    if categoria_seleccionada == 'Todos':
        proyectos_filtrados = proyectos
        porcentaje_avance_filtrado = porcentaje_avance
        colores_filtrados = colores
    else:
        proyectos_filtrados = [p for p in proyectos if p['categoria'] == categoria_seleccionada]
        porcentaje_avance_filtrado = [porcentaje_avance[i] for i, p in enumerate(proyectos) if p['categoria'] == categoria_seleccionada]
        colores_filtrados = [colores[i] for i, p in enumerate(proyectos) if p['categoria'] == categoria_seleccionada]

    proyectos_filtrados.sort(key=lambda x: x["fecha_inicio"])

    # Crea una lista de nombres de proyectos, fechas de inicio, fin y categoría
    nombres = [p["nombre"] for p in proyectos_filtrados]
    fechas_inicio = [p["fecha_inicio"] for p in proyectos_filtrados]
    fechas_fin = [p["fecha_fin"] for p in proyectos_filtrados]
    categorias = [p["categoria"] for p in proyectos_filtrados]
    porcentajes = [str(porcentaje) + "%" for porcentaje in porcentaje_avance_filtrado]

    # Crea los datos para la línea de tiempo
    data = []
    categoria_actual = None

    for nombre, inicio, fin, categoria, porcentaje, color in zip(nombres, fechas_inicio, fechas_fin, categorias, porcentajes, colores_filtrados):
        if categoria_actual != categoria:
            # Agregar un punto de segmentación
            data.append(go.Scatter(x=[inicio, inicio], y=[nombre, nombre], mode='lines',
                                   line=dict(color=colores_categorias[categoria], width=10),
                                   hoverinfo='none', showlegend=False))
            categoria_actual = categoria

        data.append(go.Scatter(x=[inicio, fin], y=[nombre, nombre], mode='lines+markers',
                               text=["Proyecto: {}<br>Inicio: {}<br>Fin: {}<br>Porcentaje de Avance: {}".format(nombre, inicio, fin, porcentaje)],
                               hoverinfo='text', line=dict(width=6, color=color), name=nombre))

    layout = dict(
        title='Línea de Tiempo de Proyectos',
        yaxis=dict(showticklabels=False),
        xaxis=dict(title='Fecha'),
        hovermode='closest'
    )

    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=False)

!pip freeze > requirements.txt