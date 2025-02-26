<div align="center">

# AI Avatar Factory

** AI Avatar Factory is an interface for creating and managing AI avatars. **


<br>
[website-shield]: https://img.shields.io/badge/ComfyOrg-4285F4?style=flat
[website-url]: https://aafactory.xyz/
<!-- Workaround to display total user from https://github.com/badges/shields/issues/4500#issuecomment-2060079995 -->
[discord-shield]: https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdiscord.com%2Fapi%2Finvites%2Fcomfyorg%3Fwith_counts%3Dtrue&query=%24.approximate_member_count&logo=discord&logoColor=white&label=Discord&color=green&suffix=%20total
[discord-url]: https://discord.gg/C2Rjy8Q2ER

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







