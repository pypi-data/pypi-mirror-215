"""The API behind BlitzChain
"""
import requests

class Client:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def Collection(self, collection_name: str):
        return Collection(api_key=self.api_key, collection_name=collection_name)

class Collection:
    def __init__(self, api_key: str, collection_name: str):
        self.collection_name = collection_name
        self.api_key = api_key
        self.base_url = "https://app.twilix.io/"

    def insert_objects(self, objects: list):
        response = requests.post(
            self.base_url + "api/v1/collection/insert_objects",
            headers={
                "Content-Type": "application/json", 
                "Authorization": "Bearer " + self.api_key
            },
            json={
                "collection_name": self.collection_name,
                "objects": objects
            }

        )
        return response.json()
    
    def generative_qa(self, user_input: str, fields: list,
        conversation_id: str, limit: int=5):
        """Get an answer based on a question that you ask.
        """
        response = requests.post(
            self.base_url + "api/v1/collection/generative_qa",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key
            },
            json={
                "collection_name": self.collection_name,
                "userInput": user_input,
                "fields": fields,
                "conversationID": conversation_id,
                "limit": limit,
            }
        )
        return response.json()
