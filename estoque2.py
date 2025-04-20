import mysql.connector
import tkinter as tk
from tkinter import messagebox


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="",  
        database="estoque_db"
    )


def adicionar_produto():
    nome = entry_nome_produto.get()
    descricao = entry_descricao_produto.get()
    categoria = entry_categoria_produto.get()
    preco = entry_preco_produto.get()
    quantidade = entry_quantidade_produto.get()

    if nome and preco and quantidade:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO produtos (nome, descricao, categoria, preco, quantidade)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, descricao, categoria, preco, quantidade))
        conexao.commit()
        conexao.close()
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")

# Função para adicionar um fornecedor
def adicionar_fornecedor():
    nome = entry_nome_fornecedor.get()
    contato = entry_contato_fornecedor.get()

    if nome and contato:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO fornecedores (nome, contato)
            VALUES (%s, %s)
        """, (nome, contato))
        conexao.commit()
        conexao.close()
        messagebox.showinfo("Sucesso", "Fornecedor adicionado com sucesso!")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")

# Função para adicionar uma movimentação
def adicionar_movimentacao():
    produto_id = entry_produto_id_movimentacao.get()
    tipo = entry_tipo_movimentacao.get().lower()
    quantidade = entry_quantidade_movimentacao.get()

    if produto_id and tipo and quantidade:
        try:
            quantidade = int(quantidade)
            conexao = conectar()
            cursor = conexao.cursor()

            # Registrar movimentação
            cursor.execute("""
                INSERT INTO movimentacoes (produto_id, tipo, quantidade)
                VALUES (%s, %s, %s)
            """, (produto_id, tipo, quantidade))

            # Atualizar a quantidade na tabela produtos
            if tipo == "entrada":
                cursor.execute("""
                    UPDATE produtos
                    SET quantidade = quantidade + %s
                    WHERE id = %s
                """, (quantidade, produto_id))
            elif tipo == "saida":
                cursor.execute("""
                    UPDATE produtos
                    SET quantidade = quantidade - %s
                    WHERE id = %s
                """, (quantidade, produto_id))
            else:
                messagebox.showerror("Erro", "Tipo de movimentação inválido. Use 'entrada' ou 'saida'.")
                conexao.rollback()
                return

            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Movimentação registrada e estoque atualizado com sucesso!")

        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")



# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Cadastro de Estoque")

# Tab de produtos
tk.Label(root, text="Cadastro de Produto").grid(row=0, column=0, columnspan=2)

tk.Label(root, text="Nome:").grid(row=1, column=0)
entry_nome_produto = tk.Entry(root)
entry_nome_produto.grid(row=1, column=1)

tk.Label(root, text="Descrição:").grid(row=2, column=0)
entry_descricao_produto = tk.Entry(root)
entry_descricao_produto.grid(row=2, column=1)

tk.Label(root, text="Categoria:").grid(row=3, column=0)
entry_categoria_produto = tk.Entry(root)
entry_categoria_produto.grid(row=3, column=1)

tk.Label(root, text="Preço:").grid(row=4, column=0)
entry_preco_produto = tk.Entry(root)
entry_preco_produto.grid(row=4, column=1)

tk.Label(root, text="Quantidade:").grid(row=5, column=0)
entry_quantidade_produto = tk.Entry(root)
entry_quantidade_produto.grid(row=5, column=1)

tk.Button(root, text="Adicionar Produto", command=adicionar_produto).grid(row=6, column=0, columnspan=2)

# Tab de fornecedores
tk.Label(root, text="Cadastro de Fornecedor").grid(row=7, column=0, columnspan=2)

tk.Label(root, text="Nome:").grid(row=8, column=0)
entry_nome_fornecedor = tk.Entry(root)
entry_nome_fornecedor.grid(row=8, column=1)

tk.Label(root, text="Contato:").grid(row=9, column=0)
entry_contato_fornecedor = tk.Entry(root)
entry_contato_fornecedor.grid(row=9, column=1)

tk.Button(root, text="Adicionar Fornecedor", command=adicionar_fornecedor).grid(row=10, column=0, columnspan=2)

# Tab de movimentações
tk.Label(root, text="Cadastro de Movimentação").grid(row=11, column=0, columnspan=2)

tk.Label(root, text="Produto ID:").grid(row=12, column=0)
entry_produto_id_movimentacao = tk.Entry(root)
entry_produto_id_movimentacao.grid(row=12, column=1)

tk.Label(root, text="Tipo (entrada/saida):").grid(row=13, column=0)
entry_tipo_movimentacao = tk.Entry(root)
entry_tipo_movimentacao.grid(row=13, column=1)

tk.Label(root, text="Quantidade:").grid(row=14, column=0)
entry_quantidade_movimentacao = tk.Entry(root)
entry_quantidade_movimentacao.grid(row=14, column=1)

tk.Button(root, text="Adicionar Movimentação", command=adicionar_movimentacao).grid(row=15, column=0, columnspan=2)

root.mainloop()
