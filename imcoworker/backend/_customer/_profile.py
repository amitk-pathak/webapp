import json
import os
from openai import OpenAI
from constants import OPENAPI_API_KEY

client = OpenAI(api_key=OPENAPI_API_KEY)

class CustomerProfile:
    _instance = None  

    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super(CustomerProfile, cls).__new__(cls)
    #         cls._instance._initialize(*args, **kwargs)
    #     return cls._instance
    
    def __init__(self, customer_input: str):
        self.customer_input = customer_input
        self.titles = None
        self.industry = None
        self.locations = None
        self.explanation = None
        self.confidence = None
        # self.read_local_file()
        self.extract_customer_profile(customer_input)
    
    def get_profile(self):
        
        return {
            "titles": self.titles,
            "industry": self.industry,
            "locations": self.locations,
            "explanation": self.explanation,
            "confidence": f"{self.confidence:.2%}" if self.confidence else None
        }

    def __str__(self):
        return json.dumps(self.get_profile(), indent=4)        

    def read_local_file(self):
        
        # Path to the JSON file in the parent directory
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
        # print("Base Directory:", base_dir)
        output_file = os.path.join(base_dir, "../customer_profile.json")  # Navigate one level up
        # print("Output File Path:", output_file)

        with open(output_file, "r", encoding="utf-8") as file:
            profile = json.load(file) 
            self.titles = [profile["role_detected"]]
            self.locations = [profile["location_detected"]]
            self.industry = profile["industry_detected"]
            self.explanation = profile["explanation"]
            self.confidence = profile["confidence"]

    def extract_customer_profile(self, text: str):
        
        print("Inside extract_customer_profile")

        response = client.chat.completions.create(
            model="gpt-4.1",
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "CustomerProfile",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "matches_target": { "type": "boolean" },

                            "role_detected": {
                                "type": "array",
                                "items": { "type": "string" },
                                "description": "List of roles the customer is searching for. Each item should contain no more than 2 words.",
                                "maxItems": 4
                            },

                            "industry_detected": {
                                "type": "string",
                                "description": "Industry keyword(s) with no more than 2 words."
                            },

                            "location_detected": {
                                "type": "array",
                                "items": { "type": "string" },
                                "description": "List of locations customer is looking client from. Each item should contain no more than 2 words.",
                            },

                            "confidence": { "type": "number" },
                            "explanation": { "type": "string" }
                        },
                        "required": ["matches_target", "role_detected", "industry_detected", "location_detected"]
                    }
                }
            },
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract structured insights from text. "
                        "Return role_detected as a list of keyword strings, each no longer than 2 words. "
                        "Return industry_detected as a string of no more than 2 words. "
                        "Extract and return the user's desired locations as a list of keyword strings, each no longer than 2 words. "
                        "Provide high-confidence structured output."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        # Convert the JSON string to a Python dictionary
        data = json.loads(response.choices[0].message.content)
        
        self.titles = data["role_detected"]
        self.locations = data["location_detected"]
        self.industry = data["industry_detected"]
        self.explanation = data.get("explanation")
        self.confidence = data.get("confidence")
        # return response.choices[0].message.content  # parsed JSON result
