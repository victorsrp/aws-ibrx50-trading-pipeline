# camada bronze - dados brutos
resource "aws_s3_bucket" "bronze" {
    bucket        = "ibrx50-datalake-bronze-vctrpereiraws"
    force_destroy = true # Permite apagar o bucket quando for deletar o projeto

    tags = {
        Project     = "larry-williams-pipeline"
        Environment = "Dev"
    }
}

# camada silver - dados limpos
resource "aws_s3_bucket" "silver" {
    bucket = "ibrx50-datalake-silver-vctrpereiraaws"
    force_destroy = true

    tags = {
        Project     = "larry-williams-pipeline"
        Environment = "Dev"
    }
}
# camada Gold - sinais e estados de trades
resource "aws_s3_bucket" "gold" {
    bucket        = "ibrx50-datalake-gold-vctrpereiraws"
    force_destroy = true

    tags = {
        Project     = "larry-williams-pipeline"
        Environment = "Dev"
    }
}