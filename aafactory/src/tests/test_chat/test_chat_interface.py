# Basic Initialization Test
import pytest
from chat.interface import create_chat_interface
from tests.test_configuration import TEST_AVATAR_IMAGE_PATH
from PIL import Image


def test_chat_interface_initialization():
    #Test that ChatInterface can be initialized."""
    chat = create_chat_interface()
    assert chat is not None
