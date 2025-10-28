import valkey

class ValkeyClient():
    def __init__(self, valkey_url: str):
        self.valkey_client = valkey.from_url(valkey_url)
    
    def insert_video(self):
        self.valkey_client.set('key', 'hello world')
        key = self.valkey_client.get('key').decode('utf-8')
        print('\nThe value of key is:', key)
        