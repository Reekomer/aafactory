# AI Avatar Factory

⚡ AI Avatar Factory is an interface for creating and managing AI avatars. ⚡

[![Website](https://img.shields.io/badge/website-000000?style=for-the-badge&logo=AAFactory.xyz&logoColor=white
)](https://aafactory.xyz/)
[![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/C2Rjy8Q2ER)

![AAFactory Screenshot](https://github.com/Reekomer/aafactory/blob/main/github_assets/napoleon_example.png?raw=true)


# IMPORTANT
- we are building a better UI for the project in here: https://github.com/orgs/AA-Factory/repositories
This repository is being deprecated.

## File Tree

```bash
├── LICENSE.md
├── README.md
├── aafactory
│   ├── assets
│   │   ├── avatar_images
│   │   │   └── ...png
│   │   ├── avatar_voice_recordings
│   │   │   └── ...wav
│   │   ├── demo
│   │   │   ├── avatar.jpg
│   │   │   ├── avatar.mp4
│   │   │   └── voice_recording.mp3
│   │   ├── generated_video
│   │   ├── generated_videos
│   │   │   └── ...mp4
│   │   ├── generated_voice
│   │   │   └── ...mp3
│   │   └── generated_voices
│   │       └── ...mp3
│   ├── databases
│   │   └── avatar_db.json
│   ├── src
│   │   ├── __init__.py
│   │   └── aafactory
│   │       ├── __init__.py
│   │       ├── act
│   │       │   └── interface.py
│   │       ├── avatar
│   │       │   └── interface.py
│   │       ├── chat
│   │       │   └── interface.py
│   │       ├── comfyui
│   │       │   └── video.py
│   │       ├── configuration.py
│   │       ├── create_gradio_ui.py
│   │       ├── database
│   │       │   └── manage_db.py
│   │       ├── fetcher
│   │       │   ├── environment_objects.py
│   │       │   └── fetching.py
│   │       ├── main.py
│   │       ├── prompts.py
│   │       ├── react
│   │       │   └── interface.py
│   │       ├── schemas.py
│   │       ├── settings.py
│   │       ├── style.py
│   │       └── utils
│   │           ├── interface.py
│   │           └── voice.py
│   ├── tests
│   └── workflows
│       ├── audio_image_to_video_with_sonic.json
│       └── text_to_speech_with_zonos.json
├── cloud_setup
│   ├── joyvasa
│   │   └── setup_joyvasa.sh
│   ├── pyproject.toml
│   ├── sonic
│   │   ├── install_sonic.sh
│   │   └── pyproject.toml
│   ├── uv.lock
│   └── zonos
│       └── pyproject.toml
├── github_assets
│   ├── hpi-logo-white.svg
│   └── napoleon_example.png
├── poetry.lock
├── pyproject.toml
└── file_tree.txt
```


## Tutorial:
- Youtube tutorial: https://www.youtube.com/watch?v=MGmBf7OsFJk
## Installation

Install the required packages by running the following commands:

```bash
pip install poetry
```

```bash
poetry install
```

### ComfyUI
- Use Video Helper Suite v1.5.0 (can be selected in ComfyManager)

## Run the application

If you use VSCode, you can run the application by clicking on the `Run and Debug` button and selecting `Python: Run and Debug` and then `Run Gradio UI`.

If you don't use VSCode, you can run the application by running the following command:

```bash
python aafactory/src/aafactory/create_gradio_ui.py
```

You will also need:
- ElevenLabs API key
- OpenAI API key
- ComfyUI server URL

For ComfyUI, the worflow is defined in the `workflows` folder. You need to make sure the nodes are installed. A more detailed guide will be available soon.

### Runpod Template for ComfyUI

- [Template](https://runpod.io/console/deploy?template=laidmkkjli&ref=uw67f0zc)


### Current Tech Stack:

- Gradio – Frontend

- ComfyUI – Backend

- OpenAI API – LLM

- ElevenLabs – TTS

- Flux – Text-to-Image (Avatar Generation)

- Sonic – Audio-Driven Video Generation


## More Examples

See our website for more examples: [AAFactory.xyz](https://aafactory.xyz/)


## Incoming Features

- [ ] Add support for Hugging Face models (Text to Speech and Text to Text)
- [x] Create documentation for ComfyUI cloud hosting
- [ ] Improve ComfyUI cloud hosting setup
- [x] Enable users to manage several avatars
- [ ] Enable users to easily share avatar's setup with others
- [ ] Add feature to let an avatar react to a Youtube video
- [ ] Add microphone button for direct chat with Avatar


## Partners

![HPI Logo](https://github.com/Reekomer/aafactory/blob/main/github_assets/hpi-logo-white.svg?raw=true)
