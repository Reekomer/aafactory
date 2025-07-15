import pytest
import aafactory.chat.interface as chat_interface

@pytest.mark.asyncio
async def test_send_request_to_llm(mocker):
    # Clear chat history before test
    chat_interface.CHAT_HISTORY.clear()
        # Mock LLM and audio/video functions
    mocker.patch("aafactory.chat.interface.send_request_to_open_ai", return_value="Hi, user!")
    mocker.patch("aafactory.chat.interface.send_request_to_elevenlabs", return_value="mock_audio_path.mp3")
    mocker.patch("aafactory.chat.interface.send_request_to_generate_video", return_value="mock_video_path.mp4")

    mock_avatar_info = chat_interface._load_avatar_infos_for_chat()

    # Call the function with test data
    first_llm_answer = await chat_interface.send_request_to_llm(
        mock_avatar_info[9], "Hello", mock_avatar_info[0], mock_avatar_info[1], mock_avatar_info[2],
        mock_avatar_info[4], mock_avatar_info[5], mock_avatar_info[6], mock_avatar_info[7], mock_avatar_info[8]
    )

    # Verify result
    assert first_llm_answer[0] == "" 
    assert first_llm_answer[1] == [["Hello", "Hi, user!"]] # Chat history
    assert first_llm_answer[2] == "mock_video_path.mp4"
    assert len(chat_interface.CHAT_HISTORY) == 1
    assert chat_interface.CHAT_HISTORY[0] == ["Hello", "Hi, user!"]

@pytest.mark.asyncio
async def test_chat_history_clears_on_avatar_change(mocker):
    chat_interface.CHAT_HISTORY.clear()
    chat_interface.CURRENT_AVATAR = None  # Reset avatar tracker

    mocker.patch("aafactory.chat.interface.send_request_to_open_ai", return_value="Hello, user!")
    mocker.patch("aafactory.chat.interface.send_request_to_elevenlabs", return_value="mock_audio_path.mp3")
    mocker.patch("aafactory.chat.interface.send_request_to_generate_video", return_value="mock_video_path.mp4")

    # First message with Avatar A
    await chat_interface.send_request_to_llm(
        "avatarA.png", "Hi Avatar A!", "AvatarA", "Friendly", "Knows stuff", 
        "elevenlabs", "voiceidA", "path/to/recA", "transcriptA", "en"
    )
    
    assert chat_interface.CHAT_HISTORY == [
        ["Hi Avatar A!", "Hello, user!"],
    ]
    
    # Second message with Avatar B
    await chat_interface.send_request_to_llm(
        "avatarB.png", "Hello Avatar B!", "AvatarB", "Serious", "Knows more stuff", 
        "elevenlabs", "voiceidB", "path/to/recB", "transcriptB", "en"
    )
    assert chat_interface.CHAT_HISTORY == [
        ["Hello Avatar B!", "Hello, user!"]
    ]
