print("🚨 [PASSO 1] Script iniciado com sucesso!")

import datetime
import json
import sys

print("🚨 [PASSO 2] Importações básicas concluídas. Carregando bibliotecas pesadas...")

try:
    import boto3
    print("   -> Boto3 (AWS) carregado com sucesso!")
    import yfinance as yf
    print("   -> YFinance (Mercado) carregado com sucesso!")
    import pandas as pd
    print("   -> Pandas (Dados) carregado com sucesso!")
except ImportError as e:
    print(f"❌ [ERRO DE IMPORTAÇÃO] Faltando biblioteca: {str(e)}")
    print("Execute no terminal: pip install yfinance boto3 pandas")
    sys.exit(1)

# ⚠️ IMPORTANTE: Use o nome exato do seu bucket Bronze do Terraform!
BUCKET_BRONZE = "ibrx50-datalake-bronze-vctrpereiraws"

TICKERS = [
    "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "ABEV3.SA",
    "BBAS3.SA", "B3SA3.SA", "WEGE3.SA", "MGLU3.SA", "GGBR4.SA"
]

def extrair_e_salvar_historico():
    print("🚨 [PASSO 3] Iniciando conexão com a AWS via Boto3...")
    try:
        s3_client = boto3.client('s3')
        print("   -> Conexão com o cliente S3 estabelecida!")
    except Exception as e:
        print(f"❌ Erro ao conectar com a AWS: {str(e)}")
        return

    data_fim = datetime.date.today()
    data_inicio = data_fim - datetime.timedelta(days=365)
    
    print(f"🚨 [PASSO 4] Solicitando dados ao Yahoo Finance de {data_inicio} até {data_fim}...")

    for ticker in TICKERS:
        try:
            print(f"📥 Tentando baixar: {ticker}")
            acao = yf.Ticker(ticker)
            # O parâmetro proxy=None garante que ele não tente usar proxies travados
            historico_df = acao.history(start=data_inicio, end=data_fim, interval="1d")
            
            if historico_df.empty:
                print(f"⚠️ Nenhum dado retornado para {ticker}.")
                continue
                
            print(f"   -> {ticker} baixado ({len(historico_df)} linhas). Formatando...")
            historico_df = historico_df.reset_index()
            historico_df['Date'] = historico_df['Date'].dt.strftime('%Y-%m-%d')
            dados_json = historico_df.to_json(orient="records")
            
            nome_arquivo = f"bronze/ingestion_date={data_fim}/{ticker}_history.json"
            
            print(f"   -> Enviando {ticker} para o S3...")
            s3_client.put_object(
                Bucket=BUCKET_BRONZE,
                Key=nome_arquivo,
                Body=dados_json,
                ContentType="application/json"
            )
            print(f"✅ {ticker} salvo no S3 Bronze!")
            
        except Exception as e:
            print(f"❌ Erro no ativo {ticker}: {str(e)}")

if __name__ == "__main__":
    extrair_e_salvar_historico()