from fastapi import APIRouter,Request
from mongo import db
from cache import cache

auth=APIRouter()

@auth.post("")
async def verify(request: Request):
    data=await request.json()
    try:
        token=data["token"]
        print(token)
        if cache.exists(token):
            username=cache.hget(token,"username")
            print("username",username)
            return {"success":True,"username":username}
        else:
            print("user not found")
            return {"success":False}
    except:
        return {"success":False}