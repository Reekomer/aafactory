<div align="center">

# AI Avatar Factory

** AI Avatar Factory is an interface for creating and managing AI avatars. **

<br>
[![Website](https://img.shields.io/badge/ComfyOrg-4285F4?style=flat)](https://aafactory.xyz/)
[![Discord](https://img.shields.io/badge/ComfyOrg-4285F4?style=flat)](https://discord.gg/C2Rjy8Q2ER)
</div>

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







