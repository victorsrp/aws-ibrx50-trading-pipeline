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
├── docs/
│   └── ...
├── src/
│   ├── glue/
│   ├── lambda/
│   └── sql/
├── tests/                                           # Scripts para testes de qualidade de dados
├── terraform/
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

**Em contrução**

---

## 🤝 Contribuição

Contribuições são bem-vindas! Se você tiver sugestões para melhorar o projeto, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.
