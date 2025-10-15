<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=30% height=30%>

# AI Project Document - Módulo 1 - FIAP

## Agentes IA Fiap

#### Nomes dos integrantes do grupo

Daniel Baião, Eric Criscuolo, Marcus Garcia, Sidney William, Hugo Rodrigues.

## Sumário

[1. Introdução](#c1)

[2. Visão Geral do Projeto](#c2)

[3. Desenvolvimento do Projeto](#c3)

[4. Resultados e Avaliações](#c4)

[5. Conclusões e Trabalhos Futuros](#c5)

[6. Referências](#c6)

[Anexos](#c7)

<br>

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto da Inteligência Artificial

A Inteligência Artificial (IA) tem desempenhado um papel crucial na modernização da agricultura, permitindo a análise de dados em tempo real, previsão de colheitas e otimização de recursos. Este projeto se insere no contexto da agricultura de precisão, utilizando IA para melhorar a eficiência e a produtividade agrícola.

### 1.1.2. Descrição da Solução Desenvolvida

A solução desenvolvida é um sistema integrado que permite o gerenciamento de dados agrícolas, incluindo o cálculo de resultados diários, previsão do momento ideal de colheita e geração de gráficos de evolução. A solução utiliza algoritmos de IA para análise preditiva e ferramentas de visualização para facilitar a tomada de decisão.

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

- Automatizar o cálculo de resultados diários com base em dados agrícolas.
- Prever o momento ideal para a colheita utilizando algoritmos de IA.
- Facilitar a visualização de dados históricos por meio de gráficos.
- Armazenar e gerenciar dados de forma eficiente em um banco de dados Oracle.

## 2.2. Público-Alvo

O público-alvo do projeto inclui agricultores, cooperativas agrícolas e empresas do setor agroindustrial que buscam otimizar suas operações e aumentar a produtividade.

## 2.3. Metodologia

A metodologia utilizada no desenvolvimento do projeto seguiu as seguintes etapas:
1. **Definição de Requisitos**: Identificação das necessidades do usuário.
2. **Desenvolvimento do Sistema**: Implementação do código Python com funcionalidades específicas.
3. **Treinamento e Teste**: Validação dos algoritmos de previsão.
4. **Integração**: Conexão com banco de dados Oracle e ferramentas de visualização.
5. **Avaliação**: Testes com usuários finais para validação da solução.

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

- **Linguagem de Programação**: Python
- **Bibliotecas**: `matplotlib`, `json`, `cx_Oracle`
- **Banco de Dados**: Oracle Database
- **Ferramentas de Desenvolvimento**: Visual Studio Code

## 3.2. Modelagem e Algoritmos

O sistema utiliza os seguintes algoritmos e processos:
- **Cálculo de Resultados**: Função `procedimento_calculo` para processar dados diários.
- **Previsão de Colheita**: Algoritmo de IA implementado na função `prever_momento_colheita`.
- **Visualização de Dados**: Geração de gráficos com a biblioteca `matplotlib`.

## 3.3. Treinamento e Teste

- **Conjuntos de Dados**: Dados históricos de produtividade agrícola.
- **Métricas de Avaliação**: Precisão das previsões e feedback dos usuários.
- **Resultados**: O sistema apresentou alta precisão na previsão do momento ideal de colheita.

# <a name="c4"></a>4. Resultados e Avaliações

## 4.1. Análise dos Resultados

Os resultados obtidos demonstraram que o sistema é capaz de:
- Processar e armazenar dados de forma eficiente.
- Prever o momento ideal de colheita com alta precisão.
- Gerar gráficos claros e informativos para análise de tendências.

# <a name="c5"></a>5. Conclusões e Trabalhos Futuros

A solução desenvolvida atingiu os objetivos propostos, oferecendo uma ferramenta eficiente para o gerenciamento de dados agrícolas. Como trabalhos futuros, propomos:
- Expansão do suporte para outros bancos de dados.
- Integração com sensores IoT para coleta automática de dados.
- Melhoria nos algoritmos de previsão para incluir mais variáveis.

# <a name="c6"></a>6. Referências

- Documentação oficial do Python: https://docs.python.org/
- Biblioteca Matplotlib: https://matplotlib.org/
- Documentação do cx_Oracle: https://cx-oracle.readthedocs.io/

# <a name="c7"></a>Anexos

## Diagramas

- Gráfico de Evolução e Projeção do Brix e Índice de Maturação da Cana:
  ![Fluxograma](Figure_1.png)

## Tabelas

- Exemplo de dados armazenados no banco de dados Oracle:
  | Data       | Resultado | Previsão de Colheita |
  |------------|-----------|----------------------|
  | 2025-10-14 | 85%       | 2025-11-01          |
