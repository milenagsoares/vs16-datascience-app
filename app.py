# Passo 3: Construir o Aplicativo Dash com Bootstrap
# O aplicativo será composto de duas partes principais: o layout (como ele se parece) e os callbacks (como ele interage).

# --- 1. Importar as bibliotecas necessárias ---
# Importe dash, dcc (componentes interativos), html (tags HTML),
# Output e Input (para callbacks), plotly.express (para gráficos),
# pandas (para manipulação de dados) e dash_bootstrap_components (para Bootstrap).

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from ucimlrepo import fetch_ucirepo


print("🔄 Carregando dados do UCI ML Repository...")

# baixando o dataset
heart_disease = fetch_ucirepo(id=45)

dados = heart_disease.data.features

# Classe alvo (diagnóstico)
target = heart_disease.data.targets

# Combinar features e target em um único DataFrame
df = dados.copy()
df['target'] = target

print(" Dados carregados com sucesso!")
print(f"Formato do dataset: {df.shape}")
print(f" Colunas: {list(df.columns)}")
print("\n Primeiras 5 linhas:")
print(df.head())

# Converter target para binário (0 = sem doença, 1 = com doença)
df['has_disease'] = (df['target'] > 0).astype(int)

# Mapear valores categóricos para labels legíveis
df['sex_label'] = df['sex'].map({0: 'Feminino', 1: 'Masculino'})
df['cp_label'] = df['cp'].map({
    1: 'Angina típica',
    2: 'Angina atípica', 
    3: 'Dor não-anginosa',
    4: 'Assintomático'
})

# iinicializar o aplicativo Dash com tema Bootstrap ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# --- 4. Layout do aplicativo com Bootstrap ---
app.layout = dbc.Container([
    # Cabeçalho
    dbc.Row([
        dbc.Col([
            html.H1("🫀 Análise de Doenças Cardíacas", 
                    className="text-center mb-2 text-primary"),
            html.P("Dashboard interativo para análise do dataset de doenças cardíacas do UCI ML Repository",
                   className="text-center text-muted lead")
        ])
    ], className="mb-4"),
    
    # Informações do dataset com Cards Bootstrap
    dbc.Row([
        dbc.Col([
            html.H3("📊 Informações do Dataset", className="text-primary mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(f"{len(df)}", className="text-info mb-0"),
                            html.P("Total de Registros", className="mb-0 text-muted")
                        ])
                    ], className="text-center h-100")
                ], width=3),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(f"{len(df.columns)}", className="text-danger mb-0"),
                            html.P("Variáveis", className="mb-0 text-muted")
                        ])
                    ], className="text-center h-100")
                ], width=3),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(f"{df['has_disease'].sum()}", className="text-warning mb-0"),
                            html.P("Com Doença Cardíaca", className="mb-0 text-muted")
                        ])
                    ], className="text-center h-100")
                ], width=3),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(f"{len(df) - df['has_disease'].sum()}", className="text-success mb-0"),
                            html.P("Sem Doença Cardíaca", className="mb-0 text-muted")
                        ])
                    ], className="text-center h-100")
                ], width=3)
            ], className="g-3")
        ])
    ], className="mb-4"),
    
    # Controles com Card Bootstrap
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("🎛️ Controles", className="mb-0")),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Selecione uma variável para análise:", className="fw-bold"),
                            dcc.Dropdown(
                                id='variavel-dropdown',
                                options=[
                                    {'label': 'Idade', 'value': 'age'},
                                    {'label': 'Pressão Arterial em Repouso', 'value': 'trestbps'},
                                    {'label': 'Colesterol', 'value': 'chol'},
                                    {'label': 'Frequência Cardíaca Máxima', 'value': 'thalach'},
                                    {'label': 'Depressão ST', 'value': 'oldpeak'}
                                ],
                                value='age',
                                className="mt-2"
                            )
                        ], width=6),
                        
                        dbc.Col([
                            dbc.Label("Filtrar por sexo:", className="fw-bold"),
                            dbc.RadioItems(
                                id='sexo-radio',
                                options=[
                                    {'label': 'Todos', 'value': 'all'},
                                    {'label': 'Masculino', 'value': 1},
                                    {'label': 'Feminino', 'value': 0}
                                ],
                                value='all',
                                className="mt-2"
                            )
                        ], width=6)
                    ])
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Gráficos com sistema de Grid Bootstrap
    dbc.Row([
        dbc.Col([
            html.H3("📈 Visualizações", className="text-primary mb-3"),
        ])
    ]),
    
    # Primeira linha de gráficos
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='grafico-distribuicao')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='grafico-sexo')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Segunda linha de gráficos
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='grafico-correlacao')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='grafico-tipo-dor')
                ])
            ])
        ], width=6)
    ])
], fluid=True, className="px-4")

# --- 5. Callbacks (como o aplicativo interage) ---
# Aqui, a mágica acontece. Use o '@app.callback' para conectar a saída de um
# componente à entrada de outro.
# O 'Output' (saída) será o seu gráfico ('id='grafico-distribuicao').
# Os 'Input' (entradas) serão os menus suspensos e radio buttons.
# A função será chamada sempre que um 'Input' mudar.

@app.callback(
    Output(component_id='grafico-distribuicao', component_property='figure'),
    [Input(component_id='variavel-dropdown', component_property='value'),
     Input(component_id='sexo-radio', component_property='value')]
)
def update_distribuicao_graph(variavel, sexo_filtro):
    """
    Gráfico de distribuição da variável selecionada
    Dentro desta função, crie o gráfico usando 'plotly.express.histogram'.
    Use os valores de 'variavel' e 'sexo_filtro' que vêm dos controles.
    """
    df_filtrado = df.copy()
    
    # Aplicar filtro por sexo se selecionado
    if sexo_filtro != 'all':
        df_filtrado = df_filtrado[df_filtrado['sex'] == sexo_filtro]
    
    # Verificar se há dados para plotar
    if len(df_filtrado) == 0:
        # Retornar gráfico vazio se não houver dados
        fig = px.scatter(title='Nenhum dado disponível para os filtros selecionados')
        return fig
    
    # Verificar se a variável existe no DataFrame
    if variavel not in df_filtrado.columns:
        fig = px.scatter(title=f'Variável {variavel} não encontrada no dataset')
        return fig
    
    # Dicionário de labels para os eixos
    labels = {
        'age': 'Idade (anos)',
        'trestbps': 'Pressão Arterial em Repouso (mmHg)',
        'chol': 'Colesterol (mg/dl)',
        'thalach': 'Frequência Cardíaca Máxima (bpm)',
        'oldpeak': 'Depressão ST'
    }
    
    try:
        # Remover valores nulos da variável selecionada
        df_clean = df_filtrado.dropna(subset=[variavel, 'has_disease'])
        
        if len(df_clean) == 0:
            fig = px.scatter(title='Nenhum dado válido disponível após limpeza')
            return fig
        
        # Criar o gráfico usando plotly.express.histogram
        fig = px.histogram(
            df_clean, 
            x=variavel, 
            color='has_disease',
            title=f'Distribuição de {labels.get(variavel, variavel)}',
            labels={
                variavel: labels.get(variavel, variavel), 
                'count': 'Frequência',
                'has_disease': 'Doença Cardíaca'
            },
            color_discrete_map={0: '#27ae60', 1: '#e74c3c'},
            nbins=20
        )
        
        # Configurar layout
        fig.update_layout(
            title_font_size=16,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            legend_title_font_size=12
        )
        
    except Exception as e:
        # Em caso de erro, retornar gráfico de erro
        fig = px.scatter(title=f'Erro ao criar gráfico: {str(e)}')
        return fig
    
    return fig

@app.callback(
    Output(component_id='grafico-sexo', component_property='figure'),
    [Input(component_id='sexo-radio', component_property='value')]
)
def update_sexo_graph(sexo_filtro):
    """Gráfico de distribuição por sexo"""
    df_plot = df.copy()
    
    if sexo_filtro != 'all':
        df_plot = df_plot[df_plot['sex'] == sexo_filtro]
    
    if len(df_plot) == 0:
        fig = px.scatter(title='Nenhum dado disponível')
        return fig
    
    # Criar gráfico de pizza
    fig = px.pie(
        df_plot, 
        names='sex_label', 
        title='Distribuição por Sexo',
        color_discrete_sequence=['#e74c3c', '#3498db']
    )
    
    fig.update_layout(title_font_size=16)
    return fig

@app.callback(
    Output(component_id='grafico-correlacao', component_property='figure'),
    [Input(component_id='sexo-radio', component_property='value')]
)
def update_correlacao_graph(sexo_filtro):
    """Gráfico de correlação idade vs frequência cardíaca"""
    df_plot = df.copy()
    
    if sexo_filtro != 'all':
        df_plot = df_plot[df_plot['sex'] == sexo_filtro]
    
    # Verificar se há dados e colunas necessárias
    if len(df_plot) == 0 or 'age' not in df_plot.columns or 'thalach' not in df_plot.columns:
        fig = px.scatter(title='Dados de correlação não disponíveis')
        return fig
    
    # scatter plot
    fig = px.scatter(
        df_plot, 
        x='age', 
        y='thalach', 
        color='has_disease',
        title='Idade vs Frequência Cardíaca Máxima',
        labels={
            'age': 'Idade (anos)', 
            'thalach': 'Freq. Cardíaca Máxima (bpm)',
            'has_disease': 'Doença Cardíaca'
        },
        color_discrete_map={0: '#27ae60', 1: '#e74c3c'}
    )
    
    fig.update_layout(
        title_font_size=16,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14
    )
    return fig

@app.callback(
    Output(component_id='grafico-tipo-dor', component_property='figure'),
    [Input(component_id='sexo-radio', component_property='value')]
)
def update_tipo_dor_graph(sexo_filtro):
    """Gráfico de tipos de dor no peito"""
    df_plot = df.copy()
    
    if sexo_filtro != 'all':
        df_plot = df_plot[df_plot['sex'] == sexo_filtro]
    
    if len(df_plot) == 0:
        fig = px.scatter(title='Nenhum dado disponível')
        return fig
    
    # Preparar dados 
    #cp label chest pain
    try:
        dados_agrupados = df_plot.groupby(['cp_label', 'has_disease']).size().reset_index(name='count')
        
        fig = px.bar(
            dados_agrupados,
            x='cp_label', 
            y='count', 
            color='has_disease',
            title='Tipos de Dor no Peito',
            labels={
                'cp_label': 'Tipo de Dor', 
                'count': 'Quantidade',
                'has_disease': 'Doença Cardíaca'
            },
            color_discrete_map={0: '#27ae60', 1: '#e74c3c'}
        )
        
        fig.update_layout(
            title_font_size=16, 
            xaxis_tickangle=-45,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14
        )
        
    except Exception as e:
        # Em caso de erro, retornar gráfico simples
        fig = px.scatter(title=f'Erro ao processar dados: {str(e)}')
    
    return fig

# executar o aplicativo ---
if __name__ == '__main__':
    print("\n" + "="*60)
    print(" Iniciando aplicativo Dash...")
    print(" Acesse: http://127.0.0.1:8050")
    print(" Pressione Ctrl+C para parar o servidor")
    print("="*60)
    app.run(debug=True, port=8050)
