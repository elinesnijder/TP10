import sqlite3

#base de daos
sql = """
CREATE TABLE 
    Clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        morada TEXT NOT NULL,
        telefone TEXT NOT NULL
    );
    
CREATE TABLE
    Hamburguers (
        nome_hamburguer TEXT PRIMARY KEY,
        ingredientes TEXT NOT NULL
    );
    
CREATE TABLE
    Pedidos (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        nome_hamburguer TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        tamanho TEXT CHECK (tamanho IN ('infantil', 'normal', 'duplo')),
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        valor_total REAL NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
        FOREIGN KEY (nome_hamburguer) REFERENCES hamburguers(nome_hamburguer)
    );
"""

data_hamburguers = [
    ('Hamburguer Simples', 'Pão, Carne de Vaca, Pickles, Cebola, Ketchup, Mostarda'),
    ('Cheeseburguer', 'Pão, Carne de Vaca, Queijo Cheddar, Pickles, Cebola, Ketchup, Mostarda'),
    ('Big Mac', 'Pão, Carne de Vaca, Queijo Cheddar, Pickles, Alface, Molho Irresistível'),
    ('CBO', 'Pão Macio, Panado de Frango, Cebola Estaladiça, Bacon, Queijo, Bacon'),
    ('McRoyal Bacon', 'Pão, Carne de Vaca, Bacon, Molho McBacon'),
    ('McRoyal Cheese', 'Pão, Queijo Cheddar, Pickles, Cebola, Ketchup, Mostarda'),
    ('Mc Chicken', 'Pão, Filete de Frango, Alface, Maionese')
]

with sqlite3.connect('hamburgueria.db') as conn:
    cursor = conn.cursor()
    cursor.executescript(sql)
    
    cursor.executemany('INSERT INTO Hamburguers (nome_hamburguer, ingredientes) VALUES (?,?)', data_hamburguers)
    conn.commit()