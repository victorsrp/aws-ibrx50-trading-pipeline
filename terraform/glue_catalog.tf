# cria o banco de dados logico no aws glue data catalog
resource "aws_glue_catalog_database" "db_trading" {
    name        = "db_trading_larry_williams"
    description = "Catalogo de dados para os setups de Larry Williams no IBrX50"
}