# Configurações globais do Terraform
terraform {
    required_version = ">= 1.5.0"

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 5.0" # Baixa a versão mais estavel e recente do plugin da aws
        }
    }
}

# Configurações do provedor aws
provider "aws" {
    region = "us-east-1"
}