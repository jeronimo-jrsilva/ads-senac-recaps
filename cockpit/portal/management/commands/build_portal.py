import os
import re
import json
import calendar
import unicodedata
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand
from portal.models import Semana, Aula, Disciplina, Professor, GlossarioTermo

REPO_ROOT = Path("/home/jeronimo/G-Sync/ads-senac-recaps")
ENGINE_DIR = REPO_ROOT / "engine"
PORTAL_DIR = REPO_ROOT / "portal"


def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)


def normalize_sort(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower()


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
    except Exception:
        paragraphs = md_processed.split("\n\n")
        return "".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs)


def linkify(html_content, glossary_terms):
    soup_tokens = re.split(r'(<[^>]+>)', html_content)
    sorted_terms = sorted(glossary_terms, key=lambda x: len(x['term']), reverse=True)

    in_code_block = False
    in_heading = False

    for i, token in enumerate(soup_tokens):
        if not token:
            continue

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
    if not num_str:
        return ""
    if str(num_str).isdigit():
        return f"Aula {int(num_str):02d}"
    return str(num_str)


class Command(BaseCommand):
    help = "Compila o portal estático a partir do banco de dados relacional via Django ORM"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Executando build_portal via Django ORM..."))

        tpl_path = ENGINE_DIR / "template_full_s2.html"
        css_path = ENGINE_DIR / "styles.css"

        if not tpl_path.exists():
            self.stderr.write(f"Erro: template não encontrado em {tpl_path}")
            return

        tpl = tpl_path.read_text(encoding='utf-8')
        master_css = css_path.read_text(encoding='utf-8') if css_path.exists() else ""

        # Obter termos do glossário
        termos_qs = GlossarioTermo.objects.all()
        glossary_list = [{"term": t.termo, "slug": t.slug} for t in termos_qs]

        # Processar Semanas e Aulas via Django ORM
        semanas_qs = Semana.objects.prefetch_related('aulas__disciplina', 'aulas__professor').order_by('numero')

        weeks_data = []
        search_index = []
        disciplines = {}
        all_lessons_by_date = {}

        for sem in semanas_qs:
            w_id = sem.codigo
            lessons = []

            for aula in sem.aulas.all().order_by('data_aula', 'id'):
                disc = aula.disciplina
                prof = aula.professor

                parts = re.split(r'##\s*Gloss[aá]rio', aula.conteudo_markdown, flags=re.IGNORECASE)
                main_md = parts[0]

                html_raw = pandoc_markdown_to_html(main_md)
                clean_text = re.sub(r'<[^>]+>', ' ', html_raw)
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()

                lesson_id = f"{w_id}-{aula.slug_arquivo}"

                # Mapeamento de calendário
                if aula.data_aula:
                    all_lessons_by_date[aula.data_aula] = {
                        "id": lesson_id,
                        "title": aula.titulo,
                        "disc": disc.nome,
                        "short": disc.sigla,
                        "color": disc.cor,
                        "bg": disc.bg_color,
                        "border": disc.border_color,
                        "num": aula.rotulo
                    }

                # Search index
                search_index.append({
                    "id": lesson_id,
                    "title": aula.titulo,
                    "disc": disc.nome,
                    "short": disc.sigla,
                    "color": disc.cor,
                    "bg": disc.bg_color,
                    "border": disc.border_color,
                    "text": clean_text,
                    "date": aula.data_aula
                })

                lesson_obj = {
                    "id": lesson_id,
                    "title": aula.titulo,
                    "disc": disc.nome,
                    "prof": prof.nome,
                    "date": aula.data_aula,
                    "rotulo": aula.rotulo,
                    "short": disc.sigla,
                    "color": disc.cor,
                    "bg": disc.bg_color,
                    "border": disc.border_color,
                    "html_raw": html_raw,
                    "num": aula.rotulo
                }
                lessons.append(lesson_obj)

            weeks_data.append({
                "id": w_id,
                "config": {"title": sem.titulo, "text": sem.descricao},
                "lessons": lessons
            })

        # Adicionar termos do glossário no search index
        for t in termos_qs:
            search_index.append({
                "id": "glossary",
                "title": f"Glossário: {t.termo}",
                "disc": "Glossário",
                "short": "GLOSS",
                "color": "#38bdf8",
                "bg": "rgba(56,189,248,0.1)",
                "border": "#38bdf8",
                "text": f"{t.termo} - {t.definicao}",
                "date": ""
            })

        # Renderizar HTML das aulas e timeline
        lessons_html = ""
        timeline_entries = ""

        for week in weeks_data:
            w_id = week['id']
            first_lesson_id = week['lessons'][0]['id'] if week['lessons'] else ""

            for l in week['lessons']:
                html_linked = linkify(l['html_raw'], glossary_list)
                label = l["rotulo"]
                date_and_label = f'{l["date"]} • {label}' if label else l["date"]

                badge_html = f"<span class='disc-badge' style='background:{l['bg']}; color:{l['color']}; border:1px solid {l['border']};'>{l['disc']} • {l['prof']}</span>"

                # Status de Revisão discreto
                is_revisao = w_id in ["W11", "W12"]
                if is_revisao:
                    status_html = "<span class='lesson-status em-revisao' style='color: #d29922; font-size: 0.72rem; opacity: 0.85; margin-left: auto; display: inline-flex; align-items: center; gap: 5px; letter-spacing: 0.3px;' title='Transcrição automática em processo de validação'><span style='font-size: 8px;'>◐</span> Em revisão</span>"
                else:
                    status_html = "<span class='lesson-status revisado' style='color: #3fb950; font-size: 0.72rem; opacity: 0.85; margin-left: auto; display: inline-flex; align-items: center; gap: 5px; letter-spacing: 0.3px;' title='Conteúdo revisado e aprovado'><span style='font-size: 8px;'>●</span> Revisado</span>"

                lessons_html += f'<section id="{l["id"]}" class="spa-section"><div class="lesson-card"><div class="lesson-metadata">{badge_html} <span style="color:#71717a;">{date_and_label}</span>{status_html}</div><h1 style="font-size: 1.6rem; margin: 15px 0 25px 0; color: #fff;">{l["title"]}</h1>{html_linked}</div></section>'

                d_name = l["disc"]
                if d_name not in disciplines:
                    prof_display = l["prof"]
                    if "linguagem c" in d_name.lower():
                        prof_display = "Vinicius-Matheus"
                    disciplines[d_name] = {"prof": prof_display, "short": l["short"], "color": l["color"], "bg": l["bg"], "border": l["border"], "lessons": []}
                disciplines[d_name]["lessons"].append(l)

            # Mini pills da Timeline
            mini_pills_html = "".join([
                f"<span class='timeline-mini-pill' style='background:{l['bg']}; color:{l['color']}; border:1px solid {l['border']};' onclick=\"event.stopPropagation(); showSection('{l['id']}');\">{(l['short'] + ' ' + l['rotulo']).strip()}</span>"
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

        # Renderizar Trilhas de Aprendizado
        discipline_view_html = "<details class='collapsible-section' open><summary>Trilhas de Aprendizado (2026.2)</summary><div class='collapsible-content'><div class='discipline-tracks'>"

        disc_objs = {d.nome: d.ordem for d in Disciplina.objects.all()}
        sorted_disc_names = sorted(disciplines.keys(), key=lambda d: disc_objs.get(d, 99))

        for d_name in sorted_disc_names:
            d_data = disciplines[d_name]
            prof_label = f"<span style='color:var(--text-dim); opacity:0.8;'>{d_data['prof']}</span>"
            badge_style = f"background:{d_data['bg']}; color:{d_data['color']}; border:1px solid {d_data['border']};"
            discipline_view_html += f"<div class='discipline-row'><span class='disc-badge' style='{badge_style}'>{d_name}</span> <span style='font-size:0.8rem; margin-right:15px;'>{prof_label}</span><div class='lesson-pills'>"
            for l in sorted(d_data["lessons"], key=lambda x: x["date"]):
                pill_style = f"background:{d_data['bg']}; color:{d_data['color']}; border:1px solid {d_data['border']};"
                pill_text = f"{l['short']} {l['rotulo']}".strip()
                discipline_view_html += f"<button class='lesson-pill' style='{pill_style}' onclick=\"showSection('{l['id']}')\">{pill_text}</button>"
            discipline_view_html += "</div></div>"
        discipline_view_html += "</div></div></details>"

        # Nav map por disciplina
        nav_map = {}
        for d_name, d_data in disciplines.items():
            disc_lessons = sorted(d_data["lessons"], key=lambda x: x["date"])
            for idx, l in enumerate(disc_lessons):
                prev_id = disc_lessons[idx - 1]["id"] if idx > 0 else None
                next_id = disc_lessons[idx + 1]["id"] if idx < len(disc_lessons) - 1 else None
                nav_map[l["id"]] = {
                    "prev": prev_id,
                    "next": next_id,
                    "label": f"{l['short']} • {l['rotulo']}"
                }

        # Glossário
        glossary_html = ""
        for t in GlossarioTermo.objects.prefetch_related('aulas__disciplina', 'aulas__semana').all().order_by('termo'):
            source_btns = "".join([
                f"<button class='action-btn' onclick=\"showSection('{a.semana.codigo}-{a.slug_arquivo}')\">{a.disciplina.sigla} {a.rotulo}</button>"
                for a in t.aulas.all().order_by('data_aula')
            ])
            wiki_btn = f"<a href='{t.wiki_url}' target='_blank' class='action-btn wiki-btn'>Wikipedia ↗</a>" if t.wiki_url else ""
            glossary_html += f"<div class='glossary-item' id='term-{t.slug}'><span class='glossary-term'>{t.termo}</span><div class='glossary-def'>{t.definicao}</div><div class='glossary-footer'><div style='display:flex;gap:8px'>{source_btns}</div>{wiki_btn}</div></div>"

        # Calendário
        month_selector_html = '<div class="month-selector">'
        calendar_views_html = ""

        current_month = 8
        for m in [8, 9, 10, 11, 12]:
            is_active = (m == current_month)
            m_name = ["Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"][m - 8]
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
                    if not in_month:
                        cls += " other-month"

                    lesson_info = all_lessons_by_date.get(d_str)
                    if lesson_info and in_month:
                        cls += " active-lesson"
                        disc_tag = lesson_info["short"]
                        badge_style = f"background:{lesson_info['bg']}; color:{lesson_info['color']}; border:1px solid {lesson_info['border']};"
                        tag_html = f"<span class='cal-tag' style='{badge_style}'>{disc_tag} {lesson_info['num']}</span>"
                        l_id = lesson_info["id"]
                        cal_grid += f'<div class="{cls}" onclick="showSection(\'{l_id}\')"><span class="day-number">{d_num}</span>{tag_html}</div>'
                    else:
                        cal_grid += f'<div class="{cls}"><span class="day-number">{d_num}</span></div>'

            cal_grid += '</div>'
            display_style = "display: block;" if is_active else "display: none;"
            calendar_views_html += f'<div id="month-m{m}" class="calendar-view {"active" if is_active else ""}" style="{display_style}">{cal_grid}</div>'

        month_selector_html += '</div>'

        # Substituições finais
        total_aulas_count = sum(len(w['lessons']) for w in weeks_data)

        final_html = tpl
        final_html = final_html.replace("{{MASTER_CSS}}", master_css)
        final_html = final_html.replace("{{DISCIPLINE_TRACKS}}", discipline_view_html)
        final_html = final_html.replace("{{TIMELINE_ENTRIES}}", timeline_entries)
        final_html = final_html.replace("{{MONTH_SELECTOR}}", month_selector_html)
        final_html = final_html.replace("{{CALENDAR_VIEWS}}", calendar_views_html)
        final_html = final_html.replace("{{LESSONS_HTML}}", lessons_html)
        final_html = final_html.replace("{{GLOSSARY_HTML}}", glossary_html)
        final_html = final_html.replace("{{NAV_MAP_JSON}}", json.dumps(nav_map, ensure_ascii=False))
        final_html = final_html.replace("{{SEARCH_INDEX_JSON}}", json.dumps(search_index, ensure_ascii=False))
        final_html = final_html.replace("{{TOTAL_SEMANAS}}", str(len(weeks_data)))
        final_html = final_html.replace("{{TOTAL_AULAS}}", str(total_aulas_count))
        final_html = final_html.replace("{{TOTAL_TERMOS}}", str(len(termos_qs)))

        outputs = [
            REPO_ROOT / "Recap_Master_S2.html",
            REPO_ROOT / "index.html",
            PORTAL_DIR / "Recap_Master_S2.html",
            PORTAL_DIR / "index.html",
        ]

        for out_file in outputs:
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(final_html, encoding='utf-8')
            self.stdout.write(f"  ✅ Gerado: {out_file.name} ({len(final_html)/1024:.1f} KB)")

        self.stdout.write(self.style.SUCCESS("🎉 Build do Portal via Django ORM concluído com sucesso!"))
