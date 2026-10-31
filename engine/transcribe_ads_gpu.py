#!/usr/bin/env python3
"""
Motor de Transcrição e Triagem ADS 2026.2 (GPU RX 7600 ROCm / Faster-Whisper)
=============================================================================
Melhorias v2.0:
1. Triagem automática por data, dia da semana e janela de horário:
   - Quinta 17h00..18h35 ou nome 'Lideranca' -> extra_lideres/ (FORA DA GRADE)
   - Segunda a Sexta 08h00..13h30 -> AULA_ADS_MANHA
   - Quinta 18h40..22h00 -> AULA_ADS_NOITE (Banco de Dados / Reposição)
   - Sábado -> SABADO_LETIVO_OU_EXTENSAO
2. Modo --sample: extrai amostras rápidas (minuto 2 e minuto 15) em <5s na GPU
   para identificar professor, disciplina e tema antes da transcrição completa.
3. Transcrição completa com marcação de tempo [HH:MM:SS] e anti-loop
   (condition_on_previous_text=False + vad_filter=True).
"""

import argparse
import datetime
import os
import re
import subprocess
import sys
import tempfile
import time

os.environ.setdefault("HSA_OVERRIDE_GFX_VERSION", "11.0.0")
from faster_whisper import WhisperModel

INBOX_DEFAULT = "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet"
OUT_DIR_DEFAULT = "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas"
DIAS_PT = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
MESES_PT = ["", "jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def get_duration(filepath: str) -> float:
    try:
        out = subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                filepath,
            ],
            text=True,
        ).strip()
        return float(out) if out else 0.0
    except Exception:
        return 0.0


def parse_recording_metadata(filepath: str) -> dict:
    bname = os.path.basename(filepath)
    dur_s = get_duration(filepath)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))

    # Padrão 1: Voz YYMMDD_HHMMSS.m4a
    m = re.match(r"Voz (\d{2})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})\.m4a", bname)
    if m:
        yy, mm, dd, hh, mi, ss = map(int, m.groups())
        start_dt = datetime.datetime(2000 + yy, mm, dd, hh, mi, ss)
        end_dt = start_dt + datetime.timedelta(seconds=dur_s)
    else:
        # Padrão 2: Lideranca DD-MM-YY.m4a ou outro nome -> usa mtime - duração
        m2 = re.search(r"(\d{2})-(\d{2})-(\d{2})", bname)
        end_dt = mtime
        start_dt = end_dt - datetime.timedelta(seconds=dur_s)
        if m2:
            dd, mm, yy = map(int, m2.groups())
            start_dt = start_dt.replace(year=2000 + yy, month=mm, day=dd)
            end_dt = start_dt + datetime.timedelta(seconds=dur_s)

    wd = start_dt.weekday()
    dia_str = DIAS_PT[wd]
    hh_float = start_dt.hour + start_dt.minute / 60.0

    # Regras de Triagem por Horário e Dia da Semana
    if "lideranca" in bname.lower() or (wd == 3 and 16.8 <= hh_float <= 18.5):
        categoria = "PROGRAMA_DE_LIDERES"
        entra_portal = False
        disciplina_sugerida = "Programa de Líderes (Extra-Grade)"
    elif wd == 5:
        categoria = "SABADO_LETIVO_EXTENSAO"
        entra_portal = True
        disciplina_sugerida = "Projeto de Extensão / Sábado Letivo"
    elif 7.5 <= hh_float <= 13.5:
        categoria = "AULA_ADS_MANHA"
        entra_portal = True
        mapa_manha = {
            0: "Projeto Integrador (PI)",
            1: "POO (Prof. Tibério)",
            2: "Linguagem C (Prof. Vinícius)",
            3: "Linguagem C / Extensão",
            4: "Banco de Dados (Prof. Alexandre)",
        }
        disciplina_sugerida = mapa_manha.get(wd, "Aula ADS Manhã")
    elif wd == 3 and hh_float >= 18.5:
        categoria = "AULA_ADS_NOITE"
        entra_portal = True
        disciplina_sugerida = "Banco de Dados (Prof. Alexandre - Quinta Noite)"
    else:
        categoria = "OUTRO_HORARIO"
        entra_portal = True
        disciplina_sugerida = "A Identificar"

    return {
        "filepath": filepath,
        "filename": bname,
        "start_dt": start_dt,
        "end_dt": end_dt,
        "duration_s": dur_s,
        "duration_str": f"{int(dur_s // 3600)}h{int((dur_s % 3600) // 60):02d}m",
        "weekday_pt": dia_str,
        "categoria": categoria,
        "entra_portal": entra_portal,
        "disciplina_sugerida": disciplina_sugerida,
    }


def load_gpu_model(model_name: str = "small"):
    try:
        print(f"🚀 Carregando modelo '{model_name}' na GPU (ROCm/CUDA float16)...")
        return WhisperModel(model_name, device="cuda", compute_type="float16")
    except Exception as e:
        print(f"⚠️ Fallback para CPU int8 ({e})...")
        return WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=8)


def sample_audio_triage(model: WhisperModel, filepath: str, sample_duration: int = 90) -> str:
    """Extrai dois trechos curtos (início + meio) para identificar tema e professor rapidamente."""
    meta = parse_recording_metadata(filepath)
    dur = meta["duration_s"]
    offsets = [120] if dur < 1200 else [180, int(dur * 0.45)]
    snippets = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, offset in enumerate(offsets):
            if offset >= dur:
                offset = max(0, int(dur / 4))
            wav_path = os.path.join(tmpdir, f"sample_{idx}.wav")
            subprocess.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-ss", str(offset), "-t", str(sample_duration),
                    "-i", filepath, "-ar", "16000", "-ac", "1", wav_path,
                ],
                check=False,
            )
            if os.path.exists(wav_path):
                segs, _ = model.transcribe(
                    wav_path,
                    language="pt",
                    beam_size=2,
                    vad_filter=True,
                    condition_on_previous_text=False,
                )
                txt = " ".join(s.text.strip() for s in segs)
                mm, ss = divmod(offset, 60)
                hh, mm = divmod(mm, 60)
                snippets.append(f"[{hh:02d}:{mm:02d}:{ss:02d}] {txt}")

    return "\n".join(snippets)


def format_ts(seconds: float) -> str:
    s = int(seconds)
    hh, rem = divmod(s, 3600)
    mm, ss = divmod(rem, 60)
    return f"{hh:02d}:{mm:02d}:{ss:02d}"


def transcribe_full(model: WhisperModel, filepath: str, out_path: str, tag_suffix: str = ""):
    meta = parse_recording_metadata(filepath)
    t0 = time.time()
    print(f"\n🎙️ Transcrevendo: {meta['filename']} ({meta['duration_str']}) -> {os.path.basename(out_path)}")

    segments, info = model.transcribe(
        filepath,
        language="pt",
        beam_size=3,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=600),
        condition_on_previous_text=False,
    )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# =====================================================================\n")
        f.write(f"# ARQUIVO DE ORIGEM : {meta['filename']}\n")
        f.write(f"# DATA DA GRAVAÇÃO  : {meta['start_dt'].strftime('%Y-%m-%d')} ({meta['weekday_pt']})\n")
        f.write(f"# HORÁRIO (INÍCIO-FIM): {meta['start_dt'].strftime('%H:%M:%S')} -> {meta['end_dt'].strftime('%H:%M:%S')} ({meta['duration_str']})\n")
        f.write(f"# CLASSIFICAÇÃO     : {meta['categoria']} | {meta['disciplina_sugerida']}\n")
        f.write(f"# ENTRA NO PORTAL?  : {'SIM' if meta['entra_portal'] else 'NÃO (Extra-Grade)'}\n")
        f.write("# =====================================================================\n\n")

        count = 0
        for seg in segments:
            ts = format_ts(seg.start)
            text = seg.text.strip()
            if text:
                f.write(f"[{ts}] {text}\n")
                count += 1
                if count % 50 == 0:
                    f.flush()
                    print(f"  ... [{ts}] ({count} segmentos processados)", flush=True)

    elapsed = time.time() - t0
    print(f"✅ Concluído em {elapsed:.1f}s ({count} segmentos) -> {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Motor GPU de Triagem e Transcrição ADS")
    parser.add_argument("--sample", nargs="+", help="Arquivos .m4a para amostragem rápida (90s)")
    parser.add_argument("--transcribe", nargs="+", help="Pares ou arquivos .m4a para transcrição completa")
    parser.add_argument("--model", default="small", help="Modelo Whisper (small, medium, large-v3-turbo)")
    args = parser.parse_args()

    model = load_gpu_model(args.model)

    if args.sample:
        for path in args.sample:
            meta = parse_recording_metadata(path)
            print("=" * 80)
            print(f"📄 ARQUIVO: {meta['filename']} | {meta['start_dt'].strftime('%d/%m/%Y (%a) %H:%M')} -> {meta['end_dt'].strftime('%H:%M')} ({meta['duration_str']})")
            print(f"🏷️ SUGESTÃO POR HORÁRIO: {meta['categoria']} -> {meta['disciplina_sugerida']} (Portal: {meta['entra_portal']})")
            sample_txt = sample_audio_triage(model, path)
            print(f"🗣️ AMOSTRA DO ÁUDIO:\n{sample_txt}\n")


if __name__ == "__main__":
    main()
