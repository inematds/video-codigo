#!/usr/bin/env bash
# Instala o video-codigo como skill do Claude Code (e do Codex) e prepara o render.
# Uso: bash instalar.sh
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
for d in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
  mkdir -p "$d"
  if [ -e "$d/video-codigo" ] && [ ! -L "$d/video-codigo" ]; then echo "  · $d/video-codigo já existe (não mexi)"; continue; fi
  ln -sfn "$AQUI" "$d/video-codigo" && echo "  ✓ skill em $d/video-codigo"
done
bash "$AQUI/scripts/preparar-entorno.sh"
echo
echo "Voz local (opcional): precisa do inemavox com Chatterbox e Whisper (ver README › Voz)."
echo "Teste: no Claude Code, peça \"/video-codigo faz um vídeo de 30 s sobre <seu produto>\"."
