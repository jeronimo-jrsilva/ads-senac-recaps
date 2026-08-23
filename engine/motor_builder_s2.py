import json
import re
import subprocess
import unicodedata
from pathlib import Path

REPO_ROOT = Path("/home/jeronimo/G-Sync/ads-senac-recaps")
SEMANAL_DIR = REPO_ROOT / "s2_2026_2/02_semanal"
OUTPUT_HTML = REPO_ROOT / "portal/Recap_Master_S2.html"
TEMPLATE_PATH = REPO_ROOT / "engine/template_master_s2.html"
CSS_PATH = REPO_ROOT / "engine/styles.css"

def process_obsidian_callouts(md):
    def replace_callout(match):
        c_type = match.group(1).lower()
        title = match.group(2).strip()
        content = match.group(3).strip()
        lines = [line.replace('>', '', 1).strip() for line in content.split('\n')]
        clean_content = '<br>'.join(lines)
        icon = "💡"
        if c_type in ["caution", "warning", "danger"]: icon = "⚠️"
        elif c_type in ["important", "todo"]: icon = "❗"
        elif c_type in ["abstract", "summary"]: icon = "📋"
        elif c_type in ["tip", "hint"]: icon = "🎯"
        if not title: title = c_type.capitalize()
        return f'<div class="callout callout-{c_type}"><div class="callout-title">{icon} {title}</div><div class="callout-content">{clean_content}</div></div>'
    pattern = r'>\s*\[!(\w+)\]\s*(.*)\n((?:>\s*.*\n?)*)'
    return re.sub(pattern, replace_callout, md)

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def convert_to_html(md):
    md = process_obsidian_callouts(md)
    def replace_pill(match):
        content = match.group(1).strip()
        return f'<span class="badge badge-poo">{content}</span>'
    md = re.sub(r'\[\[(.*?)\]\]', replace_pill, md)
    proc = subprocess.Popen(['pandoc', '-f', 'markdown', '-t', 'html'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = proc.communicate(input=md)
    return out

def build():
    print("🚀 Construindo Portal SSOT 2026.2...")
    with open(CSS_PATH, 'r', encoding='utf-8') as f:
        master_css = f.read()

    week_folders = sorted(list(SEMANAL_DIR.glob("W_*")))
    global_glossary = {}
    weeks_data = []
    all_lessons_by_id = {}
    ordered_lesson_ids = []

    for folder in week_folders:
        w_id = folder.name
        w_num = w_id.replace("W_", "")
        config_path = folder / "week_config.json"
        config = {"title": f"Semana {w_num}", "text": "Consolidação acadêmica da semana."}
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

        md_files = sorted(list(folder.glob("*.md")))
        lessons = []

        for p in md_files:
            with open(p, 'r', encoding='utf-8') as f:
                raw_text = f.read()

            date_match = re.search(r'data:\s*([\d-]+)', raw_text)
            disc_match = re.search(r'disciplina:\s*"(.*?)"', raw_text)
            prof_match = re.search(r'professor:\s*"(.*?)"', raw_text)
            tit_match = re.search(r'titulo:\s*"(.*?)"', raw_text)

            date = date_match.group(1) if date_match else "2026-08-10"
            disc = disc_match.group(1) if disc_match else "Geral"
            prof = prof_match.group(1) if prof_match else "Docente"
            titulo = tit_match.group(1) if tit_match else p.stem

            l_id = f"lesson-{w_id}-{p.stem}"
            ordered_lesson_ids.append(l_id)

            badge_cls = "badge-poo"
            disc_lower = disc.lower()
            if "c++" in disc_lower or "linguagem c" in disc_lower: badge_cls = "badge-cpp"
            elif "banco" in disc_lower or "dados" in disc_lower: badge_cls = "badge-bd"
            elif "projeto" in disc_lower: badge_cls = "badge-pi"

            parts = re.split(r'##\s*Gloss[aá]rio', raw_text, flags=re.IGNORECASE)
            if len(parts) > 1:
                matches = re.finditer(r'-\s*\*\*(.*?)\*\*[:\s]*(.*?)(?=\n-\s*\*\*|\Z)', parts[1], re.DOTALL)
                for m in matches:
                    term = m.group(1).strip()
                    norm = term.lower()
                    definition = convert_to_html(m.group(2).strip())
                    if norm not in global_glossary:
                        global_glossary[norm] = {"term": term, "def": definition, "sources": []}
                    global_glossary[norm]["sources"].append({"id": l_id, "name": f"{disc} ({date})"})

            body_md = parts[0].split('---', 2)[-1].strip()
            body_html = convert_to_html(body_md)

            lesson_obj = {
                "id": l_id,
                "title": titulo,
                "disciplina": disc,
                "professor": prof,
                "data": date,
                "badge_cls": badge_cls,
                "html": body_html,
                "week_id": w_id
            }
            lessons.append(lesson_obj)
            all_lessons_by_id[l_id] = lesson_obj

        weeks_data.append({
            "id": w_id,
            "title": config.get("title", f"Semana {w_num}"),
            "desc": config.get("text", ""),
            "lessons": lessons
        })

    nav_map = {
        "dashboard": {"label": "Dashboard", "prev": None, "next": ordered_lesson_ids[0] if ordered_lesson_ids else None}
    }
    for i, l_id in enumerate(ordered_lesson_ids):
        prev_id = ordered_lesson_ids[i - 1] if i > 0 else "dashboard"
        next_id = ordered_lesson_ids[i + 1] if i < len(ordered_lesson_ids) - 1 else "glossary"
        nav_map[l_id] = {
            "label": all_lessons_by_id[l_id]["title"],
            "prev": prev_id,
            "next": next_id
        }
    nav_map["glossary"] = {
        "label": "Glossário",
        "prev": ordered_lesson_ids[-1] if ordered_lesson_ids else "dashboard",
        "next": None
    }

    disciplines = {}
    for l_id in ordered_lesson_ids:
        l = all_lessons_by_id[l_id]
        d = l["disciplina"]
        if d not in disciplines:
            disciplines[d] = {"prof": l["professor"], "badge": l["badge_cls"], "lessons": []}
        disciplines[d]["lessons"].append(l)

    disc_cards_html = ['<div class="tracks-grid">']
    for d, data in disciplines.items():
        pill_links = []
        for l in data["lessons"]:
            parts = l["data"].split("-")
            d_str = f"{parts[2]}/{parts[1]}" if len(parts) == 3 else l["data"]
            pill_links.append(f'<a href="javascript:void(0)" onclick="showSection(\'{l["id"]}\')" class="lesson-pill-btn">{d_str} - {l["title"]}</a>')
        pills = "".join(pill_links)
        disc_cards_html.append(f'''
            <div class="track-card">
                <span class="badge {data['badge']}">{d}</span>
                <div class="track-title" style="margin-top: 10px;">{d}</div>
                <div class="track-prof">Prof. {data['prof']}</div>
                <div class="track-lessons">{pills}</div>
            </div>
        ''')
    disc_cards_html.append('</div>')
    discipline_view = "".join(disc_cards_html)

    timeline_html = []
    for w in weeks_data:
        cards_html = []
        for l in w["lessons"]:
            cards_html.append(f'''
                <div class="week-card-item" onclick="showSection('{l['id']}')">
                    <div class="item-meta">
                        <span class="badge {l['badge_cls']}">{l['disciplina']}</span> &bull; {l['data']} &bull; Prof. {l['professor']}
                    </div>
                    <div class="item-title">{l['title']}</div>
                </div>
            ''')
        timeline_html.append(f'''
            <div class="timeline-section">
                <div class="week-header">{w['title']}</div>
                <div class="week-desc">{w['desc']}</div>
                <div class="week-cards-grid">
                    {"".join(cards_html)}
                </div>
            </div>
        ''')
    timeline_content = "".join(timeline_html)

    lessons_html = []
    for l_id in ordered_lesson_ids:
        l = all_lessons_by_id[l_id]
        lessons_html.append(f'''
            <section id="{l['id']}" class="spa-section">
                <div class="lesson-card">
                    <div class="lesson-metadata">
                        <span class="badge {l['badge_cls']}">{l['disciplina']}</span>
                        <span>📅 {l['data']}</span>
                        <span>👨‍🏫 Prof. {l['professor']}</span>
                    </div>
                    <h1 style="font-size: 1.6rem; margin-bottom: 20px;">{l['title']}</h1>
                    <div class="lesson-body">
                        {l['html']}
                    </div>
                </div>
            </section>
        ''')
    lessons_content = "".join(lessons_html)

    glossary_html = []
    sorted_terms = sorted(global_glossary.keys())
    for t_key in sorted_terms:
        item = global_glossary[t_key]
        sources_html = "".join([f'<a href="javascript:void(0)" onclick="showSection(\'{s["id"]}\')" class="source-tag">{s["name"]}</a>' for s in item["sources"]])
        t_id = f"term-{slugify(item['term'])}"
        glossary_html.append(f'''
            <div class="glossary-card" id="{t_id}">
                <div class="glossary-term">{item['term']}</div>
                <div class="glossary-def">{item['def']}</div>
                <div class="glossary-sources">{sources_html}</div>
            </div>
        ''')
    glossary_content = "".join(glossary_html)

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    output = template.replace("{{MASTER_CSS}}", master_css)
    output = output.replace("{{TOTAL_WEEKS}}", str(len(weeks_data)))
    output = output.replace("{{TOTAL_LESSONS}}", str(len(ordered_lesson_ids)))
    output = output.replace("{{GLOSSARY_COUNT}}", str(len(global_glossary)))
    output = output.replace("{{DISCIPLINE_VIEW}}", discipline_view)
    output = output.replace("{{TIMELINE_CONTENT}}", timeline_content)
    output = output.replace("{{LESSONS_CONTENT}}", lessons_content)
    output = output.replace("{{GLOSSARY_CONTENT}}", glossary_content)
    output = output.replace("{{NAV_MAP}}", json.dumps(nav_map, indent=2))

    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"🎉 Recap_Master_S2.html gerado com sucesso em: {OUTPUT_HTML}")
    return True

if __name__ == "__main__":
    build()
