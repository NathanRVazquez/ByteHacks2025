from fastapi import FastAPI, HTTPException, Depends
from typing import Union, List, Annotated
from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime

# The three libraries below are used to create a model of the database, create the connection to the database
# and import the SQL alchemy DB
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

# all packages below are used for Middleware & API responses
# JSON package to parse the JSON response recieved by the server
import json 
from starlette.config import Config
from starlette.requests import Request

# all libraries below enable oauth
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError


class UserBase(BaseModel):
    created_at: DateTime
    email: str
    password: str
    broad_categories: list[str]
    specific_categories: list[str]

class SurveyQuestionaireBase(BaseModel):
    name:str
    user_id:str
    favorite_music_genres: str
    favorite_cuisine: str
    which_art_forms_do_you_need: str
    typical_ticket_budget_per_event:str
    preferred_event_typep:str
    hobbies:str
    location:str
    travel_distance:str

class Hobby(BaseModel):
    title:str


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(SessionMiddleware, secret_key="!secret")

# create DB connection 
def get_db():
    db=SessionLocal()
    try: 
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

config = Config('.env')
oauth = OAuth(config)

GOOGLE_CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=GOOGLE_CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# root will determine if a user session has been saved, if not it shows a link to to the login route
@app.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/google-login">google-login</a>')


# Register route takes JSON information and saves it to the DB. Uses UserBase to validate items are the right type
@app.post("/register")
async def register_user(user: UserBase, db: db_dependency):
    db_new_user = models.Users(email = user.email, password = user.password, created_at = user.created_at)
    db.add(db_new_user)
    db.commit()
    db.refresh(db_new_user)
    db.commit()


# function below defines the process for logging into google
@app.get('/google-login')
async def login(request: Request):
    redirect_uri = request.url_for('google_auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


# This route receives a token from Google verifying access to app, then redirects user to root 
@app.get('/google-auth')
async def google_auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)  # Fixed: use google for Google auth
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')

@app.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')



