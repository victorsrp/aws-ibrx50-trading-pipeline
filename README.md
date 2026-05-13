# Projeto Data Lakehouse Serverless

## 📖 Sobre o Projeto

Este projeto implementa um **Data Lakehouse Serverless** na AWS para coletar e processar dados históricos e diários do **IBrX 50**. O objetivo é automatizar a identificação de oportunidades de swing trade utilizando as regras de negócio dos **Setups 9.x de Larry Williams**, oferecendo uma ferramenta técnica para suporte à decisão baseada em dados reais de mercado.

---

### 🎯 O Problema

Atualmente, investidores que utilizam métodos quantitativos como os de Larry Williams enfrentam barreiras operacionais:
* **Processamento Manual:** Analisar individualmente os 50 ativos do IBrX 50 em busca de viradas de média (9.1) ou correções (9.2/9.3) consome tempo e é passível de erro humano.
* **Falta de Histórico Confiável:** É difícil realizar backtesting de estratégias sem uma base de dados limpa, padronizada e enriquecida com indicadores como volume médio e MME9.
* **Custo de Infraestrutura:** Manter ferramentas de análise ligadas 24/7 pode gerar custos altos de nuvem se não forem adotadas estratégias serverless e de FinOps.

---

### ✨ A Solução

Este projeto resolve esses problemas através de um pipeline de dados orquestrado pelo **AWS Step Functions**, seguindo a **Arquitetura Medalhão** (Bronze, Silver, Gold) para criar uma fonte única da verdade para dados financeiros. A solução automatiza desde a extração via API até a detecção de gatilhos no Athena, permitindo o acompanhamento diário de trades e stops de forma eficiente e de baixo custo.

---

## 🏛️ Arquitetura de Dados
![Data Architecture](docs/design_arquitetura.png)
A arquitetura é dividida em três camadas lógicas para garantir rastreabilidade e performance:

* 🥉 **Camada Bronze:** Contém os dados brutos (JSON/CSV) extraídos da API financeira via AWS Lambda. O foco aqui é a preservação do dado original para auditoria e reprocessamento.

* 🥈 **Camada Silver:** Camada intermediária onde os dados são limpos e padronizados. Aqui, utilizamos **AWS Glue (PySpark)** para realizar o cast de tipos e armazenar os dados em formato **Apache Iceberg**, otimizando consultas futuras.

* 🥇 **Camada Gold:** Camada final com as regras de negócio aplicadas. Através de **Window Functions** no SQL/PySpark, calculamos a MME9 e detectamos os setups de Larry Williams, além de monitorar os níveis de Stop Loss.

> Para um detalhamento visual completo, consulte o **[Diagrama da Arquitetura](docs/design_arquitetura.png)**.

---

## 📁 Estrutura do Projeto

O repositório está organizado com foco em scripts SQL, facilitando a implantação e manutenção do Data Warehouse.
```
├── datasets/                                        # Conjuntos de dados brutos usados no projeto (dados de ERP e CRM)
├── docs/
│   ├── data_architecture.drawio                     # Arquivo Draw.io mostrando a arquitetura do projeto
|   ├── data_layer.png                               # Ilustração da camada de dados, mostrando os níveis Bronze, Silver e Gold
|   ├── business_rules.md                            # Documento descrevendo as regras de negócio aplicadas durante o processo de transformação de dados
|   ├── integration_model.drawio                     # Diagrama mostrando o modelo de integração entre fontes e camadas do Data Warehouse
|   ├── data_mart.drawio                             # Arquivo Draw.io com os modelos de dados (esquema estrela)
|   ├── data_catalog.md                              # Catálogo dos conjuntos de dados, incluindo descrições de campos e metadados
|   ├── data_flow.drawio                             # Arquivo Draw.io com o diagrama de fluxo de dados
│   ├── padroes_nomenclatura.md                      # Diretrizes consistentes de nomenclatura para tabelas, colunas e arquivos
│   └── ...
├── scripts/
│   ├── bronze/                                      # Scripts para carga de dados na camada Bronze
│   ├── silver/                                      # Scripts para limpeza e transformação (Bronze -> Silver)
│   └── gold/                                        # Scripts para modelagem e agregação (Silver -> Gold)
├── tests/                                           # Scripts para testes de qualidade de dados
├── README.md                                        # Visão geral do projeto e instruções
├── LICENSE                                          # Informações de licença do repositório
└── .gitignore                                       # Arquivos e diretórios ignorados pelo Git
```

---

## 🚀 Começando

Pré-requisitos
* Conta ativa na **AWS** (utiliza serviços elegíveis ao Free Tier).
* **Terraform** instalado localmente para provisionamento.
* **AWS CLI** configurado com permissões de administrador.
  
---

## 📄 Documentação Adicional

A documentação detalhada do projeto é fundamental para a sua manutenção e evolução.

* **[Regras de Negócios](docs/business_rules.md)**: Documento que define as regras e validações de negócio que garantem a integridade e consistência dos dados no projeto.
* **[Convenções de Nomenclatura](docs/padroes_nomenclatura.md)**: Descreve todos os padrões de nomenclatura para tabelas, colunas e outros objetos do Data Warehouse.
* **[Diagrama da Arquitetura](docs/design_arquitetura.png)**: Arquivo editável do Draw.io com o diagrama completo da arquitetura de dados.
* **[Camadas do Data Warehouse](docs/data_layer.png)**: Arquivo editável do Draw.io com o diagrama completo das camadas do schema medalhão.
* **[Data Catalog](docs/data_catalog.md)**: Documento que descreve e organiza os conjuntos de dados do projeto, detalhando suas origens, estrutura, finalidade e relações no ecossistema de dados.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Se você tiver sugestões para melhorar o projeto, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.
