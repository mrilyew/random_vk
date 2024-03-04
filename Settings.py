class Settings:
    def get(self):
        return {
            'vkapi_token': '', # Set your vkapi token here
            'query': '', # space at end
            'count': 10,
            'timeout': 120, # seconds
            'timeout_between_images': 5 # seconds
        }
