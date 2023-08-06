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
        self.base_url = "https://app.twilix.io/api/v1/"
    
    def insert_objects(self, objects: list):
        url = self.base_url + "collection/bulk-insert"
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json", 
                "Authorization": "Bearer " + self.api_key
            },
            json={
                "collection": self.collection_name,
                "objects": objects
            }

        )
        print(response.content.decode())
        return response.json()
    
    def insert_pdf(self, url: str):
        api_url = self.base_url + "collection/insert-pdf"
        print(api_url)
        response = requests.post(
            api_url,
            headers={
                # "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key
            },
            json={
                "collection": self.collection_name,
                "url": url
            }
        )
        print(response.content.decode())
        return response.json()

    
    def generative_qa(self, user_input: str, answer_fields: list,
        conversation_id: str=None, limit: int=5):
        """Get an answer based on a question that you ask.
        """
        url =  self.base_url + "collection/generative-qa"
        print(url)
        data={
            "collection": self.collection_name,
            "userInput": user_input,
            "answerFields": answer_fields,
            # "limit": limit,
        }
        if conversation_id:
            data["conversationID"] = conversation_id
        print(data)
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key
            },
            json=data
        )
        print(response.content.decode())
        return response.json()
