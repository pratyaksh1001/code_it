from fastapi import APIRouter,Request
from mongo import db
import bcrypt
import jwt
from cache import cache
import sql_con as sql


login_router=APIRouter()

@login_router.post("/submit")
async def login(request: Request):
    data=await request.json()
    email=data["email"]
    password=data["password"]
    user=sql.login_user(email,password)
    if user:
        token=jwt.encode({"email":email,"password":password},"pratyaksh")
        cache.hset(token,mapping={"email":email,"username":user.username})
        cache.expire(token,3600)
        return {"token":token,"email":email,"username":user.username,"success":True}
    else:
        return {"error":"Wrong Credentials","success":False}
