-- SCRIPT DDL: BANCO DE DADOS NUTRICIONAL E BIOMÉTRICO
-- Ordem de criação respeitando as dependências de FK (Chaves Estrangeiras)

-- 1. TABELA DE PESSOAS / USUÁRIOS (Sem dependências)
CREATE TABLE PESSOA (
    id_pessoa INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_pessoa VARCHAR(100) NOT NULL,
    email_pessoa VARCHAR(100) NOT NULL UNIQUE,
    senha_pessoa VARCHAR(255) NOT NULL,
    data_nasc DATE NOT NULL,
    crm_nutricionista VARCHAR(20) DEFAULT NULL
);

-- 2. TABELA DE MOTIVOS / CONDICOES DE SAÚDE (Sem dependências)
CREATE TABLE MOTIVO_SAUDE (
    id_motivo INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_motivo VARCHAR(100) NOT NULL UNIQUE
);

-- 3. TABELA DE INGREDIENTES (Sem dependências)
CREATE TABLE INGREDIENTE (
    id_ingrediente INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_ingrediente VARCHAR(100) NOT NULL UNIQUE,
    unidade_padrao VARCHAR(30) NOT NULL
);

-- 4. TABELA DE RECEITAS (Depende de PESSOA para autor)
CREATE TABLE RECEITA (
    id_receita INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_autor INT NOT NULL,
    titulo_receita VARCHAR(150) NOT NULL,
    modo_preparo TEXT NOT NULL,
    tempo_preparo INT NOT NULL CHECK (tempo_preparo > 0),
    CONSTRAINT fk_receita_pessoa FOREIGN KEY (id_autor) REFERENCES PESSOA(id_pessoa) ON DELETE CASCADE
);

-- 5. TABELA ASSOCIATIVA: USUÁRIO E MOTIVOS DE SAÚDE (Depende de PESSOA e MOTIVO_SAUDE)
CREATE TABLE NECESSIDADE (
    id_pessoa INT NOT NULL,
    id_motivo INT NOT NULL,
    PRIMARY KEY (id_pessoa, id_motivo),
    CONSTRAINT fk_necessidade_pessoa FOREIGN KEY (id_pessoa) REFERENCES PESSOA(id_pessoa) ON DELETE CASCADE,
    CONSTRAINT fk_necessidade_motivo FOREIGN KEY (id_motivo) REFERENCES MOTIVO_SAUDE(id_motivo) ON DELETE CASCADE
);

-- 6. TABELA DE ACOMPANHAMENTO FÍSICO / HISTÓRICO (Depende de PESSOA)
CREATE TABLE ACOMPANHAMENTO_FISICO (
    id_acompanhamento INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pessoa INT NOT NULL,
    peso DECIMAL(5,2) NOT NULL CHECK (peso > 0),
    altura DECIMAL(3,2) NOT NULL CHECK (altura > 0),
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_acompanhamento_pessoa FOREIGN KEY (id_pessoa) REFERENCES PESSOA(id_pessoa) ON DELETE CASCADE
);

-- 7. TABELA ASSOCIATIVA: RECEITA E INGREDIENTES (Depende de RECEITA e INGREDIENTE)
CREATE TABLE RECEITA_INGREDIENTE (
    id_receita INT NOT NULL,
    id_ingrediente INT NOT NULL,
    quantidade DECIMAL(6,2) NOT NULL CHECK (quantidade > 0),
    unidade_medida VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_receita, id_ingrediente),
    CONSTRAINT fk_rec_ing_receita FOREIGN KEY (id_receita) REFERENCES RECEITA(id_receita) ON DELETE CASCADE,
    CONSTRAINT fk_rec_ing_ingrediente FOREIGN KEY (id_ingrediente) REFERENCES INGREDIENTE(id_ingrediente) ON DELETE RESTRICT
);

-- 8. TABELA ASSOCIATIVA: RECEITA E MOTIVOS DE SAÚDE (Depende de RECEITA e MOTIVO_SAUDE)
CREATE TABLE MOTIVO_RECEITA (
    id_receita INT NOT NULL,
    id_motivo INT NOT NULL,
    PRIMARY KEY (id_receita, id_motivo),
    CONSTRAINT fk_mot_rec_receita FOREIGN KEY (id_receita) REFERENCES RECEITA(id_receita) ON DELETE CASCADE,
    CONSTRAINT fk_mot_rec_motivo FOREIGN KEY (id_motivo) REFERENCES MOTIVO_SAUDE(id_motivo) ON DELETE CASCADE
);

-- 9. TABELA DE CARDÁPIO / PLANEJAMENTO (Depende de PESSOA e RECEITA)
CREATE TABLE CARDAPIO (
    id_cardapio INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_pessoa INT NOT NULL,
    id_receita INT NOT NULL,
    data_refeicao DATE NOT NULL,
    CONSTRAINT fk_cardapio_pessoa FOREIGN KEY (id_pessoa) REFERENCES PESSOA(id_pessoa) ON DELETE CASCADE,
    CONSTRAINT fk_cardapio_receita FOREIGN KEY (id_receita) REFERENCES RECEITA(id_receita) ON DELETE CASCADE
);