import json
import pprint
from typing import List
from google import genai
import pydantic
import os
from dotenv import load_dotenv

from fastapi import APIRouter,Request
import sql_con as sql
from cache import cache

load_dotenv()
AI_router=APIRouter()

class AIResponse(pydantic.BaseModel):
    code:str
    explanation:str
    mistakes:str
    corrected_code:str
    corrections_made:List[str]

class AI_model:
    def __init__(self):
        print(os.environ.get("GEMINI_API_KEY"))
        self.client=genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


    def code_correction(self,code,question):
        res = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"You have to analyze this code: {code} and this question: {question}",
            config={
                "response_mime_type": "application/json",
                "response_json_schema": AIResponse.model_json_schema(),
            },
        )
        res=(res.parsed)
        pprint.pprint(res)
        return res




@AI_router.post("")
async def AI_assistance(request:Request):
    data=await request.json()
    print(data)
    code=data["code"]
    question=data["question"]
    res=AI_model().code_correction(code=code,question=question)
    print(res)
    return {"response":res,"success":True}