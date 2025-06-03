# Stage 1: Base image with common dependencies
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Prevents prompts from packages asking for user input during installation
ENV DEBIAN_FRONTEND=noninteractive
# Prefer binary wheels over source distributions for faster pip installations
ENV PIP_PREFER_BINARY=1
# Ensures output from python is printed immediately to the terminal without buffering
ENV PYTHONUNBUFFERED=1 
# Speed up some cmake builds
ENV CMAKE_BUILD_PARALLEL_LEVEL=8

# Install Python, git and other necessary tools
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    libglib2.0-0 \
    git \
    wget \
    libgl1 \
    && ln -sf /usr/bin/python3.10 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip

# Clean up to reduce image size
RUN apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install comfy-cli
RUN pip install comfy-cli

# Install ComfyUI
RUN /usr/bin/yes | comfy --workspace /comfyui install --cuda-version 11.8 --nvidia --version 0.3.30

# Install runpod
RUN pip install runpod requests uv

# Go back to the root
WORKDIR /

# Add scripts
ADD pyproject.toml restore_snapshot.sh ./
RUN chmod +x /restore_snapshot.sh
# RUN uv sync --no-cache

# Optionally copy the snapshot file
ADD *snapshot*.json /

# Install ComfyUI
RUN ./restore_snapshot.sh

# Change working directory to ComfyUI
WORKDIR /comfyui

# Configure civitdl with API key
COPY server-requirements.txt /comfyui/server-requirements.txt
COPY start.sh /comfyui/start.sh
RUN pip install -r server-requirements.txt

RUN chmod +x /comfyui/start.sh
CMD ["/comfyui/start.sh"]