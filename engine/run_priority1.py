#!/usr/bin/env python3
import os, sys, time
sys.path.insert(0, "/home/jeronimo/G-Sync/ads-senac-recaps/engine")
from transcribe_ads_gpu import load_gpu_model, transcribe_full

tasks = [
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Voz 260908_081151.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/08-set-ter-poo.txt"
    ),
    (
        "/home/jeronimo/G-Sync/Audios_Faculdade/00_Inbox_Tablet/Voz 260919_083810.m4a",
        "/home/jeronimo/G-Sync/ads-senac-recaps/s2_2026_2/00_transcricoes_brutas/19-set-sab-extensao.txt"
    )
]

print("🚀 Iniciando Motor de Transcrição ADS - Prioridade 1...")
model = load_gpu_model("small")

for audio_path, out_path in tasks:
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"⏩ Já existe: {out_path} ({os.path.getsize(out_path)} bytes)")
        continue
    transcribe_full(model, audio_path, out_path)

print("🎉 Prioridade 1 concluída!")
