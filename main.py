from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers import user, authentication, forget_password, post, comment, like
import models
from database import engine

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(like.router)
app.include_router(forget_password.router)

models.Base.metadata.create_all(engine)


@app.get('/', tags=['Roots'])
def root():
    return {'message': 'the endpoint is created successfully'}

