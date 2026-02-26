import pprint

from fastapi import APIRouter,Request
import sql_con as sql
from cache import cache
import bcrypt

contribution=APIRouter()

@contribution.post("/question")
async def question(request: Request):
    data=await request.json()
    print(data)
    data["success"]=True
    data=dict(data)
    d={}
    i=cache.get("curr_qid")
    d["question"]=data["question"]
    d["qID"]=int(i)
    d["likes"]=0
    d["dislikes"]=0
    d["email"]=cache.hget(data["token"],"email")
    d["title"]=data["title"]
    d["tags"]=data["tags"]
    t=""
    for j in data["tags"]:
        cache.rpush("topics",j)
        t=t+j+" "
    print(t)
    d["tags"]=t
    print(d)
    question=sql.Question(**d)
    print(question)
    sql.add_question(question)


    t={}
    t["test_in"]=data["test_in"]
    t["test_out"]=data["test_out"]
    t["email"]=cache.hget(data["token"],"email")
    t["likes"]=0
    t["dislikes"]=0
    t["qID"]=int(i)
    t["tID"]=hash(t["test_in"])
    print(t["tID"])

    test_case=sql.Testcase(**t)
    sql.session.add(test_case)
    cache.set("curr_qid", (int(i) + 1))
    sql.session.commit()
    return data