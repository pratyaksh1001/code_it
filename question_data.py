from fastapi import APIRouter, Request
from sqlalchemy import text

import sql_con as sql
from cache import cache
from run import check_python

question_data_router = APIRouter()


@question_data_router.post("")
async def question_data(request: Request):
    data = await request.json()
    print(data)
    qID = data["qid"]
    print(qID)
    question = (
        sql.session.execute(
            text("select * from questions where qID=:qID"), {"qID": qID}
        )
        .first()
        ._mapping
    )
    test_case = (
        sql.session.execute(
            text("select * from testcases where qID=:qID"), {"qID": qID}
        )
        .first()
        ._mapping
    )
    question = dict(question)
    test_case = dict(test_case)
    question["test_in"] = test_case["test_in"]
    question["test_out"] = test_case["test_out"]
    question["tags"] = list(question["tags"].split(" "))

    question["tags"].pop()
    print(question)
    return {"success": True, "question": question}


@question_data_router.post("/testcase")
async def tcase(request: Request):
    data = await request.json()
    print(data)
    qID = data["qid"]
    test_in = data["inp"]
    test_out = data["out"]
    token = data["token"]
    email = cache.hget(token, "email")

    tc = sql.Testcase(
        email=email, test_in=test_in, test_out=test_out, qID=qID, tID=hash(test_in)
    )
    sql.session.add(tc)
    sql.session.commit()
    return {"success": True}
