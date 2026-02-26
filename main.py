from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import AI
import contribute
import login
import auth
import question_data
import questions
import register
import run

app=FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(register.register_router,prefix="/register")
app.include_router(login.login_router,prefix="/login")
app.include_router(auth.auth,prefix="/auth")
app.include_router(contribute.contribution,prefix="/contribute")
app.include_router(questions.question_router,prefix="/questions")
app.include_router(question_data.question_data_router,prefix="/question_data")
app.include_router(run.run_router,prefix="/run_code")
app.include_router(AI.AI_router,prefix="/AI")
