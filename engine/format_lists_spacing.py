import re
from pathlib import Path

REPO_ROOT = Path("/home/jeronimo/G-Sync/ads-senac-recaps")
TARGET_DIRS = [
    REPO_ROOT / "s2_2026_2/02_semanal",
    REPO_ROOT / "s2_2026_2/01_estruturadas"
]

def format_markdown_lists(text: str) -> str:
    lines = text.splitlines()
    output = []
    
    in_list = False
    is_list_item = lambda l: bool(re.match(r'^\s*([-*]|\d+\.)\s+', l))
    
    for i, line in enumerate(lines):
        curr_is_list = is_list_item(line)
        
        # Início de uma lista
        if curr_is_list and not in_list:
            # Se a linha anterior não estiver vazia, adiciona uma linha em branco
            if output and output[-1].strip() != "":
                output.append("")
            in_list = True
        
        # Fim de uma lista
        elif not curr_is_list and in_list and line.strip() != "":
            # Adiciona uma linha em branco antes do próximo conteúdo não-lista
            if output and output[-1].strip() != "":
                output.append("")
            in_list = False
        elif line.strip() == "" and in_list:
            # Linha em branco encontrada, verifica se o próximo é lista ou não
            next_is_list = False
            for future_line in lines[i+1:]:
                if future_line.strip() == "":
                    continue
                if is_list_item(future_line):
                    next_is_list = True
                break
            if not next_is_list:
                in_list = False
        
        output.append(line)
        
    return "\n".join(output).strip() + "\n"

count = 0
for tdir in TARGET_DIRS:
    for md_file in tdir.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        formatted = format_markdown_lists(content)
        md_file.write_text(formatted, encoding="utf-8")
        count += 1

print(f"✅ Formatação de listas com espaçamento isolado aplicada em {count} arquivos!")
