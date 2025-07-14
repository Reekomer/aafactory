# Basic Initialization Test
import pytest
from aafactory.chat.interface import create_chat_interface#

def test_chat_interface_initialization():
    #Test that ChatInterface can be initialized."""
    chat = create_chat_interface()
    assert chat is not None