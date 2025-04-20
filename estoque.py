import mysql.connector

# Conectar ao MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user="root",  # Substitua pelo seu usuário do MySQL
    password="",  # Substitua pela sua senha do MySQL
    database="estoque_db"  # Nome do banco de dados
)

cursor = conexao.cursor()

# Função para exibir dados de uma tabela
def exibir_dados_tabela(tabela):
    cursor.execute(f"SELECT * FROM {tabela}")
    dados = cursor.fetchall()
    
    if dados:
        print(f"Dados da tabela {tabela}:")
        for linha in dados:
            print(linha)
    else:
        print(f"Nenhum dado encontrado na tabela {tabela}.")

# Exibindo dados das tabelas 'produtos', 'fornecedores' e 'movimentacoes'
exibir_dados_tabela('produtos')
exibir_dados_tabela('fornecedores')
exibir_dados_tabela('movimentacoes')

# Fechar a conexão
cursor.close()
conexao.close()
