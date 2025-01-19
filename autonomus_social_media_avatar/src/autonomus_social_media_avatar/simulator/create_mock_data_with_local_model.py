import ast
import json
from autonomus_social_media_avatar.fetcher.environment_objects import AvatarEnvironment
from autonomus_social_media_avatar.fetcher.simulator.pydantic_models_to_grammar import generate_gbnf_grammar_and_documentation
import pandas as pd
from pathlib import Path
from loguru import logger
from huggingface_hub import hf_hub_download
from tqdm import tqdm

from functools import lru_cache
from llama_cpp import (
    Llama,
    LlamaGrammar,
)

tqdm.pandas(desc="Labelling progress")

MODEL_NAME = "TinyLlama-1.1B-32k-Instruct.Q8_0.gguf"
ROOT_PATH = Path(__file__).parent.parent.parent.parent.parent.resolve()
MODEL_PATH = Path(ROOT_PATH, "./models", MODEL_NAME)
OUTPUT_PATH = Path(ROOT_PATH, "./datasets/mock_data.json")

PROMPT = """
Create a mock data for the avatar environment. 
The data should be in the format of AvatarEnvironment.

Example:
{
  "storyline_phase": "Stage 3: Pursuit of Happiness",
  "latest_tweets": [
    {
      "text": "Just completed a challenging task and feeling great about it!",
      "timestamp": "2023-10-01T12:00:00Z",
      "user": {
        "username": "HappyAvatar",
        "description": "Just a virtual being navigating through life.",
        "location": "Virtual World",
        "followers_count": 150,
        "following_count": 50,
        "tweet_count": 300
      }
    },
    {
      "text": "Feeling inspired and ready to take on new challenges today!",
      "timestamp": "2023-10-01T08:30:00Z",
      "user": {
        "username": "HappyAvatar",
        "description": "Just a virtual being navigating through life.",
        "location": "Virtual World",
        "followers_count": 150,
        "following_count": 50,
        "tweet_count": 300
      }
    }
  ],
  "latest_news": [
    {
      "title": "Exciting Events Happening in the Virtual World!",
      "description": "Join us for a fun-filled day of challenges and games.",
      "timestamp": "2023-10-01T09:00:00Z",
      "source": "Virtual News Network"
    },
    {
      "title": "New Skills Available for Avatars!",
      "description": "Check out the latest skills you can acquire to enhance your abilities.",
      "timestamp": "2023-09-30T15:00:00Z",
      "source": "Skill Development Hub"
    }
  ],
  "friends_list": [
    {
      "username": "CoolAvatar",
      "description": "Loves adventure and exploring new worlds.",
      "location": "Adventure Land",
      "followers_count": 200,
      "following_count": 60,
      "tweet_count": 150
    },
    {
      "username": "WiseAvatar",
      "description": "A thoughtful being who enjoys sharing knowledge.",
      "location": "Knowledge Base",
      "followers_count": 180,
      "following_count": 75,
      "tweet_count": 120
    }
  ],
  "enemy_list": [
    {
      "username": "EvilAvatar",
      "description": "Always plotting and scheming.",
      "location": "Dark Realm",
      "followers_count": 50,
      "following_count": 20,
      "tweet_count": 25
    }
  ],
  "avatar_latest_status": {
    "physiological": {
      "water": 0.5,
      "food": 0.5,
      "shelter": 0.2,
      "sleep": 0.02,
      "clothing": 0.2
    },
    "safety": {
      "personal_security": 0.2,
      "employment": 0.0,
      "health": 0.2,
      "property": 0.2
    },
    "love_belonging": {
      "friendship": 0.2,
      "intimacy": 0.2,
      "family": 0.1,
      "sense_of_connection": 0.0
    },
    "esteem": {
      "respect": 0.1,
      "self_esteem": 0.2,
      "status": 0.0,
      "recognition": 0.2,
      "strength": 0.0
    }
  },
  "avatar_latest_actions": [
    {
      "action": "Completed a new skill training session.",
      "timestamp": "2023-10-01T12:30:00Z"
    },
    {
      "action": "Joined a new friend in an adventure.",
      "timestamp": "2023-10-01T11:00:00Z"
    }
  ],
  "avatar_latest_thoughts": [
    {
      "thought": "I wonder what new things I can learn today.",
      "timestamp": "2023-10-01T10:15:00Z"
    },
    {
      "thought": "Feeling grateful for my friends and the experiences we share.",
      "timestamp": "2023-10-01T09:45:00Z"
    }
  ],
  "avatar_latest_mood": [
    { "mood": "Happy", "timestamp": "2023-10-01T12:00:00Z" },
    { "mood": "Motivated", "timestamp": "2023-10-01T08:00:00Z" }
  ],
  "avatar_latest_emotions": [
    { "emotion": "Excitement", "timestamp": "2023-10-01T12:00:00Z" },
    { "emotion": "Hopeful", "timestamp": "2023-10-01T08:00:00Z" }
  ],
  "avatar_latest_goals": [
    { "goal": "Acquire a new skill", "timestamp": "2023-10-01T11:15:00Z" },
    { "goal": "Make a new friend", "timestamp": "2023-10-01T09:30:00Z" }
  ],
  "avatar_latest_skills": [
    { "skill": "Advanced Navigation", "timestamp": "2023-10-01T12:30:00Z" },
    { "skill": "Conflict Resolution", "timestamp": "2023-10-01T11:00:00Z" }
  ],
  "avatar_latest_inventory": [
    { "item": "Magic Potion", "timestamp": "2023-10-01T12:00:00Z" },
    { "item": "Map of Adventures", "timestamp": "2023-09-30T16:00:00Z" }
  ],
  "avatar_latest_stress": [
    { "stress": 0.02, "timestamp": "2023-10-01T12:00:00Z" }
  ]
}
"""


def prepare_mock_data() -> None:
    """Creates a dataset of mock data."""
    model = _load_model()
    mock_data_df = _create_mock_data(model)
    with open(OUTPUT_PATH, "w") as file:
        json.dump(mock_data_df, file, indent=4)


@lru_cache(maxsize=None)
def _load_model() -> Llama:
    """Load Llama model"""
    if MODEL_PATH.exists():
        return Llama(
            model_path=str(MODEL_PATH),
            seed=32,
            n_gpu_layers=-1,
            n_batch=512,
            n_ctx=16000,
            logits_all=True,
        )
    hf_hub_download(
        repo_id="QuantFactory/Phi-3.5-mini-instruct-GGUF",
        filename=MODEL_NAME,
        local_dir=Path(ROOT_PATH, "models"),
    )
    return Llama(
        model_path=str(MODEL_PATH),
        seed=32,
        n_gpu_layers=0,
        n_batch=512,
        n_ctx=16000,
        logits_all=True,
    )


def _create_mock_data(model: Llama) -> pd.DataFrame:
    """Create mock data for the avatar environment."""
    grammar = _prepare_grammar()
    model_response = model(
        PROMPT,
        temperature=0.5,
        repeat_penalty=1.3,
        grammar=grammar,
        max_tokens=10000,
    )["choices"][0]["text"]
    if model_response.endswith("}"):
        return ast.literal_eval(model_response)
    try:
        return ast.literal_eval(model_response)
    except SyntaxError as exception:
        logger.warning(exception)
        logger.warning(model_response)
        return [{"model_response": model_response, "error": exception}]


def _prepare_grammar() -> LlamaGrammar:
    """Prepare grammar for the model."""
    tools = [AvatarEnvironment]
    gbnf_grammar, documentation = generate_gbnf_grammar_and_documentation(
        pydantic_model_list=tools, outer_object_name="function",
        outer_object_content="function_parameters", model_prefix="Function", fields_prefix="Parameters")
    return LlamaGrammar.from_string(gbnf_grammar)


if __name__ == "__main__":
    prepare_mock_data()
