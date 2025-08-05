# Dashboard de Análise de Doenças Cardíacas

## Instruções de Instalação

### 1. Criar ambiente virtual
```bash
python -m venv meu_venv
```

### 2. Ativar ambiente virtual

**Windows (PowerShell):**
```bash
.\meu_venv\Scripts\activate
```

**Windows (CMD):**
```bash
meu_venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source meu_venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar aplicação
```bash
python app.py
```

### 5. Acessar dashboard
Abra seu navegador e acesse: http://127.0.0.1:8050

## Descrição do Projeto

Este dashboard interativo analisa dados de doenças cardíacas do UCI ML Repository, oferecendo:

- **Visualizações interativas** com gráficos de distribuição, correlação e análise por categorias
- **Filtros dinâmicos** por sexo e variáveis clínicas
- **Interface intuitiva** com explicações detalhadas das variáveis médicas
- **Análise em tempo real** de 303 registros de pacientes

## Estrutura do Projeto

```
dashweb/
├── app.py              # Aplicação principal do Dash
├── requirements.txt    # Lista de dependências
├── README.md          # Este arquivo
└── meu_venv/          # Ambiente virtual (criado após instalação)
```

## Bibliotecas Utilizadas

- **Dash**: Framework para criação de dashboards web interativos
- **Plotly**: Biblioteca para gráficos interativos e visualizações
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação científica e arrays
- **Scikit-learn**: Machine learning e análise de dados
- **UCIMLRepo**: Acesso ao repositório de datasets do UCI
