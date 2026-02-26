from fastapi import APIRouter,Request
from sqlalchemy import text

import sql_con as sql
from cache import cache


question_router=APIRouter()


@question_router.post("")
async def get_question(request: Request):
    r=sql.session.execute(text("select * from questions")).all()
    r=[i._mapping for i in r]
    return {"questions":r,"success":True}

@question_router.get("/topics")
async def get_topics(request: Request):
    l=cache.lrange(f"topics",0,-1)
    print(l)
    return {"topics":l,"success":True}

@question_router.post("/search")
async def search(request: Request):
    data=await request.json()
    print(data)
    term=data["query"]
    print(term)
    topic=data["topic"]
    print(topic)
    l = sql.session.execute(
        text("""
            SELECT * FROM questions
            WHERE tags LIKE :topic
            AND title LIKE :term
        """),
        {
            "topic": f"%{topic}%",
            "term": f"%{term}%"
        }
    ).all()
    l=[i._mapping for i in l]
    print(l)
    return {"questions":l,"success":True}