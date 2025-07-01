import pytest
from aafactory.database.manage_db import load_selected_avatar_infos

def test_load_avatar_success(mocker):
    """Test loading an avatar returns the correct information."""
    # Arrange - Create a fake avatar in the database
    fake_avatar = {
        "name": "TestAvatar",
        "personality": "Friendly helper",
        "background_knowledge": "Knows Python",
        "avatar_image_path": "Avatar.png",
        "voice_model": "elevenlabs",
        "voice_id": "voice123",
        "voice_recording_path": "voice.wav",
        "audio_transcript": "Hello!",
        "voice_language": "en"
    }
    
    # Mock the database to return our fake avatar
    mock_table = mocker.MagicMock()
    mock_table.get.return_value = fake_avatar
    mock_db = mocker.MagicMock()
    mock_db.table.return_value = mock_table
    mocker.patch("aafactory.database.manage_db.TinyDB", return_value=mock_db)
    mocker.patch("aafactory.database.manage_db.save_avatar_page_settings")
    
    # Act - Load the avatar
    result = load_selected_avatar_infos("TestAvatar")
    
    # Assert - Check we got the right avatar data back
    name, personality, knowledge, image, voice_model, voice_id, recording, transcript, language = result
    
    assert name == "TestAvatar"
    assert personality == "Friendly helper"
    assert knowledge == "Knows Python"
    assert voice_model == "elevenlabs"
    assert language == "en"