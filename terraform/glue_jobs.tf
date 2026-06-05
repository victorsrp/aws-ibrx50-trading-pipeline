# criando IAM Role para o aws glue
resource "aws_iam_role" "glue_role" {
    name = "aws-glue-trading-execution-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "glue.amazonaws.com"
                }
            }
        ]
    })
}

# vincula a permissão de adm temporariamente para facilitar o desenvolvimento do mvp
resource "aws_iam_role_policy_attachment" "glue_admin" {
    role       = aws_iam_role.glue_role.name
    policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

# declaração do aws glue job para processamento da camada silver
resource "aws_glue_job" "process_silver" {
    name         = "glue-job-incremental-silver"
    role_arn     = aws_iam_role.glue_role.arn
    glue_version = "4.0"

    # define o uso minimo de recursos para o free tier
    worker_type       = "G.025X" # tipo de worker de baixo custo para pequenos volumes de dados
    number_of_workers = 2        # minimo de workers possiveis para evitar cobrancas pesadas

    command {
        name            = "glueetl"
        script_location = "s3://${aws_s3_bucket.bronze.id}/scripts/transform_bronze_to_silver.py"
        python_version  = "3"
    }
    # parametros necessarios para ativar o suporte ao formato apache iceberg e job bookmarks
    default_arguments = {
        "--job-bookmark-option"              = "job-bookmark-enable" # evita processar dados repetidos
        "--datalake-formats"                 = "iceberg"              # ativa o conector nativo do Apache Iceberg
        "--conf"                             = "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
    }
}