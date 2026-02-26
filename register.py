import json

import jwt
from fastapi import APIRouter,Request,Form
from fastapi.templating import Jinja2Templates



from models import User
from mongo import db
from cache import cache
import bcrypt
import sql_con as sql

register_router = APIRouter()
jinja = Jinja2Templates(directory="templates")


@register_router.post("/submit")
async def register_submit(request: Request):
    data=await request.json()
    username = data["username"]
    password = data["password"]
    email = data["email"]
    status=sql.create_user(username=username,email=email,password=password)
    if status:
        return {"error":"User Already Exists!","success": False}
    else:
        return {"success":True}
