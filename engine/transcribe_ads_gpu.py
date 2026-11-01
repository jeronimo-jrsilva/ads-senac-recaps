#!/usr/bin/env python3
"""
Motor de Transcrição e Triagem ADS 2026.2 (GPU AMD Radeon RX 7600 ROCm / whisper.cpp)
=============================================================================
Aceleração nativa por hardware:
- ROCm / HIP (HSA_OVERRIDE_GFX_VERSION=11.0.0)
- whisper-cli compilado com suporte a GPU
- Modelo padrão: ggml-small.bin (~23x mais rápido que tempo real)
- Timestamps padronizados [HH:MM:SS]
"""

import argparse
import datetime
import os
import re
import subprocess
import sys
import tempfile
import time

WHISPER_BIN = "/home/jeronimo/whisper.cpp/build/bin/whisper-cli"
MODEL_DEFAULT = "/home/jeronimo/whisper.cpp/models/ggml-small.bin"
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
        # Padrão 2: Lideranca DD-MM-YY.m4a ou outro
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

    # Classificação
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


def transcribe_file_whisper_cpp(audio_path: str, output_path: str, model_path: str = MODEL_DEFAULT):
    meta = parse_recording_metadata(audio_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"\n🎙️ Transcrevendo via ROCm GPU: {meta['filename']} ({meta['duration_str']})")
    print(f"   -> Destino: {os.path.basename(output_path)}")
    t0 = time.time()

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = os.path.join(tmpdir, "input.wav")
        # Conversão rápida para 16kHz Mono 16-bit
        conv_cmd = [
            "ffmpeg", "-y", "-i", audio_path,
            "-ar", "16000", "-ac", "1", "-sample_fmt", "s16",
            wav_path
        ]
        subprocess.run(conv_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        env = os.environ.copy()
        env["HSA_OVERRIDE_GFX_VERSION"] = "11.0.0"

        whisper_cmd = [
            WHISPER_BIN,
            "-m", model_path,
            "-f", wav_path,
            "-l", "pt",
            "-t", "8",
            "-np"
        ]

        proc = subprocess.Popen(
            whisper_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )

        lines = []
        raw_output, stderr_output = proc.communicate()

        # Converte formato [00:00:00.000 --> 00:00:06.000] em [00:00:00]
        pattern = re.compile(r"\[(\d{2}:\d{2}:\d{2})\.\d+ --> \d{2}:\d{2}:\d{2}\.\d+\]\s*(.*)")
        for line in raw_output.splitlines():
            line = line.strip()
            if not line:
                continue
            m = pattern.match(line)
            if m:
                ts = m.group(1)
                txt = m.group(2).strip()
                if txt:
                    # Deduplicação simples de stuttering consecutivo
                    if lines and lines[-1].endswith(txt):
                        continue
                    lines.append(f"[{ts}] {txt}")
            else:
                lines.append(line)

    header = f"""# =====================================================================
# ARQUIVO DE ORIGEM : {meta['filename']}
# DATA DA GRAVAÇÃO  : {meta['start_dt'].strftime('%Y-%m-%d')} ({meta['weekday_pt']})
# HORÁRIO (INÍCIO-FIM): {meta['start_dt'].strftime('%H:%M:%S')} -> {meta['end_dt'].strftime('%H:%M:%S')} ({meta['duration_str']})
# CLASSIFICAÇÃO     : {meta['categoria']} | {meta['disciplina_sugerida']}
# ENTRA NO PORTAL?  : {'SIM' if meta['entra_portal'] else 'NÃO (Extra-grade)'}
# =====================================================================

"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")

    elapsed = time.time() - t0
    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ Concluído em {elapsed:.1f}s ({len(lines)} segmentos, {size_kb:.1f} KB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motor de Transcrição ADS ROCm")
    parser.add_argument("input", nargs="?", help="Arquivo de áudio de entrada")
    parser.add_argument("output", nargs="?", help="Arquivo de texto de saída")
    args = parser.parse_args()

    if args.input and args.output:
        transcribe_file_whisper_cpp(args.input, args.output)
    else:
        print("Uso: transcribe_ads_gpu.py <audio_in> <text_out>")
