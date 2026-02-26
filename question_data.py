from sqlalchemy import text

from cache import cache
import sql_con as sql
from fastapi import APIRouter,Request

question_data_router=APIRouter()


@question_data_router.post("")
async def question_data(request: Request):
    data=await request.json()
    print(data)
    qID=data["qid"]
    print(qID)
    question=sql.session.execute(text("select * from questions where qID=:qID"),{"qID":qID}).first()._mapping
    test_case=sql.session.execute(text("select * from testcases where qID=:qID"),{"qID":qID}).first()._mapping
    question=dict(question)
    test_case=dict(test_case)
    question["test_in"]=test_case["test_in"]
    question["test_out"]=test_case["test_out"]
    question["tags"]=list(question["tags"].split(" "))
    print(question)
    return {"success":True,"question":question}

