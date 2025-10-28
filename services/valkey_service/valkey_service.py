import valkey
import json
class ValkeyClient():
    def __init__(self, valkey_url: str):
        self.valkey_client = valkey.from_url(valkey_url)
    
    def insert_video(self, key: str, data):
        """Insert video, auto-convert to JSON"""
        if isinstance(data, str):
            try:
                json.loads(data)
            except json.JSONDecodeError:
                data = json.dumps(eval(data))
        else:
            data = json.dumps(data)
        
        self.valkey_client.set(key, data)
    
    def get_all_videos(self):
        videos = []
        for key in self.valkey_client.scan_iter(match="video:*"):
            value = self.valkey_client.get(key)
            try:
                value = value.decode("utf-8")
                value = json.loads(value)
            except Exception:
                pass  
            videos.append({ "key": key.decode("utf-8"), "value": value })
        return videos

    def change_status(self, key: str, new_status: str):
        """
        Update the 'status' field of a video in Valkey.
        new_status can be 'IN PROGRESS' or 'COMPLETED'.
        """
        if new_status not in ["IN PROGRESS", "COMPLETED"]:
            raise ValueError("Status must be 'IN PROGRESS' or 'COMPLETED'")
        
        value = self.valkey_client.get(key)
        if not value:
            raise KeyError(f"No video found with key: {key}")
        
        try:
            value = value.decode("utf-8")
            data = json.loads(value)
        except Exception as e:
            raise ValueError(f"Invalid JSON stored at {key}: {e}")
        
        data["status"] = new_status
        self.valkey_client.set(key, json.dumps(data))
        print(f"🔄 Updated {key} → status = {new_status}")
        return data
