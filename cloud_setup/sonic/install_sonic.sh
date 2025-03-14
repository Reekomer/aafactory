#!/bin/bash
. /venv/bin/activate
pip install poetry
poetry install

huggingface-cli download LeonJoe13/Sonic --local-dir  ./ComfyUI/models/sonic
huggingface-cli download stabilityai/stable-video-diffusion-img2vid-xt --local-dir  ./ComfyUI/models/sonic/stable-video-diffusion-img2vid-xt
huggingface-cli download openai/whisper-tiny --local-dir ./ComfyUI/models/sonic/whisper-tiny
mv ComfyUI/models/sonic/stable-video-diffusion-img2vid-xt/svd_xt.safetensors ComfyUI/models/checkpoints/
mv ComfyUI/models/sonic/Sonic/* ComfyUI/models/sonic/