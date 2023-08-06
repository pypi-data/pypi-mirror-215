# Agent
import requests

class Agent:
    def __init__(self, api_key, agent_id):
        self.api_key = api_key
        self.agent_id = agent_id

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_agent_id(self, agent_id):
        self.agent_id = agent_id

    def completion(self, prompt):
        # Headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        # Endpoint
        url = 'https://playground.judini.ai/api/v1/agent/'+ self.agent_id
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        response = requests.post(url, json=data, headers=headers)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                raw_data += chunk.decode('utf-8')

        raw_data = raw_data.replace("data: ", '')
        raw_data = raw_data.replace("\n", '')
        raw_data = raw_data.replace("[DONE]", '')
        return raw_data