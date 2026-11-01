#!/usr/bin/env python3
"""
Execução do Lote de Outubro via GPU Nativa (ROCm / whisper.cpp)
"""
import os
import sys

sys.path.insert(0, "/home/jeronimo/G-Sync/ads-senac-recaps/engine")
from transcribe_ads_gpu import transcribe_file_whisper_cpp

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
    # Programa de Líderes (armazenado em extra_lideres/)
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Lideranca 15-10-26.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/extra_lideres/15-out-qui-lideranca.txt"
    ),
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Voz 261029_172850.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/extra_lideres/29-out-qui-lideranca.txt"
    )
]

print("=" * 60)
print("🚀 MOTOR ADS 2026.2 - TRANSCRIÇÃO GPU ROCm (RADEON RX 7600)")
print("=" * 60)

for audio_path, out_path in tasks:
    # Se já existir e tiver tamanho expressivo (>25KB), pula
    if os.path.exists(out_path) and os.path.getsize(out_path) > 25000:
        print(f"⏩ Já concluído: {os.path.basename(out_path)} ({os.path.getsize(out_path)/1024:.1f} KB)")
        continue
    transcribe_file_whisper_cpp(audio_path, out_path)

print("\n🎉 Todas as transcrições do lote foram finalizadas com sucesso!")
