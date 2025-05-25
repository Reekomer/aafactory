import pytest
from aafactory.chat.interface import _load_avatar_infos_for_chat, send_request_to_llm, CHAT_HISTORY

@pytest.mark.asyncio
async def test_chat_with_avatar_mock(mocker):
    # Clear global state
    CHAT_HISTORY.clear()
    
    # Mock the common dependencies (open ai, comfyui)
    mocker.patch("aafactory.chat.interface.send_request_to_open_ai", new_callable=mocker.AsyncMock, return_value="Hi there!")
    mocker.patch("aafactory.chat.interface.send_request_to_generate_video", new_callable=mocker.AsyncMock, return_value="video_path.mp4")
    
    # Mock avatar info loader
    mocker.patch(
        "aafactory.chat.interface._load_avatar_infos_for_chat",
        return_value=(
            "Bot", "Friendly", "Knows stuff", "avatar_video.mp4",
            "elevenlabs", "voiceid", "path/to/rec", "transcript", "en", "avatar.png"
        )
    )

    # Print initial state
    print(f"Initial CHAT_HISTORY: {CHAT_HISTORY}")

    avatar_info = _load_avatar_infos_for_chat()

    # Test with elevenlabs
    mocker.patch("aafactory.chat.interface.send_request_to_elevenlabs", new_callable=mocker.AsyncMock, return_value="audio_path.wav")

    result1 = await send_request_to_llm(
        avatar_info[9], "Hello", avatar_info[0], avatar_info[1], avatar_info[2],
        avatar_info[4], avatar_info[5], avatar_info[6], avatar_info[7], avatar_info[8]
    )
    
    # Print states after the call
    print("RESULT_11labs:", result1)
    print("CHAT_HISTORY_11labs:", CHAT_HISTORY)

    # Verify elevenlabs result
    assert result1[0] == ""
    assert len(result1[1]) == 1
    assert result1[1][0][0] == "Hello"
    assert result1[1][0][1] == "Hi there!"
    assert result1[2] == "video_path.mp4"
    assert len(CHAT_HISTORY) == 1
    assert CHAT_HISTORY[0] == ["Hello", "Hi there!"]

# Clear history for next test with zonos
    CHAT_HISTORY.clear()
    
    # Test with zonos
    # Patch dependencies for zonos BEFORE calling send_request_to_llm
    mocker.patch("aafactory.chat.interface.send_request_to_generate_video", new_callable=mocker.AsyncMock, return_value="video_path.mp4")
    mocker.patch("aafactory.chat.interface.send_request_to_zonos", new_callable=mocker.AsyncMock, return_value="zonos_audio.wav")

    result2 = await send_request_to_llm(
        avatar_info[9], "Hello", avatar_info[0], avatar_info[1], avatar_info[2],
        "zonos", avatar_info[5], avatar_info[6], avatar_info[7], avatar_info[8]
    )
    
    # Print states after the call
    print("RESULT_Zonos:", result2)
    print("CHAT_HISTORY_Zonos:", CHAT_HISTORY)

    # Verify zonos result
    assert result2[0] == ""
    assert len(result2[1]) == 1
    assert result2[1][0][0] == "Hello"
    assert result2[1][0][1] == "Hi there!"
    assert result2[2] == "video_path.mp4"

