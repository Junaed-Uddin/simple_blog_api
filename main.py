from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers import user, authentication, forget_password, post
import models
from database import engine

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(forget_password.router)
app.include_router(post.router)

models.Base.metadata.create_all(engine)


@app.get('/', tags=['Roots'])
def root():
    return {'message': 'the endpoint is created successfully'}

