from fastapi import APIRouter,Request
from sqlalchemy import text
import multiprocessing as mp
import sql_con as sql
from cache import cache
import subprocess
import time

run_router=APIRouter()


def check_python(inp, out):
    res = subprocess.run(
        ["python", "user.py"],
        input=inp,
        capture_output=True,
        text=True
    ).stdout.strip()
    print("output is")
    print(res)
    return res == out

def check_bun(inp,out):
    res = subprocess.run(
        ["bun", "user.js"],
        input=inp,
        capture_output=True,
        text=True
    ).stdout.strip()
    print("output is")
    print(res)
    return res == out


@run_router.post("")
async def run_code_python(request: Request):
    data=await request.json()
    language=data["language"]
    qID=data["qid"]
    token=data["token"]
    email=cache.hget(token,"email")
    print(email)
    print(language)
    print(qID)
    code=data["code"]
    print(code)
    with open("user.py","w") as f:
        f.write(code)
    testcases=sql.session.execute(text("select * from testcases where qID=:qID"),{"qID":qID}).all()
    inputs=[i[1] for i in testcases]
    outputs=[i[2] for i in testcases]
    print(testcases)
    res=0
    n=len(inputs)
    r=0
    for i in range(n):
        if check_python(inputs[i], outputs[i]):
            r+=1
        else:
            return {"output": f"test cases passed are - {r}/{n}", "success": False}
    print(r)
    return {"output": f"test cases passed are - {r}/{n}","success": True}

@run_router.post("/js")
async def run_code_js(request: Request):
    data=await request.json()
    language=data["language"]
    qID=data["qID"]
    token=data["token"]
    email=cache.hget(token,"email")
    code=data["code"]
    if language=="javascript":
        with open("user.js","w") as f:
            f.write(code)
        testcases=sql.session.execute(text("select * from testcases where qID=:qID"),{"qID":qID}).all()
        inputs = [i[1] for i in testcases]
        outputs = [i[2] for i in testcases]
        print(testcases)
        n=len(inputs)
        r=0
        for i in range(n):
            if check_bun(inputs[i], outputs[i]):
                r+=1
            else:
                return {"output": f"test cases passed are - {r}/{n}", "success": False}
        return {"output": f"test cases passed are - {r}/{n}","success": True}
    else:
        return {"output": f"An unexpected error occurred","success": False}
