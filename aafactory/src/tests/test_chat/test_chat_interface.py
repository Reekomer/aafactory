# Basic Initialization Test
import pytest
from aafactory.chat.interface import create_chat_interface
from aafactory.tests.test_configuration import TEST_AVATAR_IMAGE_PATH
from PIL import Image


def test_chat_interface_initialization():
    #Test that ChatInterface can be initialized."""
    chat = create_chat_interface()
    assert chat is not None

def test_chat_interface_avatar_loading():
    # Test that the avatar can be loaded from the database
    chat = create_chat_interface()
    assert chat.avatar is not None

def test_chat_interface_avatar_image_loading():
    # Test that the avatar image can be loaded from the database
    chat = create_chat_interface()
    assert chat.avatar_image is not None
