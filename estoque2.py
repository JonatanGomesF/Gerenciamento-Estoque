import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

# Conectar ao banco de dados
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="delta@1919",
        database="estoque_tintas"
    )

# Função para adicionar produto
def adicionar_produto():
    try:
        nome = entry_nome_produto.get().strip()
        descricao = entry_descricao_produto.get().strip()
        preco = float(entry_preco_produto.get())
        quantidade = int(entry_quantidade_produto.get())
        nome_fabricante = combobox_fabricante_produto.get()
        id_fabricante = fabricante_dict.get(nome_fabricante)

        if nome and descricao and id_fabricante is not None:
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO produto (nome, descricao, id_fabricante, preco, quantidade)
                VALUES (%s, %s, %s, %s, %s)
            """, (nome, descricao, id_fabricante, preco, quantidade))
            conexao.commit()
            conexao.close()
            atualizar_combobox_produtos()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
    except ValueError:
        messagebox.showerror("Erro", "Verifique os campos numéricos (preço, quantidade).")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro no banco de dados", str(err))

# Função para adicionar fabricante
def adicionar_fabricante():
    nome = entry_nome_fabricante.get().strip()
    cnpj = entry_cnpj_fabricante.get().strip()

    if nome and cnpj:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO fabricante (nome, cnpj)
            VALUES (%s, %s)
        """, (nome, cnpj))
        conexao.commit()
        conexao.close()
        atualizar_combobox_fabricantes()
        messagebox.showinfo("Sucesso", "Fabricante adicionado com sucesso!")
    else:
        messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")

# Função para carregar produtos no Combobox
def carregar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM produto")
    produtos = cursor.fetchall()
    conexao.close()
    return produtos

# Função para carregar fabricantes no Combobox
def carregar_fabricantes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM fabricante")
    fabricantes = cursor.fetchall()
    conexao.close()
    return fabricantes

# Atualizar Combobox de produtos
produto_dict = {}
def atualizar_combobox_produtos():
    global produto_dict
    produtos = carregar_produtos()
    produto_dict = {nome: pid for pid, nome in produtos}
    combobox_produto['values'] = list(produto_dict.keys())

# Atualizar Combobox de fabricantes
fabricante_dict = {}
def atualizar_combobox_fabricantes():
    global fabricante_dict
    fabricantes = carregar_fabricantes()
    fabricante_dict = {nome: fid for fid, nome in fabricantes}
    combobox_fabricante_produto['values'] = list(fabricante_dict.keys())

# Função para registrar movimentação
def registrar_movimentacao():
    nome_produto = combobox_produto.get()
    tipo = combobox_tipo.get()
    quantidade = entry_quantidade_mov.get()

    if nome_produto and tipo and quantidade:
        try:
            produto_id = produto_dict[nome_produto]
            quantidade = int(quantidade)
            conexao = conectar()
            cursor = conexao.cursor()

            # Verifica se tem estoque suficiente para saída
            if tipo == "saida":
                cursor.execute("SELECT quantidade FROM produto WHERE id = %s", (produto_id,))
                estoque_atual = cursor.fetchone()[0]
                if estoque_atual < quantidade:
                    messagebox.showerror("Erro", "Estoque insuficiente para a saída.")
                    return

            cursor.execute("""
                INSERT INTO movimentacoes (produto_id, tipo, quantidade, fabricante_id)
                VALUES (%s, %s, %s, NULL)
            """, (produto_id, tipo, quantidade))

            if tipo == "entrada":
                cursor.execute("""
                    UPDATE produto
                    SET quantidade = quantidade + %s
                    WHERE id = %s
                """, (quantidade, produto_id))
            elif tipo == "saida":
                cursor.execute("""
                    UPDATE produto
                    SET quantidade = quantidade - %s
                    WHERE id = %s
                """, (quantidade, produto_id))

            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Movimentação registrada com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
    else:
        messagebox.showerror("Erro", "Preencha todos os campos.")


# Função para excluir produto pelo ID
def excluir_produto_por_id():
    id_produto = entry_id_produto.get()
    if id_produto:
        resposta = messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o produto com ID {id_produto}?")
        if resposta:
            try:
                conexao = conectar()
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM produto WHERE id = %s", (id_produto,))
                conexao.commit()
                conexao.close()
                entry_id_produto.delete(0, tk.END)
                atualizar_combobox_produtos()  # Atualiza dropdowns se tiver
                messagebox.showinfo("Sucesso", f"Produto com ID {id_produto} excluído com sucesso!")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", str(err))
    else:
        messagebox.showerror("Erro", "Digite o ID do produto.")


def excluir_fabricante_por_id():
    id_fabricante = entry_id_fabricante.get()
    if id_fabricante:
        resposta = messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o fabricante com ID {id_fabricante}?")
        if resposta:
            try:
                conexao = conectar()
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM fabricante WHERE id = %s", (id_fabricante,))
                conexao.commit()
                conexao.close()
                entry_id_fabricante.delete(0, tk.END)
                atualizar_combobox_fabricantes()  # Se estiver usando combobox
                messagebox.showinfo("Sucesso", f"Fabricante com ID {id_fabricante} excluído com sucesso!")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", str(err))
    else:
        messagebox.showerror("Erro", "Digite o ID do fabricante.")

# Função para pesquisar produto
def pesquisar_produto():
    termo = entry_pesquisa.get().strip()
    if not termo:
        messagebox.showerror("Erro", "Digite o nome ou ID do produto para pesquisar.")
        return

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        if termo.isdigit():
            cursor.execute("SELECT * FROM produto WHERE id = %s", (int(termo),))
        else:
            cursor.execute("SELECT * FROM produto WHERE nome LIKE %s", (f"%{termo}%",))
        resultado = cursor.fetchall()
        conexao.close()

        if resultado:
            texto = ""
            for prod in resultado:
                texto += f"ID: {prod[0]}\nNome: {prod[1]}\nDescrição: {prod[2]}\nFabricante ID: {prod[3]}\nPreço: R${prod[4]:.2f}\nQuantidade: {prod[5]}\n\n"
            messagebox.showinfo("Resultado da Pesquisa", texto)
        else:
            messagebox.showinfo("Sem resultados", "Nenhum produto encontrado.")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", str(err))


        

# --- Interface Gráfica ---
root = tk.Tk()
root.title("Sistema de Estoque de Tintas")


# --- Cadastro de Produto ---
tk.Label(root, text="Cadastro de Produto", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)

tk.Label(root, text="Nome:").grid(row=1, column=0)
entry_nome_produto = tk.Entry(root)
entry_nome_produto.grid(row=1, column=1)

tk.Label(root, text="Descrição:").grid(row=2, column=0)
entry_descricao_produto = tk.Entry(root)
entry_descricao_produto.grid(row=2, column=1)

tk.Label(root, text="Preço:").grid(row=3, column=0)
entry_preco_produto = tk.Entry(root)
entry_preco_produto.grid(row=3, column=1)

tk.Label(root, text="Quantidade:").grid(row=4, column=0)
entry_quantidade_produto = tk.Entry(root)
entry_quantidade_produto.grid(row=4, column=1)

tk.Label(root, text="Fabricante:").grid(row=5, column=0)
combobox_fabricante_produto = ttk.Combobox(root, state="readonly")
combobox_fabricante_produto.grid(row=5, column=1)

tk.Button(root, text="Adicionar Produto", command=adicionar_produto).grid(row=6, column=0, columnspan=2, pady=5)

# --- Pesquisa de Produto ---
tk.Label(root, text="Pesquisar Produto (Nome ou ID):", font=("Arial", 12, "bold")).grid(row=7, column=0, columnspan=2, pady=10)
entry_pesquisa = tk.Entry(root)
entry_pesquisa.grid(row=8, column=0, columnspan=2)

tk.Button(root, text="Pesquisar", command=pesquisar_produto).grid(row=9, column=0, columnspan=2, pady=5)

# --- Cadastro de Fabricante ---
tk.Label(root, text="Cadastro de Fabricante", font=("Arial", 12, "bold")).grid(row=10, column=0, columnspan=2, pady=10)

tk.Label(root, text="Nome:").grid(row=11, column=0)
entry_nome_fabricante = tk.Entry(root)
entry_nome_fabricante.grid(row=11, column=1)

tk.Label(root, text="CNPJ:").grid(row=12, column=0)
entry_cnpj_fabricante = tk.Entry(root)
entry_cnpj_fabricante.grid(row=12, column=1)

tk.Button(root, text="Adicionar Fabricante", command=adicionar_fabricante).grid(row=13, column=0, columnspan=2, pady=5)

# --- Movimentação de Estoque ---
tk.Label(root, text="Movimentação de Estoque", font=("Arial", 12, "bold")).grid(row=14, column=0, columnspan=2, pady=10)

tk.Label(root, text="Produto:").grid(row=15, column=0)
combobox_produto = ttk.Combobox(root, state="readonly")
combobox_produto.grid(row=15, column=1)

tk.Label(root, text="Tipo (entrada/saida):").grid(row=16, column=0)
combobox_tipo = ttk.Combobox(root, state="readonly", values=["entrada", "saida"])
combobox_tipo.grid(row=16, column=1)

tk.Label(root, text="Quantidade:").grid(row=17, column=0)
entry_quantidade_mov = tk.Entry(root)
entry_quantidade_mov.grid(row=17, column=1)

tk.Button(root, text="Registrar Movimentação", command=registrar_movimentacao).grid(row=18, column=0, columnspan=2, pady=5)


# Seção de exclusão de produto
tk.Label(root, text="Exclusão de Produto", font=("Arial", 12, "bold")).grid(row=19, column=0, columnspan=2, pady=(20, 5))

tk.Label(root, text="ID do Produto:").grid(row=20, column=0, padx=5, pady=5)
entry_id_produto = tk.Entry(root)
entry_id_produto.grid(row=20, column=1, padx=5, pady=5)

tk.Button(root, text="Excluir Produto", command=excluir_produto_por_id).grid(row=21, column=0, columnspan=2, pady=10)

# Seção de exclusão de fabricante
tk.Label(root, text="Exclusão de Fabricante", font=("Arial", 12, "bold")).grid(row=22, column=0, columnspan=2, pady=(20, 5))

tk.Label(root, text="Id_fabricante:").grid(row=23, column=0, padx=5, pady=5)
entry_id_fabricante = tk.Entry(root)
entry_id_fabricante.grid(row=23, column=1, padx=5, pady=5)

tk.Button(root, text="Excluir Fabricante", command=excluir_fabricante_por_id).grid(row=24, column=0, columnspan=2, pady=10)

# Iniciar Combobox com dados do banco
atualizar_combobox_produtos()
atualizar_combobox_fabricantes()

# Loop da aplicação
root.mainloop()





