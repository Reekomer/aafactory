import pytest
from aafactory.chat.interface import _load_avatar_infos_for_chat, CHAT_HISTORY
import aafactory.chat.interface as chat_interface

@pytest.mark.asyncio
async def test_send_request_to_llm(mocker):
    # Clear global state
    CHAT_HISTORY.clear()
    
    # Mock comfyui video generation
    mocker.patch("aafactory.chat.interface.send_request_to_generate_video", new_callable=mocker.AsyncMock, return_value="video_path.mp4")
    
    # Mock send_request_to_open_ai to also update CHAT_HISTORY
    def llm_side_effect(*args, **kwargs):
        CHAT_HISTORY.append(["Hello", "Hi there!"])
        return ("", [["Hello", "Hi there!"]], "video_path.mp4")

    mocker.patch(
        "aafactory.chat.interface.send_request_to_open_ai",
        new_callable=mocker.AsyncMock,
        side_effect=llm_side_effect
    )

    # Mock avatar info loader
    mocker.patch(
        "aafactory.chat.interface._load_avatar_infos_for_chat",
        return_value=(
            "Bot", "Friendly", "Knows stuff", "avatar_video.mp4",
            "elevenlabs", "voiceid", "path/to/rec", "transcript", "en", "avatar.png"
        )
    )

    avatar_info = _load_avatar_infos_for_chat()

    first_llm_answer = await chat_interface.send_request_to_open_ai(
        avatar_info[9], "Hello", avatar_info[0], avatar_info[1], avatar_info[2],
        avatar_info[4], avatar_info[5], avatar_info[6], avatar_info[7], avatar_info[8]
    )

    # Verify result
    assert first_llm_answer[0] == "" 
    assert first_llm_answer[1] == [["Hello", "Hi there!"]] # Chat history
    assert first_llm_answer[2] == "video_path.mp4"
    assert len(CHAT_HISTORY) == 1
    assert CHAT_HISTORY[0] == ["Hello", "Hi there!"]
