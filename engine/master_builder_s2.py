import os
import re
import json
import calendar
import unicodedata
import subprocess
from pathlib import Path

REPO_ROOT = Path("/home/jeronimo/G-Sync/ads-senac-recaps")
ENGINE_DIR = REPO_ROOT / "engine"
PORTAL_DIR = REPO_ROOT / "portal"
SEMANAL_DIR = REPO_ROOT / "s2_2026_2/02_semanal"

PORTAL_DIR.mkdir(parents=True, exist_ok=True)

DISC_STYLES = {
    "Projeto Integrador": {"short": "PI", "color": "#a855f7", "bg": "rgba(168, 85, 247, 0.12)", "border": "rgba(168, 85, 247, 0.4)", "tag": "tag-pi", "order": 1},
    "Programação Orientada a Objetos": {"short": "POO", "color": "#f59e0b", "bg": "rgba(245, 158, 11, 0.12)", "border": "rgba(245, 158, 11, 0.4)", "tag": "tag-poo", "order": 2},
    "Linguagem C": {"short": "C", "color": "#06b6d4", "bg": "rgba(6, 182, 212, 0.12)", "border": "rgba(6, 182, 212, 0.4)", "tag": "tag-c", "order": 3},
    "Banco de Dados Relacional": {"short": "BD", "color": "#10b981", "bg": "rgba(16, 185, 129, 0.12)", "border": "rgba(16, 185, 129, 0.4)", "tag": "tag-bd", "order": 4},
    "Projeto de Extensão": {"short": "Ext", "color": "#ec4899", "bg": "rgba(236, 72, 153, 0.12)", "border": "rgba(236, 72, 153, 0.4)", "tag": "tag-ext", "order": 5},
    "Outros": {"short": "Outros", "color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.12)", "border": "rgba(148, 163, 184, 0.4)", "tag": "tag-outros", "order": 99},
}

def get_disc_meta(disc_name):
    for k, v in DISC_STYLES.items():
        if k.lower() in disc_name.lower() or disc_name.lower() in k.lower():
            return v
    return DISC_STYLES["Outros"]

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def normalize_sort(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower()

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

def pandoc_markdown_to_html(md_text):
    callout_pattern = r'>\s*\[!(tip|note|important|warning|caution|abstract|info|question|quote|bug)\]\s*(.*?)(?=\n\n|\n[^\>]|$)'
    def replace_callout(match):
        c_type = match.group(1).lower()
        c_content = match.group(2).strip()
        return f'<div class="callout callout-{c_type}"><div class="callout-title">{c_type.upper()}</div><div class="callout-content">{c_content}</div></div>'
    
    md_processed = re.sub(callout_pattern, replace_callout, md_text, flags=re.DOTALL)
    
    try:
        res = subprocess.run(
            ["pandoc", "-f", "markdown+hard_line_breaks+backtick_code_blocks+fenced_code_attributes", "-t", "html", "--syntax-highlighting=tango"],
            input=md_processed,
            text=True,
            capture_output=True,
            check=True
        )
        return res.stdout
    except Exception as e:
        paragraphs = md_processed.split("\n\n")
        return "".join(f"<p>{p.replace('\n', '<br>')}</p>" for p in paragraphs)

def linkify(html_content, glossary_terms):
    soup_tokens = re.split(r'(<[^>]+>)', html_content)
    sorted_terms = sorted(glossary_terms, key=lambda x: len(x['term']), reverse=True)
    
    in_code_block = False
    in_heading = False
    
    for i, token in enumerate(soup_tokens):
        if not token: continue
        
        if token.startswith('<'):
            tag_name = token.strip('<>/').split()[0].lower()
            if tag_name in ['pre', 'code']:
                in_code_block = not token.startswith('</')
            elif tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                in_heading = not token.startswith('</')
            continue
            
        if in_code_block or in_heading:
            continue
            
        text = token
        for item in sorted_terms:
            t = item['term']
            slug = item['slug']
            pattern = re.compile(rf'(?<![\w\-_/])({re.escape(t)})(?![\w\-_/])', re.IGNORECASE)
            text = pattern.sub(rf'<a href="#term-{slug}" class="term-link">\1</a>', text)
        soup_tokens[i] = text
        
    return "".join(soup_tokens)

def get_label(num_str):
    if num_str.isdigit():
        return f"Aula {int(num_str):02d}"
    return num_str

def clean_glossary_definition(raw_def):
    wiki_url = ""
    # 1. HTML link: <a href="(url)">...</a>
    m_html = re.search(r"<a\s+[^>]*href=['\"](https?://[^'\"]*wikipedia\.org[^'\"]*)['\"][^>]*>.*?</a>", raw_def, re.IGNORECASE)
    if m_html:
        wiki_url = m_html.group(1).strip()
        raw_def = raw_def[:m_html.start()] + raw_def[m_html.end():]
        
    # 2. Markdown link [Wikipedia](url) ou [Wikipédia](url)
    if not wiki_url:
        m_md = re.search(r"\[(?:Wikipedia|Wikip[eé]dia|Wiki)\]\((https?://[^\s]+)\)", raw_def, re.IGNORECASE)
        if m_md:
            wiki_url = m_md.group(1).strip()
            raw_def = raw_def[:m_md.start()] + raw_def[m_md.end():]

    # 3. Qualquer link markdown residual com wikipedia
    if not wiki_url:
        m_md_any = re.search(r"\[[^\]]*\]\((https?://[^\s]+?wikipedia\.org[^\s]*)\)", raw_def, re.IGNORECASE)
        if m_md_any:
            wiki_url = m_md_any.group(1).strip()
            raw_def = raw_def[:m_md_any.start()] + raw_def[m_md_any.end():]

    # 4. URL solta
    if not wiki_url:
        m_url = re.search(r"https?://[^\s]+?wikipedia\.org[^\s]*", raw_def, re.IGNORECASE)
        if m_url:
            wiki_url = m_url.group(0).rstrip(".)")
            raw_def = raw_def[:m_url.start()] + raw_def[m_url.end():]

    # Limpeza refinada do texto da definição
    raw_def = re.sub(r"<[^>]+>", " ", raw_def)
    raw_def = re.sub(r"\[\s*\]|\(\s*\)", "", raw_def)
    raw_def = re.sub(r"\s*\)\s*\.", ".", raw_def)
    raw_def = re.sub(r"\s*\]\s*\.", ".", raw_def)
    raw_def = re.sub(r"\s*;\s*\.", ".", raw_def)
    raw_def = re.sub(r"\s+", " ", raw_def).strip()
    raw_def = raw_def.rstrip(" .);,")
    if raw_def:
        raw_def += "."
        
    return raw_def, wiki_url

def build():
    print(f"🚀 Invocando Motor Master S2 (2026.2) com Bordas Nítidas nos Cards do Glossário...")
    
    tpl = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recap | ADS 2026.2</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
{{MASTER_CSS}}
    </style>
</head>
<body>
    <div class="main-container">
        <!-- Top App Bar (1 Linha Unificada) -->
        <header class="app-header">
            <div class="brand">
                <span class="brand-icon">🎓</span>
                <span class="brand-title">ADS SENAC</span>
                <span class="brand-badge">2026.2</span>
            </div>
            <div class="header-actions">
                <button class="search-trigger-btn" onclick="openSearchModal()" title="Busca Global (Ctrl+K)">
                    <span style="font-size:0.9rem; color:var(--accent);">🔍</span>
                    <span class="search-placeholder">Buscar aula, código, termo...</span>
                    <span class="kbd-shortcut">Ctrl+K</span>
                </button>
                <div class="semester-pills">
                    <a href="Recap_Master_S1.html" class="sem-link">2026.1</a>
                    <a href="Recap_Master_S2.html" class="sem-link active">2026.2</a>
                </div>
            </div>
        </header>

        <!-- Barra de Navegação Flutuante -->
        <nav class="weekly-timeline">
            <button id="nav-home" class="info-pill active" onclick="showSection('dashboard')" title="Início">🏠 Início</button>
            <button id="nav-prev" class="day-btn" onclick="goPrev()" title="Aula Anterior na Matéria">‹</button>
            <div id="nav-context" class="info-pill context-pill">Dashboard</div>
            <button id="nav-next" class="day-btn" onclick="goNext()" title="Próxima Aula na Matéria">›</button>
            <button id="nav-glossary" class="info-pill" onclick="showSection('glossary')" title="Glossário">📚 Glossário</button>
        </nav>

        <main id="spa-content">
            <section id="week-summary" class="spa-section active">
                <div class="lesson-card hero-card">
                    <!-- Header Horizontal (1 Linha, 2 Colunas / Título + Métricas) -->
                    <div class="hero-header-row">
                        <div class="hero-brand-col">
                            <h1 class="hero-title">Dashboard Semestral — 2026.2</h1>
                            <div class="hero-subtitle">Análise e Desenvolvimento de Sistemas • 2º Semestre</div>
                        </div>
                        <div class="stats-cards-col">
                            <div class="stat-card"><span class="stat-value">2</span><span class="stat-label">Semanas</span></div>
                            <div class="stat-card"><span class="stat-value">10</span><span class="stat-label">Aulas</span></div>
                            <div class="stat-card"><span class="stat-value">{{TOTAL_TERMOS}}</span><span class="stat-label">Termos</span></div>
                        </div>
                    </div>
                    
                    {{DISCIPLINE_TRACKS}}

                    <details class="collapsible-section" open>
                        <summary>Visão Temporal do Semestre</summary>
                        <div class="collapsible-content">
                            <!-- Filtro Rápido de Matéria no Calendário -->
                            <div class="cal-filter-bar">
                                <span class="filter-label">Filtrar matéria:</span>
                                <button class="cal-filter-btn active" onclick="filterCalendar('all', this)">Todas</button>
                                <button class="cal-filter-btn btn-poo" onclick="filterCalendar('POO', this)">POO</button>
                                <button class="cal-filter-btn btn-c" onclick="filterCalendar('C', this)">C</button>
                                <button class="cal-filter-btn btn-pi" onclick="filterCalendar('PI', this)">PI</button>
                                <button class="cal-filter-btn btn-bd" onclick="filterCalendar('BD', this)">BD</button>
                                <button class="cal-filter-btn btn-ext" onclick="filterCalendar('Ext', this)">Extensão</button>
                            </div>
                            {{MONTH_SELECTOR}}
                            <div class="calendar-wrapper">
                                {{CALENDAR_VIEWS}}
                            </div>
                        </div>
                    </details>

                    <details class="collapsible-section" open>
                        <summary>Linha do Tempo Semestral</summary>
                        <div class="collapsible-content">
                            <div class="timeline-container">
                                {{TIMELINE_ENTRIES}}
                            </div>
                        </div>
                    </details>
                </div>
            </section>

            {{LESSONS_HTML}}

            <section id="glossary" class="spa-section">
                <div class="lesson-card">
                    <div style="border-bottom: 1px solid var(--border); padding-bottom: 15px; margin-bottom: 25px;">
                        <h1 style="font-size: 1.8rem; margin:0; color:#fff;">Glossário Técnico Cruzado (2026.2)</h1>
                        <div style="color: var(--accent); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 5px;">Índice Alfabético com Backlinks Diretos e Fontes Wikipedia</div>
                    </div>
                    <div class="glossary-grid">
                        {{GLOSSARY_HTML}}
                    </div>
                </div>
            </section>
        </main>
    </div>

    <!-- Modal de Busca Global (Spotlight) -->
    <div id="search-modal" class="search-modal-backdrop" onclick="handleBackdropClick(event)">
        <div class="search-modal-box">
            <div class="search-input-wrapper">
                <span class="search-modal-icon">🔍</span>
                <input type="text" id="search-input" placeholder="Digite para pesquisar em todas as aulas, códigos ou glossário..." oninput="handleSearch(this.value)" autocomplete="off">
                <button class="search-close-btn" onclick="closeSearchModal()">Esc</button>
            </div>
            <div id="search-results" class="search-results-list">
                <div class="search-empty-state">Digite algo para buscar (ex: <code>malloc</code>, <code>Fred</code>, <code>TAP</code>, <code>Lâmpada</code>, <code>scanf</code>)...</div>
            </div>
        </div>
    </div>

    <script>
        const NAV_MAP = {{NAV_MAP_JSON}};
        const SEARCH_INDEX = {{SEARCH_INDEX_JSON}};
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
            
            document.querySelectorAll('.calendar-view').forEach(v => {
                v.classList.remove('active');
                v.style.display = 'none';
            });
            const m = document.getElementById('month-' + monthId);
            if (m) {
                m.classList.add('active');
                m.style.display = 'block';
            }
        }

        function filterCalendar(discShort, btnEl) {
            document.querySelectorAll('.cal-filter-btn').forEach(b => b.classList.remove('active'));
            btnEl.classList.add('active');
            
            document.querySelectorAll('.calendar-day').forEach(cell => {
                if (discShort === 'all') {
                    cell.style.opacity = '1';
                    cell.style.filter = 'none';
                } else {
                    const tag = cell.getAttribute('data-disc');
                    if (tag === discShort) {
                        cell.style.opacity = '1';
                        cell.style.filter = 'none';
                        cell.style.boxShadow = '0 0 10px rgba(56, 189, 248, 0.4)';
                    } else if (cell.classList.contains('active-lesson')) {
                        cell.style.opacity = '0.25';
                        cell.style.filter = 'grayscale(80%)';
                        cell.style.boxShadow = 'none';
                    }
                }
            });
        }

        // Modal de Busca Global
        function openSearchModal() {
            const m = document.getElementById('search-modal');
            m.classList.add('open');
            const inp = document.getElementById('search-input');
            inp.focus();
            inp.select();
        }

        function closeSearchModal() {
            const m = document.getElementById('search-modal');
            m.classList.remove('open');
        }

        function handleBackdropClick(e) {
            if (e.target.id === 'search-modal') closeSearchModal();
        }

        function handleSearch(query) {
            const q = query.trim().toLowerCase();
            const resContainer = document.getElementById('search-results');
            if (!q) {
                resContainer.innerHTML = '<div class="search-empty-state">Digite algo para buscar...</div>';
                return;
            }

            const results = [];
            SEARCH_INDEX.forEach(item => {
                let score = 0;
                if (item.title.toLowerCase().includes(q)) score += 10;
                if (item.disc.toLowerCase().includes(q)) score += 5;
                if (item.text.toLowerCase().includes(q)) score += 2;
                
                if (score > 0) {
                    const lowerText = item.text.toLowerCase();
                    const idx = lowerText.indexOf(q);
                    let snippet = "";
                    if (idx !== -1) {
                        const start = Math.max(0, idx - 40);
                        const end = Math.min(item.text.length, idx + 100);
                        snippet = (start > 0 ? "..." : "") + item.text.substring(start, end) + (end < item.text.length ? "..." : "");
                        const safeQ = q.replace(/[-\/\\\\^$*+?.()|[\\]{}]/g, '\\\\$&');
                        const regex = new RegExp("(" + safeQ + ")", "gi");
                        snippet = snippet.replace(regex, "<mark class='search-highlight'>$1</mark>");
                    } else {
                        snippet = item.text.substring(0, 100) + "...";
                    }
                    results.push({ item, score, snippet });
                }
            });

            results.sort((a, b) => b.score - a.score);

            if (results.length === 0) {
                resContainer.innerHTML = '<div class="search-empty-state">Nenhum resultado encontrado para "<b>' + query + '</b>".</div>';
                return;
            }

            let html = "";
            results.slice(0, 8).forEach(r => {
                const it = r.item;
                const badgeStyle = "background:" + it.bg + "; color:" + it.color + "; border:1px solid " + it.border + ";";
                html += `
                <div class="search-result-item" onclick="showSection('${it.id}'); closeSearchModal();">
                    <div class="search-result-header">
                        <span class="search-result-badge" style="${badgeStyle}">${it.short}</span>
                        <span class="search-result-title">${it.title}</span>
                        <span class="search-result-date">${it.date || ''}</span>
                    </div>
                    <div class="search-result-snippet">${r.snippet}</div>
                </div>`;
            });
            resContainer.innerHTML = html;
        }

        // Atalhos de Teclado
        document.addEventListener('keydown', e => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                openSearchModal();
            }
            if (e.key === 'Escape') {
                closeSearchModal();
            }
            if (!document.getElementById('search-modal').classList.contains('open')) {
                if (e.key === 'ArrowLeft') goPrev();
                if (e.key === 'ArrowRight') goNext();
            }
        });

        // Links de Glossário com Efeito Flash
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
                        el.classList.add('term-flash');
                        setTimeout(() => el.classList.remove('term-flash'), 1500);
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

    # Ler CSS Master
    css_path = ENGINE_DIR / "styles.css"
    master_css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    
    # CSS Customizado com Top App Bar, Trilhas e Bordas Nítidas nos Cards do Glossário
    extra_css = """
    /* --- TOP APP BAR UNIFICADA (1 LINHA HORIZONTAL) --- */
    .app-header {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
        background: #141417 !important;
        border: 1px solid #27272a !important;
        border-radius: 14px !important;
        padding: 10px 18px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
        flex-wrap: wrap !important;
        gap: 15px !important;
    }
    .brand {
        display: inline-flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 8px !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        color: #fff !important;
        text-decoration: none !important;
    }
    .brand-icon { font-size: 1.2rem !important; line-height: 1 !important; }
    .brand-title { font-weight: 800 !important; letter-spacing: 0.5px !important; color: #f4f4f5 !important; }
    .brand-badge {
        background: rgba(56, 189, 248, 0.12) !important;
        color: var(--accent) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        padding: 2px 7px !important;
        border-radius: 6px !important;
        font-size: 0.72rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
    }
    .header-actions {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 12px !important;
    }
    .search-trigger-btn {
        background: #18181b !important;
        border: 1px solid #27272a !important;
        color: #a1a1aa !important;
        padding: 6px 14px !important;
        border-radius: 8px !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 10px !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
    }
    .search-trigger-btn:hover {
        border-color: var(--accent) !important;
        color: #fff !important;
        background: #202025 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.15) !important;
    }
    .kbd-shortcut {
        background: #222227 !important;
        border: 1px solid #33333d !important;
        color: var(--accent) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-size: 0.65rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
    }
    .semester-pills {
        display: inline-flex !important;
        flex-direction: row !important;
        background: #0e0e11 !important;
        border: 1px solid #27272a !important;
        padding: 3px !important;
        border-radius: 8px !important;
        gap: 4px !important;
    }
    .sem-link {
        text-decoration: none !important;
        padding: 5px 12px !important;
        border-radius: 6px !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        color: #71717a !important;
        transition: all 0.2s !important;
        line-height: 1.2 !important;
        border: 1px solid transparent !important;
    }
    .sem-link:hover { color: #f4f4f5 !important; }
    .sem-link.active {
        background: var(--accent) !important;
        color: #000 !important;
        font-weight: 800 !important;
        box-shadow: 0 2px 8px rgba(56, 189, 248, 0.3) !important;
    }

    /* --- HEADER HERO HORIZONTAL --- */
    .hero-header-row {
        display: flex; justify-content: space-between; align-items: center;
        gap: 25px; padding-bottom: 25px; border-bottom: 1px solid var(--border); margin-bottom: 25px;
    }
    .hero-brand-col { flex: 1; }
    .hero-title { margin: 0; font-size: 1.8rem; font-weight: 800; color: #fff; letter-spacing: -0.5px; }
    .hero-subtitle { color: var(--accent); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 6px; font-weight: 600; }
    
    .stats-cards-col { display: flex; gap: 12px; }
    .stat-card {
        background: #141417; border: 1px solid #27272a; padding: 12px 18px;
        border-radius: 10px; min-width: 95px; text-align: center;
    }
    .stat-value { font-size: 1.4rem; font-weight: 800; color: var(--accent); display: block; line-height: 1; }
    .stat-label { font-size: 0.65rem; color: #a1a1aa; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-top: 5px; display: block; }

    /* --- SEÇÕES COLAPSÁVEIS MODERNAS --- */
    .collapsible-section {
        margin-top: 20px; border: 1px solid var(--border); border-radius: 12px;
        background: rgba(255,255,255,0.01); overflow: hidden; margin-bottom: 20px;
    }
    .collapsible-section summary {
        padding: 14px 18px; font-size: 0.95rem; font-weight: 700; color: #f4f4f5;
        cursor: pointer; background: #141417; display: flex; align-items: center;
        justify-content: space-between; user-select: none; transition: background 0.2s;
    }
    .collapsible-section summary:hover { background: #1c1c20; }
    .collapsible-section[open] summary { border-bottom: 1px solid var(--border); background: #18181c; }
    .collapsible-section summary::-webkit-details-marker { display: none; }
    .collapsible-section summary::after { content: '▾'; font-size: 1.1rem; color: var(--accent); transition: transform 0.2s; }
    .collapsible-section[open] summary::after { transform: rotate(180deg); }
    .collapsible-content { padding: 18px; }

    /* --- CALENDÁRIO MODERNO (APENAS MÊS ATIVO) --- */
    .calendar-view { display: none; }
    .calendar-view.active { display: block !important; }

    .cal-filter-bar { display: flex; align-items: center; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }
    .filter-label { font-size: 0.75rem; color: #888; font-weight: 600; text-transform: uppercase; }
    .cal-filter-btn {
        background: #18181b; border: 1px solid #333; color: #ccc;
        padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
    }
    .cal-filter-btn:hover { border-color: #555; color: #fff; }
    .cal-filter-btn.active { background: var(--accent); color: #000; border-color: var(--accent); }
    .cal-filter-btn.btn-poo.active { background: #f59e0b; color: #000; border-color: #f59e0b; }
    .cal-filter-btn.btn-c.active { background: #06b6d4; color: #000; border-color: #06b6d4; }
    .cal-filter-btn.btn-pi.active { background: #a855f7; color: #fff; border-color: #a855f7; }
    .cal-filter-btn.btn-bd.active { background: #10b981; color: #000; border-color: #10b981; }
    .cal-filter-btn.btn-ext.active { background: #ec4899; color: #fff; border-color: #ec4899; }

    .month-selector { display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
    .month-pill {
        background: #141417; border: 1px solid #27272a; color: #a1a1aa;
        padding: 6px 14px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
    }
    .month-pill:hover { color: #fff; border-color: #3f3f46; }
    .month-pill.active { background: var(--accent); color: #000; border-color: var(--accent); font-weight: 800; }

    .calendar-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; }
    .calendar-header-day {
        text-align: center; font-size: 0.7rem; font-weight: 800; color: #71717a;
        text-transform: uppercase; letter-spacing: 1px; padding: 6px 0; border-bottom: 1px solid #27272a;
    }
    .calendar-day {
        background: #121215; border: 1px solid #27272a; border-radius: 8px;
        min-height: 68px; padding: 6px 8px; display: flex; flex-direction: column;
        justify-content: space-between; transition: all 0.2s;
    }
    .calendar-day.other-month { opacity: 0.2; background: #0b0b0d; border-color: #1a1a1d; }
    .calendar-day.active-lesson { background: #16161d; border-color: rgba(56, 189, 248, 0.3); cursor: pointer; }
    .calendar-day.active-lesson:hover {
        transform: translateY(-2px); border-color: var(--accent); box-shadow: 0 4px 15px rgba(56, 189, 248, 0.15);
    }
    .day-number { font-size: 0.8rem; font-weight: 700; color: #a1a1aa; }
    .calendar-day.active-lesson .day-number { color: #fff; }
    .cal-tag {
        display: block; padding: 2px 5px; border-radius: 4px; font-size: 0.65rem;
        font-weight: 800; text-align: center; letter-spacing: 0.5px; margin-top: 3px;
    }

    /* --- TRILHAS DE APRENDIZADO COM ESPAÇAMENTO RESPIRADO --- */
    .discipline-tracks { display: flex; flex-direction: column; gap: 12px; }
    .discipline-row {
        display: flex; align-items: center; gap: 16px; padding: 12px 18px;
        border-radius: 12px; border: 1px solid var(--border);
        background: rgba(255,255,255,0.015); flex-wrap: wrap;
    }
    .disc-badge {
        padding: 6px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 800;
        text-transform: uppercase; letter-spacing: 0.8px; min-width: 190px; text-align: left;
    }
    .lesson-pills { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
    .lesson-pill {
        padding: 6px 14px; border-radius: 8px; font-size: 0.75rem; font-weight: 700;
        cursor: pointer; transition: all 0.2s; border: 1px solid transparent;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3); margin: 2px 0;
    }
    .lesson-pill:hover { transform: translateY(-2px); filter: brightness(1.25); box-shadow: 0 4px 12px rgba(0,0,0,0.5); }

    /* --- LINHA DO TEMPO SEMESTRAL VIBRANTE & ELEGANTE --- */
    .timeline-container {
        display: flex; flex-direction: column; gap: 18px;
        position: relative; padding-left: 25px; border-left: 2px solid #27272a; margin-left: 12px;
    }
    .timeline-card {
        background: #141417; border: 1px solid #27272a; border-radius: 12px;
        padding: 20px 24px; cursor: pointer; transition: all 0.25s ease; position: relative;
    }
    .timeline-card:hover {
        background: #17171d; border-color: rgba(56, 189, 248, 0.4);
        transform: translateX(4px); box-shadow: 0 8px 25px rgba(0,0,0,0.5);
    }
    .timeline-dot {
        position: absolute; left: -34px; top: 26px; width: 14px; height: 14px;
        border-radius: 50%; background: var(--accent); box-shadow: 0 0 12px rgba(56, 189, 248, 0.8);
        border: 2px solid #121215;
    }
    .timeline-badge {
        display: inline-block; background: rgba(56, 189, 248, 0.12); color: var(--accent);
        border: 1px solid rgba(56, 189, 248, 0.3); padding: 3px 10px; border-radius: 6px;
        font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;
    }
    .timeline-title { font-size: 1.15rem; font-weight: 700; color: #fff; margin: 0 0 8px 0; }
    .timeline-text { font-size: 0.88rem; color: #a1a1aa; line-height: 1.55; margin-bottom: 15px; }
    .timeline-mini-pills {
        display: flex; gap: 8px; flex-wrap: wrap; border-top: 1px solid #27272a; padding-top: 14px;
    }
    .timeline-mini-pill {
        padding: 4px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;
        cursor: pointer; transition: all 0.15s;
    }
    .timeline-mini-pill:hover { transform: translateY(-1px); filter: brightness(1.25); }

    /* Termos do Glossário no Texto */
    .term-link {
        color: #fbbf24 !important;
        text-decoration: none !important;
        border-bottom: 1.5px dotted #f59e0b !important;
        font-weight: 600 !important;
        padding: 0 3px;
        border-radius: 3px;
        transition: all 0.15s ease;
    }
    .term-link:hover {
        background: rgba(245, 158, 11, 0.18) !important;
        color: #fef08a !important;
        border-bottom-style: solid !important;
    }

    /* --- GLOSSÁRIO COM BORDA NÍTIDA & DELIMITADORA --- */
    .glossary-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)) !important;
        gap: 16px !important;
        margin-top: 20px !important;
    }
    .glossary-item {
        background: #141417 !important;
        border: 1px solid #2d2d34 !important;
        border-radius: 12px !important;
        padding: 20px 22px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    .glossary-item:hover {
        border-color: var(--accent) !important;
        background: #18181d !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.5) !important;
    }
    .glossary-term {
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        color: #fff !important;
        margin-bottom: 8px !important;
        display: block !important;
        letter-spacing: -0.3px !important;
    }
    .glossary-def {
        font-size: 0.88rem !important;
        color: #c4c4cc !important;
        line-height: 1.55 !important;
        margin-bottom: 16px !important;
        flex-grow: 1 !important;
    }
    .glossary-footer {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        border-top: 1px solid #27272a !important;
        padding-top: 12px !important;
        gap: 8px !important;
        flex-wrap: wrap !important;
    }
    .action-btn {
        background: #202025 !important;
        color: #a1a1aa !important;
        border: 1px solid #33333d !important;
        padding: 4px 10px !important;
        border-radius: 6px !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.15s !important;
    }
    .action-btn:hover {
        background: var(--accent) !important;
        color: #000 !important;
    }
    .wiki-btn {
        background: rgba(56, 189, 248, 0.1) !important; color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important; font-weight: 700 !important;
        text-decoration: none !important; display: inline-flex !important; align-items: center !important;
    }
    .wiki-btn:hover { background: #38bdf8 !important; color: #000 !important; }

    /* --- ILUMINAÇÃO DE SINTAXE VIBRANTE (DRACULA / ONE DARK) --- */
    pre, div.sourceCode {
        background: #0d1117 !important;
        border: 1px solid #30363d !important;
        border-left: 4px solid var(--accent) !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
        overflow-x: auto !important;
        margin: 22px 0 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.88rem !important;
        line-height: 1.6 !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.5) !important;
    }
    pre code, code.sourceCode, .sourceCode span {
        font-family: 'JetBrains Mono', monospace !important;
    }
    span.kw, code span.kw { color: #ff7b72 !important; font-weight: 700 !important; }
    span.dt, code span.dt { color: #79c0ff !important; font-weight: 600 !important; }
    span.st, code span.st { color: #a5d6ff !important; }
    span.co, code span.co { color: #8b949e !important; font-style: italic !important; }
    span.fu, code span.fu { color: #d2a8ff !important; font-weight: 600 !important; }
    span.dv, span.fl, span.bn, code span.dv, code span.fl { color: #ffa657 !important; font-weight: 600 !important; }
    span.op, code span.op { color: #79c0ff !important; }
    span.pp, code span.pp { color: #ff7b72 !important; font-weight: 600 !important; }
    span.cf, code span.cf { color: #ff7b72 !important; font-weight: 700 !important; }
    span.va, code span.va { color: #e6edf3 !important; }

    /* Modal de Busca */
    .search-modal-backdrop {
        position: fixed; inset: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(5px);
        z-index: 10000; display: none; align-items: flex-start; justify-content: center; padding-top: 10vh;
    }
    .search-modal-backdrop.open { display: flex; }
    .search-modal-box {
        background: #18181b; border: 1px solid #3f3f46; border-radius: 14px;
        width: 90%; max-width: 680px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); overflow: hidden;
    }
    .search-input-wrapper {
        display: flex; align-items: center; gap: 12px; padding: 16px 20px;
        border-bottom: 1px solid #27272a; background: #121215;
    }
    .search-modal-icon { font-size: 1.2rem; color: var(--accent); }
    #search-input {
        background: transparent; border: none; outline: none; color: #fff;
        font-size: 1rem; width: 100%; font-family: 'Inter', sans-serif;
    }
    .search-close-btn {
        background: #27272a; border: 1px solid #3f3f46; color: #888;
        padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; cursor: pointer;
    }
    .search-results-list { max-height: 420px; overflow-y: auto; padding: 10px; }
    .search-empty-state { color: #71717a; text-align: center; padding: 30px; font-size: 0.9rem; }
    .search-result-item {
        padding: 12px 16px; border-radius: 8px; margin-bottom: 6px;
        background: rgba(255,255,255,0.02); border: 1px solid transparent; cursor: pointer; transition: all 0.15s;
    }
    .search-result-item:hover { background: rgba(56, 189, 248, 0.08); border-color: rgba(56, 189, 248, 0.3); }
    .search-result-header { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
    .search-result-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; font-weight: 800; }
    .search-result-title { font-weight: 700; color: #f4f4f5; font-size: 0.9rem; flex-grow: 1; }
    .search-result-date { font-size: 0.75rem; color: #71717a; }
    .search-result-snippet { font-size: 0.8rem; color: #a1a1aa; line-height: 1.4; }
    .search-highlight { background: rgba(245, 158, 11, 0.3); color: #fbbf24; padding: 0 3px; border-radius: 2px; }
    
    .term-flash { animation: flashHighlight 1.5s ease; }
    @keyframes flashHighlight {
        0% { background: rgba(56, 189, 248, 0.35); }
        100% { background: transparent; }
    }
    """
    
    combined_css = master_css + "\n" + extra_css
    tpl = tpl.replace("{{MASTER_CSS}}", combined_css)

    week_folders = sorted(list(SEMANAL_DIR.glob("W_*")))
    global_glossary, weeks_lessons_raw, all_lessons_by_date = {}, [], {}
    search_index = []

    for folder in sorted(week_folders, reverse=False):
        w_id = folder.name.replace("_", "")
        config_path = folder / "week_config.json"
        config = {"title": f"Semana {w_id}", "text": "Consolidação das aulas da semana."}
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f: config = json.load(f)
            
        lessons = []
        for file in sorted(folder.glob("*.md")):
            raw_text = file.read_text(encoding='utf-8')
            meta, body = extract_frontmatter_and_content(raw_text)
            
            parts = re.split(r'##\s*Gloss[aá]rio', body, flags=re.IGNORECASE)
            main_content = parts[0]
            glossary_content = parts[1] if len(parts) > 1 else ""

            lesson_num = ""
            num_match = re.search(r'Aula\s*(\d+)', meta.get("titulo", ""), re.IGNORECASE)
            if num_match: lesson_num = num_match.group(1)

            disc_name = meta.get("disciplina", "Geral")
            disc_meta = get_disc_meta(disc_name)
            short_disc = disc_meta["short"]

            date_str = meta.get("data", "")
            wd = ""
            if date_str:
                try:
                    dt = calendar.datetime.date.fromisoformat(date_str)
                    wd_names = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
                    wd = wd_names[dt.weekday()]
                except: pass

            lesson_id = f"{w_id}-{file.stem}"
            html_raw = pandoc_markdown_to_html(main_content)

            if glossary_content:
                for line in glossary_content.strip().split("\n"):
                    line = line.strip()
                    if line.startswith("-") or line.startswith("*"):
                        m_term = re.match(r'[-*]\s*\*\*([^*]+)\*\*:\s*(.*)', line)
                        if m_term:
                            t = m_term.group(1).strip()
                            raw_def = m_term.group(2).strip()
                            clean_def, wiki_url = clean_glossary_definition(raw_def)
                                
                            slug = slugify(t)
                            if slug not in global_glossary:
                                global_glossary[slug] = {"term": t, "def": clean_def, "wiki": wiki_url, "sources": []}
                            elif wiki_url and not global_glossary[slug].get("wiki"):
                                global_glossary[slug]["wiki"] = wiki_url
                                
                            global_glossary[slug]["sources"].append({
                                "id": lesson_id, "name": f"{short_disc} {get_label(lesson_num)}", "date": date_str
                            })
                            # Adicionar no search index
                            search_index.append({
                                "id": "glossary", "title": f"Glossário: {t}", "disc": "Glossário",
                                "short": "GLOSS", "color": "#38bdf8", "bg": "rgba(56,189,248,0.1)", "border": "#38bdf8",
                                "text": f"{t} - {clean_def}", "date": ""
                            })

            lesson_obj = {
                "id": lesson_id, "file": file.name, "meta": meta, "html_raw": html_raw,
                "title": meta.get("titulo", file.stem), "disc": disc_name, "prof": meta.get("professor", "Docente"),
                "date": date_str, "wd": wd, "num": lesson_num, "short": short_disc, "cls": disc_meta["tag"],
                "color": disc_meta["color"], "bg": disc_meta["bg"], "border": disc_meta["border"],
                "order": disc_meta.get("order", 99)
            }
            lessons.append(lesson_obj)
            if date_str: all_lessons_by_date[date_str] = lesson_obj
            
            clean_text = re.sub(r'<[^>]+>', ' ', html_raw)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            search_index.append({
                "id": lesson_id, "title": lesson_obj["title"], "disc": disc_name,
                "short": short_disc, "color": disc_meta["color"], "bg": disc_meta["bg"], "border": disc_meta["border"],
                "text": clean_text, "date": date_str
            })

        weeks_lessons_raw.append({"id": w_id, "config": config, "lessons": lessons})

    glossary_list = [{"term": g["term"], "slug": k} for k, g in global_glossary.items()]

    day_buttons_html, lessons_html, timeline_entries = "", "", ""
    disciplines = {}

    for week in weeks_lessons_raw:
        w_id = week['id']
        first_lesson_id = week['lessons'][0]['id'] if week['lessons'] else ""
        for l in week['lessons']:
            html_linked = linkify(l['html_raw'], glossary_list)
            label = get_label(l["num"])
            
            badge_html = f"<span class='disc-badge' style='background:{l['bg']}; color:{l['color']}; border:1px solid {l['border']};'>{l['disc']} • {l['prof']}</span>"
            lessons_html += f'<section id="{l["id"]}" class="spa-section"><div class="lesson-card"><div class="lesson-metadata">{badge_html} <span style="color:#71717a;">{l["date"]} • {label}</span></div><h1 style="font-size: 1.6rem; margin: 15px 0 25px 0; color: #fff;">{l["title"]}</h1>{html_linked}</div></section>'
            
            d_name = l["disc"]
            if d_name not in disciplines: disciplines[d_name] = {"prof": l["prof"], "short": l["short"], "meta": get_disc_meta(d_name), "lessons": []}
            disciplines[d_name]["lessons"].append(l)

        # Montar mini-pills da semana para a Linha do Tempo
        mini_pills_html = "".join([
            f"<span class='timeline-mini-pill' style='background:{l['bg']}; color:{l['color']}; border:1px solid {l['border']};' onclick=\"event.stopPropagation(); showSection('{l['id']}');\">{l['short']} {get_label(l['num'])}</span>"
            for l in week['lessons']
        ])
        
        timeline_entries += f"""
        <div class='timeline-card' onclick="showSection('{first_lesson_id}')">
            <div class='timeline-dot'></div>
            <span class='timeline-badge'>Semana {w_id[1:]}</span>
            <h4 class='timeline-title'>{week['config']['title']}</h4>
            <p class='timeline-text'>{week['config']['text']}</p>
            <div class='timeline-mini-pills'>{mini_pills_html}</div>
        </div>"""

    # Ordenar por dia da semana
    discipline_view_html = "<details class='collapsible-section' open><summary>Trilhas de Aprendizado (2026.2)</summary><div class='collapsible-content'><div class='discipline-tracks'>"
    
    sorted_disc_names = sorted(
        disciplines.keys(),
        key=lambda d: disciplines[d]["meta"].get("order", 99)
    )

    for d_name in sorted_disc_names:
        d_meta = disciplines[d_name]["meta"]
        prof_label = f"<span style='color:var(--text-dim); opacity:0.8;'>{disciplines[d_name]['prof']}</span>"
        badge_style = f"background:{d_meta['bg']}; color:{d_meta['color']}; border:1px solid {d_meta['border']};"
        discipline_view_html += f"<div class='discipline-row'><span class='disc-badge' style='{badge_style}'>{d_name}</span> <span style='font-size:0.8rem; margin-right:15px;'>{prof_label}</span><div class='lesson-pills'>"
        for l in sorted(disciplines[d_name]["lessons"], key=lambda x: x["date"]):
            pill_style = f"background:{d_meta['bg']}; color:{d_meta['color']}; border:1px solid {d_meta['border']};"
            discipline_view_html += f"<button class='lesson-pill' style='{pill_style}' onclick=\"showSection('{l['id']}')\">{l['short']} {get_label(l['num'])}</button>"
        discipline_view_html += "</div></div>"
    discipline_view_html += "</div></div></details>"

    # Navegação contextual por DISCIPLINA
    nav_map = {}
    for d_name, d_data in disciplines.items():
        disc_lessons = sorted(d_data["lessons"], key=lambda x: x["date"])
        for idx, l in enumerate(disc_lessons):
            prev_id = disc_lessons[idx-1]["id"] if idx > 0 else None
            next_id = disc_lessons[idx+1]["id"] if idx < len(disc_lessons)-1 else None
            nav_map[l["id"]] = {
                "prev": prev_id,
                "next": next_id,
                "label": f"{l['short']} • {get_label(l['num'])}"
            }

    # Glossário Final com Botão Wikipedia Formatado Uniformemente
    glossary_html = ""
    for k in sorted(global_glossary.keys(), key=lambda x: normalize_sort(global_glossary[x]["term"])):
        g = global_glossary[k]
        g['sources'].sort(key=lambda x: x['date'])
        ps = g['sources'][0] if g['sources'] else None
        source_btns = f"<button class='action-btn' onclick=\"showSection('{ps['id']}')\">{ps['name']}</button>" if ps else ""
        wiki_btn = f"<a href='{g['wiki']}' target='_blank' class='action-btn wiki-btn'>Wikipedia ↗</a>" if g.get("wiki") else ""
        glossary_html += f"<div class='glossary-item' id='term-{slugify(g['term'])}'><span class='glossary-term'>{g['term']}</span><div class='glossary-def'>{g['def']}</div><div class='glossary-footer'><div style='display:flex;gap:8px'>{source_btns}</div>{wiki_btn}</div></div>"

    # --- CALENDÁRIO 2026.2 (Com display isolado de cada mês) ---
    month_selector_html = '<div class="month-selector">'
    calendar_views_html = ""
    
    current_month = 8
    for m in [8, 9, 10, 11, 12]:
        is_active = (m == current_month)
        m_name = ["Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"][m-8]
        month_selector_html += f'<button id="pill-m{m}" class="month-pill {"active" if is_active else ""}" onclick="changeMonth(\'m{m}\')">{m_name}</button>'
        
        cal = calendar.Calendar(firstweekday=0)
        days = cal.monthdatescalendar(2026, m)
        
        cal_grid = '<div class="calendar-grid"><div class="calendar-header-day">Seg</div><div class="calendar-header-day">Ter</div><div class="calendar-header-day">Qua</div><div class="calendar-header-day">Qui</div><div class="calendar-header-day">Sex</div><div class="calendar-header-day">Sáb</div>'
        
        for week in days:
            for day in week[:6]:
                d_str = day.isoformat()
                d_num = day.day
                in_month = (day.month == m)
                cls = "calendar-day"
                if not in_month: cls += " other-month"
                
                lesson_info = all_lessons_by_date.get(d_str)
                if lesson_info and in_month:
                    cls += f" active-lesson"
                    disc_tag = lesson_info["short"]
                    badge_style = f"background:{lesson_info['bg']}; color:{lesson_info['color']}; border:1px solid {lesson_info['border']};"
                    tag_html = f"<span class='cal-tag' style='{badge_style}'>{disc_tag} {lesson_info['num']}</span>"
                    click_attr = f"onclick=\"showSection('{lesson_info['id']}')\""
                    cal_grid += f'<div class="{cls}" data-disc="{disc_tag}" {click_attr}><span class="day-number">{d_num}</span>{tag_html}</div>'
                else:
                    cal_grid += f'<div class="{cls}"><span class="day-number">{d_num}</span></div>'
                    
        cal_grid += '</div>'
        display_style = "display: block;" if is_active else "display: none;"
        calendar_views_html += f'<div id="month-m{m}" class="calendar-view {"active" if is_active else ""}" style="{display_style}">{cal_grid}</div>'

    month_selector_html += '</div>'

    # Injeção Final
    final_html = tpl.replace("{{DISCIPLINE_TRACKS}}", discipline_view_html)
    final_html = final_html.replace("{{TIMELINE_ENTRIES}}", timeline_entries)
    final_html = final_html.replace("{{MONTH_SELECTOR}}", month_selector_html)
    final_html = final_html.replace("{{CALENDAR_VIEWS}}", calendar_views_html)
    final_html = final_html.replace("{{LESSONS_HTML}}", lessons_html)
    final_html = final_html.replace("{{GLOSSARY_HTML}}", glossary_html)
    final_html = final_html.replace("{{NAV_MAP_JSON}}", json.dumps(nav_map, ensure_ascii=False))
    final_html = final_html.replace("{{SEARCH_INDEX_JSON}}", json.dumps(search_index, ensure_ascii=False))
    final_html = final_html.replace("{{TOTAL_TERMOS}}", str(len(global_glossary)))

    out_file = PORTAL_DIR / "Recap_Master_S2.html"
    out_file.write_text(final_html, encoding="utf-8")
    
    # Mirror para index.html
    (PORTAL_DIR / "index.html").write_text(final_html, encoding="utf-8")

    print(f"🎉 Recap_Master_S2.html gerado com sucesso!")

if __name__ == "__main__":
    build()
