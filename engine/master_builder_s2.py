import calendar
import json
import re
import subprocess
import unicodedata
from pathlib import Path
from datetime import datetime
import sys

# Paths
REPO_ROOT = Path("/home/jeronimo/G-Sync/ads-senac-recaps")
SEMANAL_DIR = REPO_ROOT / "s2_2026_2/02_semanal"
OUTPUT_HTML = REPO_ROOT / "portal/Recap_Master_S2.html"
TEMPLATE_PATH = REPO_ROOT / "engine/template_master_s2.html"
CSS_SNIPPET = Path("/home/jeronimo/G-Sync/MultiPurpose/90_Sistema/98_Recursos/snippets/master_styles.css")

MONTH_NAMES = {8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
WEEKDAYS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

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

def normalize_sort(text):
    return "".join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)).lower()

def sanitize_glossary_def(html_text):
    html_text = re.sub(r'\[Wikip[eé]dia\]\(.*?\)', '', html_text, flags=re.IGNORECASE)
    html_text = re.sub(r'<a\s+[^>]*wikipedia\.org[^>]*>.*?</a>', '', html_text, flags=re.IGNORECASE)
    html_text = re.sub(r'Wikip[eé]dia', '', html_text, flags=re.IGNORECASE)
    html_text = re.sub(r'\[\s*\]|\(\s*\)', '', html_text)
    html_text = re.sub(r'\.\s*\.', '.', html_text)
    html_text = re.sub(r'\s+\.', '.', html_text)
    return html_text.strip()

def convert_to_html(md):
    md = process_obsidian_callouts(md)
    def replace_pill(match):
        content = match.group(1).strip()
        if content.lower().startswith("dica:"): return f'<span class="text-dica">{content}</span>'
        cls = "concept-pill"
        if content.lower().startswith("ref:"): cls += " pill-ref"
        elif content.lower().startswith("importante:"): cls += " pill-importante"
        return f'<span class="{cls}">{content}</span>'
    md = re.sub(r'\[\[(.*?)\]\]', replace_pill, md)
    proc = subprocess.Popen(['pandoc', '-f', 'markdown', '-t', 'html', '--highlight-style=tango'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = proc.communicate(input=md)
    def inject_lang(match):
        div_open, lang = match.group(1), match.group(2)
        return f'<div {div_open} class="sourceCode {lang}" data-lang="{lang}"><pre\nclass="sourceCode {lang}"'
    out = re.sub(r'<div (.*?)class="sourceCode".*?>\s*<pre\s+class="sourceCode (\w+)"', inject_lang, out, flags=re.DOTALL)
    out = out.replace('<h2>', '<br><hr /><br><h2>')
    for tag in ['</p>', '</div>', '</table>', '</ol>', '</ul>']:
        out = out.replace(tag, f'{tag}<div class="vertical-spacer"></div>')
    return out.replace('<div class="vertical-spacer"></div><div class="vertical-spacer"></div>', '<div class="vertical-spacer"></div>')

def linkify(html, glossary_list):
    if not glossary_list: return html
    sorted_g = sorted(glossary_list, key=lambda x: len(x['term']), reverse=True)
    term_map = {normalize_sort(item['term']): item for item in sorted_g}
    pattern_string = r'(?<![a-zA-Z0-9])(' + '|'.join([re.escape(item['term']) for item in sorted_g]) + r')(?![a-zA-Z0-9])'
    pattern = re.compile(pattern_string, re.IGNORECASE)
    def replace_callback(match):
        term_text = match.group(1)
        item = term_map.get(normalize_sort(term_text))
        return f'<a href="#term-{slugify(item["term"])}" class="term-link">{term_text}</a>' if item else term_text
    code_blocks = []
    def save_code(match):
        code_blocks.append(match.group(0))
        return f"__CODE_PLACEHOLDER_{len(code_blocks)-1}__"
    html = re.sub(r'<(pre|code|a).*?>.*?</\1>', save_code, html, flags=re.DOTALL)
    parts = re.split(r'(<[^>]+>)', html)
    for i in range(len(parts)):
        if not parts[i].startswith('<'): parts[i] = pattern.sub(replace_callback, parts[i])
    html = "".join(parts)
    for i, block in enumerate(code_blocks): html = html.replace(f"__CODE_PLACEHOLDER_{i}__", block)
    return html

def get_label(num):
    if str(num).isdigit(): return f"Aula {num}"
    return num

def build():
    print(f"🚀 Invocando Motor Master S2 (2026.2)...")
    
    # Template HTML base
    tpl = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recap | ADS 2026.2</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
{{MASTER_CSS}}
    </style>
</head>
<body>
    <div class="main-container">
        <!-- Header & Semester Switcher -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 10px 0; border-bottom: 1px solid var(--border);">
            <div style="font-weight: 800; font-size: 1.1rem; color: #fff; letter-spacing: 1px;">
                🎓 ADS SENAC <span style="color: var(--accent); font-size: 0.8rem; border: 1px solid var(--accent); padding: 2px 8px; border-radius: 6px; margin-left: 5px;">2026.2</span>
            </div>
            <div style="display: flex; gap: 8px;">
                <a href="Recap_Master_S1.html" style="text-decoration: none; padding: 6px 14px; border-radius: 8px; font-size: 0.75rem; font-weight: 700; color: #888; border: 1px solid #333; background: #161616;">2026.1</a>
                <a href="Recap_Master_S2.html" style="text-decoration: none; padding: 6px 14px; border-radius: 8px; font-size: 0.75rem; font-weight: 700; color: #000; background: var(--accent); border: 1px solid var(--accent);">2026.2</a>
            </div>
        </div>

        <nav class="weekly-timeline">
            <button id="nav-home" class="info-pill active" onclick="showSection('dashboard')" title="Início">🏠</button>
            <button id="nav-prev" class="day-btn" onclick="goPrev()" style="display:flex;">‹</button>
            <div id="nav-context" class="info-pill" style="min-width: 200px; cursor: default;">Dashboard</div>
            <button id="nav-next" class="day-btn" onclick="goNext()" style="display:flex;">›</button>
            <button id="nav-glossary" class="info-pill" onclick="showSection('glossary')" title="Glossário">📚</button>
        </nav>

        <main id="spa-content">
            <section id="week-summary" class="spa-section active">
                <div class="lesson-card">
                    <div style="display: flex; flex-direction: column; gap: 15px; margin-bottom: 30px; border-bottom: 1px solid var(--border); padding-bottom: 20px;">
                        <div>
                            <h1 style="margin:0; font-size: 1.8rem;">Dashboard Semestral — 2026.2</h1>
                            <div style="color: var(--accent); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 5px;">Análise e Desenvolvimento de Sistemas • 2º Semestre</div>
                        </div>
                    </div>

                    {{DISCIPLINE_VIEW}}

                    <details class="collapsible-section" open>
                        <summary>Visão Temporal (Calendário 2026.2)</summary>
                        <div class="collapsible-content">
                            {{MONTH_SELECTOR}}
                            <div class="calendar-section">
                                {{CALENDAR_VIEWS}}
                            </div>
                        </div>
                    </details>

                    <div class="stats-bar">
                        <div class="stat-card"><span class="stat-value">{{TOTAL_WEEKS}}</span><span class="stat-label">Semanas</span></div>
                        <div class="stat-card"><span class="stat-value">{{TOTAL_LESSONS}}</span><span class="stat-label">Aulas</span></div>
                        <div class="stat-card"><span class="stat-value">{{GLOSSARY_COUNT}}</span><span class="stat-label">Termos</span></div>
                    </div>

                    <details class='collapsible-section' open>
                        <summary>Panorama do Semestre</summary>
                        <div class='collapsible-content'>
                            <div class='global-timeline'>
                                {{TIMELINE_CONTENT}}
                            </div>
                        </div>
                    </details>
                </div>
            </section>

            {{LESSONS_CONTENT}}

            <section id="glossary" class="spa-section">
                <div class="lesson-card">
                    <div class="lesson-metadata">Dicionário Técnico Transversal • 2026.2</div>
                    <h2>Glossário ({{GLOSSARY_COUNT}} termos)</h2>
                    <div class="glossary-grid">{{GLOSSARY_CONTENT}}</div>
                </div>
            </section>
        </main>
    </div>

    <script>
        const NAV_MAP = {{NAV_MAP}};
        let currentLessonId = 'dashboard';

        function showSection(id) {
            currentLessonId = id;
            document.querySelectorAll('.spa-section').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.day-btn, .info-pill').forEach(b => b.classList.remove('active'));
            
            const targetId = (id === 'dashboard') ? 'week-summary' : id;
            const target = document.getElementById(targetId);
            
            if (target) {
                target.classList.add('active');
                updateNavBar(id);
                window.scrollTo({ top: 0, behavior: 'smooth' });
                
                document.querySelectorAll("table").forEach(table => {
                    if (!table.parentElement.classList.contains("table-wrapper")) {
                        const wrapper = document.createElement("div");
                        wrapper.className = "table-wrapper";
                        table.parentNode.insertBefore(wrapper, table);
                        wrapper.appendChild(table);
                    }
                });
            }
        }

        function updateNavBar(id) {
            const contextBox = document.getElementById('nav-context');
            const prevBtn = document.getElementById('nav-prev');
            const nextBtn = document.getElementById('nav-next');
            const homeBtn = document.getElementById('nav-home');
            const glossBtn = document.getElementById('nav-glossary');

            if (id === 'dashboard') {
                contextBox.innerHTML = 'Dashboard';
                prevBtn.style.opacity = '0.2'; prevBtn.style.pointerEvents = 'none';
                nextBtn.style.opacity = '0.2'; nextBtn.style.pointerEvents = 'none';
                homeBtn.classList.add('active');
            } else if (id === 'glossary') {
                contextBox.innerHTML = 'Glossário';
                prevBtn.style.opacity = '0.2'; prevBtn.style.pointerEvents = 'none';
                nextBtn.style.opacity = '0.2'; nextBtn.style.pointerEvents = 'none';
                glossBtn.classList.add('active');
            } else {
                const nav = NAV_MAP[id];
                contextBox.innerHTML = nav ? nav.label : 'Aula';
                contextBox.classList.add('active');
                
                if (nav && nav.prev) {
                    prevBtn.style.opacity = '1'; prevBtn.style.pointerEvents = 'all';
                } else {
                    prevBtn.style.opacity = '0.2'; prevBtn.style.pointerEvents = 'none';
                }

                if (nav && nav.next) {
                    nextBtn.style.opacity = '1'; nextBtn.style.pointerEvents = 'all';
                } else {
                    nextBtn.style.opacity = '0.2'; nextBtn.style.pointerEvents = 'none';
                }
            }
        }

        function switchWeek(weekId, targetLessonId) {
            if (targetLessonId) {
                showSection(targetLessonId);
            }
        }

        function goPrev() {
            const nav = NAV_MAP[currentLessonId];
            if (nav && nav.prev) showSection(nav.prev);
        }

        function goNext() {
            const nav = NAV_MAP[currentLessonId];
            if (nav && nav.next) showSection(nav.next);
        }

        function changeMonth(monthId) {
            document.querySelectorAll('.month-pill').forEach(p => p.classList.remove('active'));
            const p = document.getElementById('pill-' + monthId);
            if (p) p.classList.add('active');
            document.querySelectorAll('.calendar-view').forEach(v => v.classList.remove('active'));
            const m = document.getElementById('month-' + monthId);
            if (m) m.classList.add('active');
        }

        document.addEventListener('click', e => {
            const link = e.target.closest('.term-link');
            if (link) { 
                e.preventDefault(); 
                showSection('glossary'); 
                const href = link.getAttribute('href');
                const termId = href.replace('#', '');
                setTimeout(() => {
                    const el = document.getElementById(termId);
                    if (el) {
                        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }, 150);
            }
        });

        window.onload = () => {
            const hash = window.location.hash.substring(1);
            showSection(hash || 'dashboard');
        };
    </script>
</body>
</html>
"""

    week_folders = sorted(list(SEMANAL_DIR.glob("W_*")))
    global_glossary, weeks_lessons_raw, all_lessons_by_date = {}, [], {}

    for folder in sorted(week_folders, reverse=False):
        w_id = folder.name.replace("_", "")
        config_path = folder / "week_config.json"
        config = {"title": f"Semana {w_id}", "text": "Consolidação das aulas da semana."}
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f: config = json.load(f)
        
        md_files = sorted(list(folder.glob("*.md")))
        
        week_lessons = []
        for p in md_files:
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    date = re.search(r'data:\s*([\d-]+)', content).group(1)
                    disc_raw = re.search(r'disciplina:\s*"(.*?)"', content).group(1)
                    prof_raw = re.search(r'professor:\s*"(.*?)"', content).group(1)
                    tit_raw = re.search(r'titulo:\s*"(.*?)"', content).group(1)
                    
                    disc_lower = disc_raw.lower()
                    if "linguagem c" in disc_lower or disc_lower == "c": short = "C"
                    elif "objeto" in disc_lower or "poo" in disc_lower: short = "POO"
                    elif "banco" in disc_lower or "dados" in disc_lower: short = "BD"
                    elif "extensão" in disc_lower: short = "Ext"
                    elif "projeto" in disc_lower: short = "PI"
                    elif "prática" in disc_lower: short = "Prat"
                    else: short = disc_raw.split()[0]
                    
                    num_match = re.search(r'(\d+)', p.stem)
                    num = num_match.group(1) if num_match else "01"
                    cls = ""
                    
                    l_id = f"{w_id}-{p.stem}"
                    
                    parts = re.split(r'##\s*Gloss[aá]rio', content, flags=re.IGNORECASE)
                    if len(parts) > 1:
                        matches = re.finditer(r'-\s*\*\*(.*?)\*\*[:\s]*(.*?)(?=\n-\s*\*\*|\Z)', parts[1], re.DOTALL)
                        for m in matches:
                            term = m.group(1).strip()
                            norm = term.lower()
                            definition = convert_to_html(m.group(2).strip())
                            if norm not in global_glossary:
                                global_glossary[norm] = {"term": term, "def": definition, "sources": []}
                            global_glossary[norm]["sources"].append({"id": l_id, "name": f"{short} {num}", "date": date})

                    body_md = parts[0].split('---', 2)[-1].strip()
                    lesson_data = {
                        "id": l_id, "date": date, "disc": disc_raw, "prof": prof_raw, 
                        "short": short, "num": num, "cls": cls, "title": tit_raw,
                        "wd": WEEKDAYS[datetime.strptime(date, "%Y-%m-%d").weekday()], 
                        "html_raw": convert_to_html(body_md)
                    }
                    week_lessons.append(lesson_data)
                    all_lessons_by_date[date] = lesson_data
                except Exception as e: print(f"  ⚠️ Ignorado {p.name}: {e}")
        
        if week_lessons:
            week_lessons.sort(key=lambda x: x['date'])
            weeks_lessons_raw.append({"id": w_id, "config": config, "lessons": week_lessons})

    total_lessons_count = sum(len(w['lessons']) for w in weeks_lessons_raw)
    glossary_list = list(global_glossary.values())
    
    day_buttons_html, lessons_html, timeline_entries = "", "", ""
    disciplines = {}

    for week in weeks_lessons_raw:
        w_id = week['id']
        first_lesson_id = week['lessons'][0]['id'] if week['lessons'] else ""
        for l in week['lessons']:
            html_linked = linkify(l['html_raw'], glossary_list)
            label = get_label(l["num"])
            day_buttons_html += f'<button id="btn-{l["id"]}" class="day-btn week-{w_id}" onclick="showSection(\'{l["id"]}\')"><strong>{l["short"]} {l["num"]}</strong><span>{l["wd"]} - {l["date"][8:]}/{l["date"][5:7]}</span></button>'
            lessons_html += f'<section id="{l["id"]}" class="spa-section"><div class="lesson-card"><div class="lesson-metadata">{l["disc"]} | {l["prof"]} | {l["date"]} | {label}</div><h1 style="font-size: 1.6rem; margin: 15px 0 25px 0; color: #fff;">{l["title"]}</h1>{html_linked}</div></section>'
            
            d_name = l["disc"]
            if d_name not in disciplines: disciplines[d_name] = {"prof": l["prof"], "short": l["short"], "lessons": []}
            disciplines[d_name]["lessons"].append(l)

        timeline_entries += f"<div class='timeline-entry' onclick=\"switchWeek('{w_id}', '{first_lesson_id}')\"><div class='timeline-dot'></div><div class='timeline-info'><span class='timeline-week'>Semana {w_id[1:]}</span><h4 class='timeline-title'>{week['config']['title']}</h4><p class='timeline-text'>{week['config']['text']}</p></div></div>"

    discipline_view_html = "<details class='collapsible-section' open><summary>Trilhas de Aprendizado (2026.2)</summary><div class='collapsible-content'><div class='discipline-tracks'>"
    for d_name in sorted(disciplines.keys()):
        prof_label = f"<span style='color:var(--accent);'>{disciplines[d_name]['prof']}</span>"
        discipline_view_html += f"<div class='discipline-row'><span class='discipline-label'>{d_name} | <span style='color:var(--text-dim);opacity:0.7;'>{prof_label}</span></span><div class='lesson-pills'>"
        for l in sorted(disciplines[d_name]["lessons"], key=lambda x: x["date"]):
            discipline_view_html += f"<button class='lesson-pill {l['cls']}' onclick=\"showSection('{l['id']}')\">{l['short']} {get_label(l['num'])}</button>"
        discipline_view_html += "</div></div>"
    discipline_view_html += "</div></div></details>"

    nav_map = {}
    # Navegação contextual por DISCIPLINA
    for d_name, d_data in disciplines.items():
        disc_lessons = sorted(d_data["lessons"], key=lambda x: x["date"])
        for idx, l in enumerate(disc_lessons):
            prev_id = disc_lessons[idx-1]["id"] if idx > 0 else None
            next_id = disc_lessons[idx+1]["id"] if idx < len(disc_lessons)-1 else None
            nav_map[l["id"]] = {
                "prev": prev_id,
                "next": next_id,
                "label": f"{l['short']}<br><span class='nav-lesson-num'>{get_label(l['num'])}</span>"
            }

    # Glossário Final
    glossary_html = ""
    for k in sorted(global_glossary.keys(), key=lambda x: normalize_sort(global_glossary[x]["term"])):
        g = global_glossary[k]
        wiki_match = re.search(r'href=["\']([^"\']*wikipedia\.org[^"\']*)["\']', g["def"], re.IGNORECASE)
        wiki_url = wiki_match.group(1) if wiki_match else ""
        g["def"] = sanitize_glossary_def(g["def"])
        g["def"] = re.sub(r'<[^>]*>', '', g["def"])
        if g["def"] and not g["def"].endswith('.'): g["def"] += "."
        g['sources'].sort(key=lambda x: x['date'])
        ps = g['sources'][0] if g['sources'] else None
        source_btns = f"<button class='action-btn' onclick=\"showSection('{ps['id']}')\">{ps['name']}</button>" if ps else ""
        wiki_btn = f"<a href='{wiki_url}' target='_blank' class='action-btn wiki-btn'>Wikipedia</a>" if wiki_url else ""
        glossary_html += f"<div class='glossary-item' id='term-{slugify(g['term'])}'><span class='glossary-term'>{g['term']}</span><div class='glossary-def'>{g['def']}</div><div class='glossary-footer'><div style='display:flex;gap:8px'>{source_btns}</div>{wiki_btn}</div></div>"

    # --- CALENDÁRIO 2026.2 ---
    month_selector_html = '<div class="month-selector">'
    calendar_views_html = ""
    WEEK_MAP = {"Seg": "PI", "Ter": "POO", "Qua": "C", "Qui": "C", "Sex": "BD", "Sáb": "Ext"}
    
    current_month = 8
    for m in [8, 9, 10, 11, 12]:
        is_active = (m == current_month)
        month_selector_html += f'<div id="pill-{m:02d}" class="month-pill {"active" if is_active else ""}" onclick="changeMonth(\'{m:02d}\')">{MONTH_NAMES[m]}</div>'
        calendar_views_html += f'<div id="month-{m:02d}" class="calendar-view {"active" if is_active else ""}">\n<div class="calendar-header"><div class="calendar-title">{MONTH_NAMES[m]} 2026</div><div style="font-size: 0.7rem; color: #555;">Semestre 2026.2</div></div>\n<div class="calendar-grid" style="grid-template-columns: repeat(6, 1fr);">\n'
        for d_name in ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]:
            calendar_views_html += f'<div class="weekday-label">{d_name}<br><span style="color:var(--accent);font-size:0.55rem;font-weight:800;opacity:0.8;">{WEEK_MAP.get(d_name, "")}</span></div>'
        
        cal = calendar.Calendar(firstweekday=0)
        for week in cal.monthdays2calendar(2026, m):
            if not any(d != 0 and wd != 6 for d, wd in week): continue
            for d, wd in week:
                if wd == 6: continue
                if d == 0: calendar_views_html += '<div class="day-cell empty"></div>'
                else:
                    date_str = f"2026-{m:02d}-{d:02d}"
                    l = all_lessons_by_date.get(date_str)
                    if l:
                        status_class = l['cls'] if l['cls'] else "active"
                        calendar_views_html += f'<div class="day-cell has-lesson {status_class}" onclick="showSection(\'{l["id"]}\')"><span class="day-number">{d}</span><span class="lesson-tag">{l["short"]}</span></div>'
                    else:
                        calendar_views_html += f'<div class="day-cell"><span class="day-number" style="opacity:0.3;">{d}</span></div>'
        calendar_views_html += "</div>\n</div>"
    month_selector_html += "</div>"

    master_css = CSS_SNIPPET.read_text(encoding='utf-8') if CSS_SNIPPET.exists() else ""
    
    final = tpl.replace("{{MASTER_CSS}}", master_css)
    final = final.replace("{{TOTAL_WEEKS}}", str(len(weeks_lessons_raw)))
    final = final.replace("{{TOTAL_LESSONS}}", str(total_lessons_count))
    final = final.replace("{{GLOSSARY_COUNT}}", str(len(glossary_list)))
    final = final.replace("{{DISCIPLINE_VIEW}}", discipline_view_html)
    final = final.replace("{{MONTH_SELECTOR}}", month_selector_html)
    final = final.replace("{{CALENDAR_VIEWS}}", calendar_views_html)
    final = final.replace("{{TIMELINE_CONTENT}}", timeline_entries)
    final = final.replace("{{LESSONS_CONTENT}}", lessons_html)
    final = final.replace("{{GLOSSARY_CONTENT}}", glossary_html)
    final = final.replace("{{NAV_MAP}}", json.dumps(nav_map))

    version_label = '<div style="text-align:center; padding: 20px; color: var(--text-dim); font-size: 0.6rem; opacity: 0.5;">v5.0.0 • SSOT ADS 2026.2 Dashboard</div>'
    final = final.replace('</body>', version_label + '</body>')

    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(final)

    # Também gerar como index.html na raiz do portal para abrir direto
    with open(OUTPUT_HTML.parent / "index.html", 'w', encoding='utf-8') as f:
        f.write(final)

    print(f"🎉 Recap_Master_S2.html gerado com sucesso em: {OUTPUT_HTML}")
    return True

if __name__ == "__main__":
    build()
