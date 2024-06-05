import sqlite3

#base de daos
sql = """
CREATE TABLE 
    Clientes (
        id_cliente INTEGER PRIMERY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        morada TEXT NOT NULL,
        telefone TEXT NOT NULL
    );
    
CREATE TABLE
    Hamburguers (
        nome_hamburguer TEXT PRIMARY KEY,
        indredientes TEXT NOT NULL
    );
    
CREATE TABLE
    Pedidos (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        nome_hamburguer TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        tamanho TEXT CHECK (tamanho IN ("infantil", "normal", "duplo")),
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        valor_total REAL NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
        FOREIGN KEY (nome_hamburguer) REFERENCES hamburgueres(nome_hamburguer)
    );
"""

with sqlite3.connect("hamburgueria.db") as conn:
    cursor = conn.cursor()
    cursor.executescript(sql)