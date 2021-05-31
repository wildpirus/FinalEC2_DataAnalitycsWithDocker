import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2 as pc
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import numpy as np
 
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

DB_HOST = "postgres_db"
DB_NAME = "test_db"
DB_USER = "root"
DB_PASS = "root"

conn = pc.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

r=read_query(conn, "select Hora, Valor, Lugar from INVEMAR where Valor<150")
o=read_query(conn, "select Hora, avg(Valor) from INVEMAR group by Hora order by Hora")
q=read_query(conn, "select Hora, max(Valor) from INVEMAR where Lugar='Punta Betin' group by Hora order by Hora")

cur.close() 
conn.close()



app = dash.Dash(__name__)

a = []
b = []
c = []
for data in r:
    a.append(data[0])
    b.append(data[1])
    c.append(data[2])
dd = {'Hora':a,'Velocidad':b, "Lugar":c }
fig1 = px.scatter(dd, x="Hora", y="Velocidad", color="Lugar", marginal_y="violin",
           marginal_x="box", trendline="ols", template="simple_white",title="Gráfico de dispersion")

a = []
b = []
for data in o:
    a.append(data[0])
    b.append(data[1])
dd = {'Hora':a,'Velocidad':b }
fig2 = px.line(dd, x="Hora", y="Velocidad", title='Promedio de velocidad por hora')

a = []
b = []
for data in q:
    a.append(data[0])
    b.append(data[1])
dd = {'Hora':a,'Velocidad':b }
fig3 = px.line(dd, x="Hora", y="Velocidad", title='Maxima de velocidad por hora en Punta Betin')

#-----------------------------
# App layout
app.layout = html.Div([

    html.H1("Información sobre las costas (INVEMAR)", style={'text-align': 'center'}),
    html.Br(),
    dcc.Graph(id="chart1", figure=fig1),
    html.Br(),
    dcc.Graph(id="chart2", figure=fig2),
    html.Br(),
    dcc.Graph(id="chart3", figure=fig3),
])

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8080,debug=True)