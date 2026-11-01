#!/usr/bin/env python3
"""
Inicializador e Carga Relacional SQLite — ADS Senac Recaps
==========================================================
Cria o banco de dados 'recap_senac.db' com schema normalizado e
migra os dados históricos das semanas (W_01 a W_12).
"""

import os
import re
import json
import sqlite3
import unicodedata
from pathlib import Path

REPO_ROOT = Path("/home/jeronimo/G-Sync/ads-senac-recaps")
DATA_DIR = REPO_ROOT / "data"
SEMANAL_DIR = REPO_ROOT / "s2_2026_2/02_semanal"
DB_PATH = DATA_DIR / "recap_senac.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

DISC_STYLES = {
    "Projeto Integrador": {"short": "PI", "color": "#a855f7", "bg": "rgba(168, 85, 247, 0.12)", "border": "rgba(168, 85, 247, 0.4)", "tag": "tag-pi", "order": 1},
    "Programação Orientada a Objetos": {"short": "POO", "color": "#f59e0b", "bg": "rgba(245, 158, 11, 0.12)", "border": "rgba(245, 158, 11, 0.4)", "tag": "tag-poo", "order": 2},
    "Linguagem C": {"short": "C", "color": "#06b6d4", "bg": "rgba(6, 182, 212, 0.12)", "border": "rgba(6, 182, 212, 0.4)", "tag": "tag-c", "order": 3},
    "Banco de Dados Relacional": {"short": "BD", "color": "#10b981", "bg": "rgba(16, 185, 129, 0.12)", "border": "rgba(16, 185, 129, 0.4)", "tag": "tag-bd", "order": 4},
    "Projeto de Extensão": {"short": "Ext", "color": "#ec4899", "bg": "rgba(236, 72, 153, 0.12)", "border": "rgba(236, 72, 153, 0.4)", "tag": "tag-ext", "order": 5},
    "Coordenação Institucional": {"short": "Coord", "color": "#38bdf8", "bg": "rgba(56, 189, 248, 0.12)", "border": "rgba(56, 189, 248, 0.4)", "tag": "tag-coord", "order": 6},
    "Ciclo Avaliativo (AV1)": {"short": "AV1", "color": "#ef4444", "bg": "rgba(239, 68, 68, 0.12)", "border": "rgba(239, 68, 68, 0.4)", "tag": "tag-av1", "order": 7},
    "Registro Acadêmico": {"short": "Aviso", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.12)", "border": "rgba(148, 163, 184, 0.4)", "tag": "tag-aviso", "order": 8},
    "Outros": {"short": "Geral", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.12)", "border": "rgba(148, 163, 184, 0.4)", "tag": "tag-outros", "order": 99},
}

DDL_SCHEMA = """
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS glossario_aulas;
DROP TABLE IF EXISTS glossario_termos;
DROP TABLE IF EXISTS aulas;
DROP TABLE IF EXISTS semanas;
DROP TABLE IF EXISTS disciplinas;
DROP TABLE IF EXISTS professores;

CREATE TABLE professores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    papel TEXT DEFAULT 'Docente Titular'
);

CREATE TABLE disciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    sigla TEXT NOT NULL,
    cor TEXT NOT NULL,
    bg_color TEXT NOT NULL,
    border_color TEXT NOT NULL,
    ordem INTEGER DEFAULT 99
);

CREATE TABLE semanas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL UNIQUE,
    codigo TEXT NOT NULL UNIQUE,
    titulo TEXT NOT NULL,
    descricao TEXT
);

CREATE TABLE aulas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    semana_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,
    professor_id INTEGER NOT NULL,
    slug_arquivo TEXT NOT NULL,
    titulo TEXT NOT NULL,
    data_aula TEXT,
    rotulo TEXT,
    conteudo_markdown TEXT NOT NULL,
    UNIQUE(semana_id, slug_arquivo),
    FOREIGN KEY (semana_id) REFERENCES semanas(id) ON DELETE CASCADE,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
    FOREIGN KEY (professor_id) REFERENCES professores(id) ON DELETE CASCADE
);

CREATE TABLE glossario_termos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    termo TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    definicao TEXT NOT NULL,
    wiki_url TEXT
);

CREATE TABLE glossario_aulas (
    termo_id INTEGER NOT NULL,
    aula_id INTEGER NOT NULL,
    PRIMARY KEY (termo_id, aula_id),
    FOREIGN KEY (termo_id) REFERENCES glossario_termos(id) ON DELETE CASCADE,
    FOREIGN KEY (aula_id) REFERENCES aulas(id) ON DELETE CASCADE
);
"""


def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)


def extract_frontmatter_and_content(md_text):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', md_text, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        content_text = match.group(2)
        meta = {}
        for line in yaml_text.splitlines():
            kv = line.split(":", 1)
            if len(kv) == 2:
                key = kv[0].strip()
                val = kv[1].strip().strip('"').strip("'")
                meta[key] = val
        return meta, content_text
    return {}, md_text


def init_database():
    print(f"📦 Inicializando banco relacional SQLite em: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(DDL_SCHEMA)
    conn.commit()

    # Inserir Disciplinas Oficiais
    print("📋 Inserindo Disciplinas padronizadas...")
    for nome, d in DISC_STYLES.items():
        cursor.execute(
            "INSERT INTO disciplinas (nome, sigla, cor, bg_color, border_color, ordem) VALUES (?, ?, ?, ?, ?, ?)",
            (nome, d["short"], d["color"], d["bg"], d["border"], d["order"])
        )
    conn.commit()

    # Ler e popular Semanas e Aulas
    print("📂 Lendo e populando Semanas (W_01 a W_12)...")
    week_folders = sorted(list(SEMANAL_DIR.glob("W_*")))
    
    total_aulas = 0
    total_termos = 0

    for folder in week_folders:
        w_code = folder.name.replace("_", "")
        w_num = int(w_code.replace("W", ""))
        config_path = folder / "week_config.json"
        
        titulo_semana = f"Semana {w_num}"
        desc_semana = ""
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                c = json.load(f)
                titulo_semana = c.get("title", titulo_semana)
                desc_semana = c.get("text", "")

        cursor.execute(
            "INSERT INTO semanas (numero, codigo, titulo, descricao) VALUES (?, ?, ?, ?)",
            (w_num, w_code, titulo_semana, desc_semana)
        )
        semana_id = cursor.lastrowid

        for md_file in sorted(folder.glob("*.md")):
            raw_text = md_file.read_text(encoding="utf-8")
            meta, body = extract_frontmatter_and_content(raw_text)

            # Normalização de Disciplina
            disc_raw = meta.get("disciplina", "Outros")
            disc_matched = "Outros"
            for k in DISC_STYLES.keys():
                if k.lower() in disc_raw.lower() or disc_raw.lower() in k.lower():
                    disc_matched = k
                    break
            if "banco de dados" in disc_raw.lower():
                disc_matched = "Banco de Dados Relacional"

            cursor.execute("SELECT id FROM disciplinas WHERE nome = ?", (disc_matched,))
            disc_row = cursor.fetchone()
            disciplina_id = disc_row[0] if disc_row else 1

            # Normalização de Professor
            prof_nome = meta.get("professor", "Corpo Docente ADS").strip()
            if prof_nome == "Vinicius":
                prof_nome = "Vinícius"
            elif prof_nome == "Haelio Márcio":
                prof_nome = "Haélio Márcio"
            cursor.execute("SELECT id FROM professores WHERE nome = ?", (prof_nome,))
            prof_row = cursor.fetchone()
            if prof_row:
                professor_id = prof_row[0]
            else:
                cursor.execute("INSERT INTO professores (nome) VALUES (?)", (prof_nome,))
                professor_id = cursor.lastrowid

            # Rótulo da aula
            num_match = re.search(r'Aula\s*(\d+)', meta.get("titulo", ""), re.IGNORECASE)
            rotulo = meta.get("rotulo", "")
            if not rotulo and num_match:
                rotulo = f"Aula {int(num_match.group(1)):02d}"

            # Inserir Aula
            cursor.execute(
                """
                INSERT INTO aulas (semana_id, disciplina_id, professor_id, slug_arquivo, titulo, data_aula, rotulo, conteudo_markdown)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    semana_id,
                    disciplina_id,
                    professor_id,
                    md_file.stem,
                    meta.get("titulo", md_file.stem),
                    meta.get("data", ""),
                    rotulo,
                    body
                )
            )
            aula_id = cursor.lastrowid
            total_aulas += 1

            # Extração de Termos do Glossário
            parts = re.split(r'##\s*Gloss[aá]rio', body, flags=re.IGNORECASE)
            if len(parts) > 1:
                glossary_content = parts[1]
                for line in glossary_content.strip().split("\n"):
                    line = line.strip()
                    if line.startswith("-") or line.startswith("*"):
                        m_term = re.match(r'[-*]\s*\*\*([^*]+)\*\*:\s*(.*)', line)
                        if m_term:
                            t = m_term.group(1).strip()
                            raw_def = m_term.group(2).strip()
                            # Extrair URL da wiki se houver
                            m_wiki = re.search(r'\[(?:Wikipedia|Fonte|Link)\]\((https?://[^\)]+)\)', raw_def)
                            wiki_url = m_wiki.group(1) if m_wiki else None
                            clean_def = re.sub(r'\[(?:Wikipedia|Fonte|Link)\]\([^\)]+\)', '', raw_def).strip()

                            slug = slugify(t)
                            cursor.execute("SELECT id FROM glossario_termos WHERE slug = ?", (slug,))
                            termo_row = cursor.fetchone()
                            if termo_row:
                                termo_id = termo_row[0]
                            else:
                                cursor.execute(
                                    "INSERT INTO glossario_termos (termo, slug, definicao, wiki_url) VALUES (?, ?, ?, ?)",
                                    (t, slug, clean_def, wiki_url)
                                )
                                termo_id = cursor.lastrowid
                                total_termos += 1

                            cursor.execute(
                                "INSERT OR IGNORE INTO glossario_aulas (termo_id, aula_id) VALUES (?, ?)",
                                (termo_id, aula_id)
                            )

    conn.commit()
    conn.close()

    print("\n" + "=" * 50)
    print("🎉 BANCO DE DADOS RELACIONAL INICIALIZADO COM SUCESSO!")
    print(f"📊 Semanas inseridas: {len(week_folders)}")
    print(f"📚 Aulas registradas: {total_aulas}")
    print(f"📖 Termos no glossário: {total_termos}")
    print("=" * 50)


if __name__ == "__main__":
    init_database()
