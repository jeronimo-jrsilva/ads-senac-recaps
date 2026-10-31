#!/usr/bin/env python3
import os, sys
sys.path.insert(0, "/home/jeronimo/G-Sync/ads-senac-recaps/engine")
from transcribe_ads_gpu import load_gpu_model, transcribe_full

tasks = [
    # Aulas ADS Outubro
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Voz 261020_081409.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/20-out-ter-poo.txt"
    ),
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Voz 261021_082417.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/21-out-qua-c.txt"
    ),
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Voz 261022_081548.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/22-out-qui-c-extensao.txt"
    ),
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Voz 261023_081032.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/23-out-sex-bd.txt"
    ),
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Voz 261029_082039.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/29-out-qui-c.txt"
    ),
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Voz 261029_185426.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/29-out-qui-bd-noite.txt"
    ),
    # Programa de Líderes (vai direto para extra_lideres/)
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Lideranca 15-10-26.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/extra_lideres/15-out-qui-lideranca.txt"
    ),
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Voz 261029_172850.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/extra_lideres/29-out-qui-lideranca.txt"
    )
]

print("🚀 Iniciando Motor de Transcrição ADS - Lote de Outubro...")
model = load_gpu_model("small")

for audio_path, out_path in tasks:
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"⏩ Já existe: {out_path} ({os.path.getsize(out_path)} bytes)")
        continue
    transcribe_full(model, audio_path, out_path)

print("🎉 Lote de Outubro concluído!")
