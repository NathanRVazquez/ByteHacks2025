import os
import datetime
from fastapi import FastAPI, Request, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from typing import List
import recommender   # 👈 import your recommender.py module


from pydantic_extra_types.pendulum_dt import DateTime

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from typing import Annotated


from supabase import create_client, Client

load_dotenv()  # Load .env at the top

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# setup db engine
# models.Base.metadata.create_all(bind=engine)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# create DB connection 
def get_db():
    db=SessionLocal()
    try: 
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# create models for input
class UserBase(BaseModel):
    created_at: DateTime
    email: str
    password: str
    # broad_categories: list[str]
    # specific_categories: list[str]

class SurveyQuestionaireBase(BaseModel):
    user_id:int
    comedy_and_performance: str
    community_and_culture: str
    food_and_drink: str
    nightlife_and_parties:str
    stem:str
    home_and_lifestyle:str
    charity_and_social_causes:str
    business:str
    music:str
    online:str

class MeetingInformation(BaseModel):
    summary:str
    description:str
    startDateTime:DateTime
    endDateTime:DateTime
    timeZone: str = "America/New_York"

class LoginInformation(BaseModel):
    email:str
    password:str


# Environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://127.0.0.1:8000/auth/callback")
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Temporary in-memory credentials
user_creds = None

# --- Pydantic model for POST /add-event ---
class EventData(BaseModel):
    og_title: str
    og_description: str = None
    event_start_time: str
    event_end_time: str
    event_location_latitude: str = None
    event_location_longitude: str = None

# --- Helper to get Google Calendar service ---
def get_calendar_service():
    global user_creds
    if not user_creds or not user_creds.valid:
        return None
    return build("calendar", "v3", credentials=user_creds)

# Register route takes JSON information and saves it to the DB. Uses UserBase to validate items are the right type
@app.post("/register")
async def register_user(user: UserBase, db: db_dependency):
    # db_new_user = models.Users(email = user.email, password = user.password, created_at = user.created_at)
    # db.add(db_new_user)
    # db.commit()
    # db.refresh(db_new_user)
    # db.commit()
    response = supabase.auth.sign_up(
        {"email": user.email,
        "password": user.password,
        "created_at":user.created_at
        })
    # return response.aud
    return response.user.aud


# --- Step 1: Login ---
@app.get("/google-login")
def google_login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")
    return RedirectResponse(auth_url)

@app.post("/login")
def login_email_password(user_creds: LoginInformation):
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": user_creds.email,
            "password": user_creds.password,
            })
        return {
            "acccess_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "expires_in": response.session.expires_in,
            "token_type":"bearer",
            "user":{
                "id":response.user.id,
                "email":response.user.email,
                "role":response.user.role
            }
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# --- Step 2: OAuth callback ---
@app.get("/auth/callback")
def auth_callback(request: Request):
    global user_creds
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="❌ No code found in query")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    flow.fetch_token(code=code)
    user_creds = flow.credentials
    return HTMLResponse("✅ Auth success! Now try /events or /add-event")


# --- Step 3: List events ---
# @app.get("/events")
# def list_events():
#     service = get_calendar_service()
#     if not service:
#         raise HTTPException(status_code=401, detail="❌ Not authenticated. Go to /login first.")
#     now = datetime.datetime.utcnow().isoformat() + "Z"
#     events_result = service.events().list(
#         calendarId="primary",
#         timeMin=now,
#         maxResults=10,
#         singleEvents=True,
#         orderBy="startTime",
#     ).execute()
#     return JSONResponse(events_result.get("items", []))

# --- Step 4: Add event (POST) ---
@app.post("/add-event")
def add_event_post(event: EventData):
    service = get_calendar_service()
    if not service:
        raise HTTPException(status_code=401, detail="❌ Not authenticated. Go to /login first.")

    start = datetime.datetime.fromisoformat(event.event_start_time)
    end = datetime.datetime.fromisoformat(event.event_end_time)

    # Free/busy check
    fb = service.freebusy().query(
        body={"timeMin": start.isoformat(), "timeMax": end.isoformat(), "items": [{"id": "primary"}]}
    ).execute()
    if fb["calendars"]["primary"].get("busy"):
        raise HTTPException(status_code=400, detail="❌ Time slot is busy")

    location = None
    if event.event_location_latitude and event.event_location_longitude:
        location = f"{event.event_location_latitude},{event.event_location_longitude}"

    new_event = {
        "summary": event.og_title,
        "description": event.og_description or "",
        "start": {"dateTime": start.isoformat(), "timeZone": "America/New_York"},
        "end": {"dateTime": end.isoformat(), "timeZone": "America/New_York"},
        "location": location,
    }
    created = service.events().insert(calendarId="primary", body=new_event).execute()
    return HTMLResponse(f'✅ Event created: <a href="{created.get("htmlLink")}" target="_blank">View in Calendar</a>')

# --- Step 4b: Add event (GET with query params) ---
@app.get("/add-event")
def add_event_get(
    summary: str = Query(...),
    startDateTime: str = Query(...),
    endDateTime: str = Query(...),
    description: str = Query(None),
    timeZone: str = Query("America/New_York"),
):
    service = get_calendar_service()
    if not service:
        raise HTTPException(status_code=401, detail="❌ Not authenticated. Go to /login first.")

    start = datetime.datetime.fromisoformat(startDateTime)
    end = datetime.datetime.fromisoformat(endDateTime)

    fb = service.freebusy().query(
        body={"timeMin": start.isoformat(), "timeMax": end.isoformat(), "items": [{"id": "primary"}]}
    ).execute()
    if fb["calendars"]["primary"].get("busy"):
        raise HTTPException(status_code=400, detail="❌ Time slot is busy")

    new_event = {
        "summary": summary,
        "description": description or "",
        "start": {"dateTime": start.isoformat(), "timeZone": timeZone},
        "end": {"dateTime": end.isoformat(), "timeZone": timeZone},
    }
    created = service.events().insert(calendarId="primary", body=new_event).execute()
    return HTMLResponse(f'✅ Event created: <a href="{created.get("htmlLink")}" target="_blank">View in Calendar</a>')

@app.get("/event")
def get_event(eventId: str = Query(None, description="Event ID to fetch")):
    print(eventId)
    if eventId is not None:
        try:
            event_id_int = int(eventId)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="event_id must be an integer")
        result = supabase.table("events").select("*").eq("event_id", event_id_int).single().execute()
        return result.data
    else:
        events = supabase.table("events").select("*").execute()
        return events.data

@app.get("/recommendations/tags")
def get_recommendations_by_tags(
    tags: List[str] = Query(..., description="List of user tags"),
    top_k: int = Query(10, description="Number of recommendations")
):
    results = recommender.recommend_tags(tags)
    return results[:top_k]

@app.get("/recommendations/description")
def get_recommendations_by_description(
    query: str = Query(..., description="Event description to search"),
    top_k: int = Query(3, description="Number of recommendations")
):
    results = recommender.recommend_description(query)
    return results[:top_k]



# @app.post("/survey")
# def post_survey(user_survey: SurveyQuestionaireBase):
#     # db_new_survey = models
#     return user_survey

# @app.get("/login")
# def login():
#     return 

# @app.get("/")
# def dashboard():
#     return 

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)