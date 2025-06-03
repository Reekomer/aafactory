#!/usr/bin/env bash

# Use libtcmalloc for better memory management
TCMALLOC="$(ldconfig -p | grep -Po "libtcmalloc.so.\d" | head -n 1)"
export LD_PRELOAD="${TCMALLOC}"

# Download models
huggingface-cli download LeonJoe13/Sonic --local-dir  ./models/sonic
huggingface-cli download stabilityai/stable-video-diffusion-img2vid-xt --local-dir  ./models/sonic/stable-video-diffusion-img2vid-xt
huggingface-cli download openai/whisper-tiny --local-dir ./models/sonic/whisper-tiny
mv models/sonic/stable-video-diffusion-img2vid-xt/svd_xt.safetensors models/checkpoints/
mv models/sonic/Sonic/* models/sonic/

# Start ComfyUI
python3 main.py --listen 0.0.0.0
