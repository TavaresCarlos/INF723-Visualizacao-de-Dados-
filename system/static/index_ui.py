import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import tempfile
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

class index_windows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = False
        self.index_initUI()
    
    def index_initUI(self):
        self.setGeometry(50,120,1800,870)
        self.setWindowTitle("Wind Power Data SCADA Viewer")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setMinimumHeight(40)

        self.layout_vertical = QGridLayout(self.central_widget)

        #Botão para carregar csv
        self.load_button = QPushButton("Carregar CSV", self)
        self.load_button.setMaximumSize(200, 4320)
        self.load_button.clicked.connect(self.load_csv)
        self.layout_vertical.addWidget(self.load_button, 0, 0, 1, 1) #numero da linha, numero da coluna, total de linhas, total de colunas

        #Visualizar headers de cada coluna do arquivo csv
        self.list_widget = QListWidget(self)
        self.list_widget.setMaximumSize(200, 4320)
        self.layout_vertical.addWidget(self.list_widget, 1, 0, 11, 1)
        
        #Curva de produção de energia
        self.plot_widget = QWebEngineView()
        self.layout_vertical.addWidget(self.plot_widget, 1, 1, 5, 1)

        #Boxplot 
        self.plot_widget2 = QWebEngineView()
        self.layout_vertical.addWidget(self.plot_widget2, 1, 2, 5, 1)

        #Imagem do aerogerador
        self.label_imagem = QLabel(self)
        self.layout_vertical.addWidget(self.label_imagem, 1, 3, 9, 1)

        #Produção de energia ao longo do tempo
        self.plot_widget3 = QWebEngineView()
        self.layout_vertical.addWidget(self.plot_widget3, 6, 1, 6, 2)
        
        #Regressão Linear entre temperatura amabiente x temperatura nacelle 
        #self.plot_widget4 = QWebEngineView()
        #self.layout_vertical.addWidget(self.plot_widget4, 6, 2, 6, 1)

    def open_image(self):
        pixmap = QPixmap('./asserts/image/wind-turbine.jpg')
        self.label_imagem.setPixmap(pixmap)
        self.setMinimumSize(1800,870)
        self.setMaximumSize(1450, 790)

    def anomaly_chart(self):
        #PAF = Pontos de Anomalias e Falhas
        anomaly_trace_1 = go.Scatter(
            x = self.df['Wind Speed (m/s)'],
            y = self.df['LV ActivePower (kW)'],
            mode = 'markers',
            marker = dict(color='#836FFF'),
            name = 'PAF'
        )

        #CR = Curva de Referência
        anomaly_trace_2 = go.Scatter(
            x = self.df['Wind Speed (m/s)'],
            y = self.df['Theoretical_Power_Curve (KWh)'],
            mode = 'markers',
            marker = dict(color='#F0E68C'),
            name = 'CR'
        )

        anomaly_layout = go.Layout(
            title = 'Curva de Potência (kW)',
            xaxis = dict(title='Velocidade do Vento (m/s)'),
            yaxis = dict(title='Potência (kW)')
        )

        # Adicionar os traces ao objeto de dados (data)
        anomaly_data = [anomaly_trace_1, anomaly_trace_2]
        # Criar a figura
        anomaly_fig = go.Figure(data = anomaly_data, layout = anomaly_layout)
        anomaly_temp_file = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
        anomaly_fig.write_html(anomaly_temp_file.name)
        anomaly_temp_file.close()
        self.plot_widget.setUrl(QUrl.fromLocalFile(anomaly_temp_file.name))
    
    def bloxplot_chart(self):
        boxplot_fig = make_subplots(rows=1, cols=2)

        boxplot_fig.add_trace(go.Box(y = self.df['Wind Speed (m/s)'], name = 'Wind Speed (m/s)', showlegend = False, boxpoints = 'outliers'), row = 1, col = 1)
        boxplot_fig.add_trace(go.Box(y = self.df['LV ActivePower (kW)'], name = 'ActivePower (kW)', showlegend = False, boxpoints = 'outliers'), row = 1, col = 2)

        boxplot_fig.update_layout(title='Distribuição dos Dados e Detecção de Outliers')

        boxplot_temp_file = tempfile.NamedTemporaryFile(suffix = '.html', delete = False)
        boxplot_fig.write_html(boxplot_temp_file.name)
        boxplot_temp_file.close()
        self.plot_widget2.setUrl(QUrl.fromLocalFile(boxplot_temp_file.name))

    def time_produce_chart(self):
        time_produce_trace_1 = go.Scatter(
            x = self.df['Date/Time'],
            y = self.df['LV ActivePower (kW)'],
            mode = 'lines+markers',
            marker = dict(color='#836FFF'),
            name = 'Produção'
        )
       
        
        time_produce_trace_2 = go.Scatter(
            x = self.df['Date/Time'],
            y = self.df['Theoretical_Power_Curve (KWh)'],
            mode = 'lines+markers',
            marker = dict(color='#ff6961'),
            name = 'Teórica'
        )
        

        time_produce_layout = go.Layout(
            title = 'Potências Real x Teórica',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Power (kW)')
        )

        time_produce_data = [time_produce_trace_2, time_produce_trace_1]
        time_produce_fig = go.Figure(data = time_produce_data, layout = time_produce_layout)
        
        time_produce_fig.update_xaxes(showticklabels=False)
        time_produce_fig.update_layout(xaxis=dict(range=[0, 200]))

        time_produce_temp_file = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
        time_produce_fig.write_html(time_produce_temp_file.name)
        time_produce_temp_file.close()
        self.plot_widget3.setUrl(QUrl.fromLocalFile(time_produce_temp_file.name)) 
        

   
    def load_csv(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if fileName:
            self.populate_table_widget(fileName)   
        
        self.df = pd.read_csv(fileName)
        #01
        self.anomaly_chart()
        #02
        self.bloxplot_chart()
        #03
        self.time_produce_chart()
        #05
        self.open_image()
    
    def populate_table_widget(self, file_path):
        self.df = pd.read_csv(file_path)
        headers = list(self.df.columns)
        self.list_widget.addItems(headers)

    def mousePressEvent(self, event):
        # Obter as coordenadas x e y do evento de clique do mouse
        x = event.x()
        y = event.y()

        if 1399 <= x <= 1510 and 185 <= y <= 223:
            print("Nacele")
            self.label_imagem.setPixmap(QPixmap('./asserts/image/wind-turbine-nacelle.jpg'))

            self.secondary_window = SecondaryWindow()
            self.secondary_window.show()


        if 1460 <= x <= 1541 and 59 <= y <= 104:
            print("Blade")
            self.label_imagem.setPixmap(QPixmap('./asserts/image/wind-turbine-blade.jpg'))

        print(f'Coordenadas do Clique: ({x}, {y})')

class SecondaryWindow(index_windows):
    def __init__(self):
        super().__init__()
        self.plot_line_nacelle()

    def plot_line_nacelle(self):
        self.setWindowTitle("Gráfico")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.plot_widget5 = QWebEngineView()
        self.layout.addWidget(self.plot_widget5)

        df = pd.read_csv('../dataset-example/wind-data.csv')

        fig = px.scatter(df, x=df['Wind Direction (°)'], y=df['Wind Speed (m/s)'])
        fig.update_layout(margin=dict(l=50, r=50, t=50, b=50))

        plotly_html = fig.to_html(include_plotlyjs='cdn', full_html=False)
        self.plot_widget5.setHtml(plotly_html)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)
