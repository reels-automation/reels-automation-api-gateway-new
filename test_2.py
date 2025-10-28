from settings import VALKEY_URL
from services.valkey_service.valkey_service import ValkeyClient

valkey_client = ValkeyClient(VALKEY_URL)
data = {
    "tema": "Explica la programacion orientada a dops",
    "usuario": 1,
    "idioma": "es",
    "personaje": "Homero Simpson",
    "script": "",
    "audio_item": [
        {
            "tts_audio_name": "",
            "tts_audio_directory": "",
            "file_getter": "",
            "pitch": 0,
            "tts_voice": "es-ES-XimenaNeural",
            "tts_rate": 0,
            "pth_voice": "HOMERO SIMPSON LATINO",
        }
    ],
    "subtitle_item": [
        {"subtitles_name": "", "file_getter": "", "subtitles_directory": ""}
    ],
    "author": "Mi amigo el galofa",
    "gameplay_name": "",
    "background_music": [
        {"audio_name": "", "file_getter": "", "start_time": 0, "duration": 100}
    ],
    "images": [
        {
            "image_name": "homero1.png",
            "image_modifier": "rotate",
            "file_getter": "",
            "image_directory": "local",
            "timestamp": 0,
            "duration": 10,
        }
    ],
    "random_images": False,
    "random_amount_images": 0,
    "gpt_model": "deepseek3.2:3b",
}

key = "video:porky"
valkey_client.insert_video(key,str(data))

valkey_client.change_status(key, "IN PROGRESS")
    
print(valkey_client.get_all_videos())