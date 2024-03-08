from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import models
import pydantic_models
import traceback
from starlette.middleware.sessions import SessionMiddleware
import uuid
import pytz
from datetime import datetime

def get_or_create_session_id(request: Request):
    # Check if the session already has a session_id set
    if "session_id" not in request.session:
        # Generate a new session_id and save it to the session
        request.session["session_id"] = str(uuid.uuid4())
    return request.session["session_id"]


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

@app.on_event("startup")
async def startup():
    await models.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await models.database.disconnect()


# Set up template directory
templates = Jinja2Templates(directory="templates")

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    session_id = get_or_create_session_id(request)
    referer = request.headers.get("referer")
    return templates.TemplateResponse("signup_form.html", {"request": request, "sessionId": session_id, "referer": referer})


@app.get("/success", response_class=HTMLResponse)
async def signup_success(request: Request):
    return templates.TemplateResponse("success_page.html", {"request": request})


@app.post("/signup")
async def form_signup(request: Request, name: str = Form(...), email: str = Form(...), phone: str = Form(...), referer: str = Form(...)):
    session_id = get_or_create_session_id(request)
    ip_address = request.client.host
    query = models.User.__table__.insert().values(name=name,
                                                  email=email,
                                                  phone=phone,
                                                  session_id=session_id,
                                                  referer=referer,
                                                  ip_address=ip_address,
                                                  created_at_v2=datetime.now(pytz.utc),
                                                  )
    last_record_id = await models.database.execute(query)
    # Redirect to the success page after processing
    return RedirectResponse(url="/success", status_code=303)


ACTION_MAPPING = {
    "schedule_tour_clicked": 1,
    "follow_instagram_clicked": 2,
    "google_maps_clicked": 3,
}

@app.post("/track-click")
async def track_click(request: Request, event: pydantic_models.ClickEvent):
    session_id = get_or_create_session_id(request)
    ip_address = request.client.host
    action_int = ACTION_MAPPING.get(event.action, 0)
    try:
        query = models.ClickEvent.__table__.insert().values(
            action=action_int,
            session_id=session_id,
            ip_address=ip_address,
            timestamp_v2=datetime.now(pytz.utc),
        )
        last_record_id = await models.database.execute(query)
        return {"status": "success", "record_id": last_record_id}
    except Exception as e:
        traceback.print_exc()  # Print the traceback to help debug
        print(f"Error inserting click event: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")