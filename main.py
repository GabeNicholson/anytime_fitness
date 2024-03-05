from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import models
import pydantic_models
import traceback

app = FastAPI()


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
    return templates.TemplateResponse("signup_form.html", {"request": request})


@app.get("/success", response_class=HTMLResponse)
async def signup_success(request: Request):
    return templates.TemplateResponse("success_page.html", {"request": request})


@app.post("/signup")
async def form_signup(request: Request, name: str = Form(...), email: str = Form(...), phone: str = Form(...)):
    query = models.User.__table__.insert().values(name=name, email=email, phone=phone)
    last_record_id = await models.database.execute(query)
    # Redirect to the success page after processing
    return RedirectResponse(url="/success", status_code=303)


action_mapping = {
    "schedule_tour_clicked": 1,
    # Add more mappings as needed
}

@app.post("/track-click")
async def track_click(event: pydantic_models.ClickEvent):
    action_int = action_mapping.get(event.action, 0)
    naive_timestamp = event.timestamp.replace(tzinfo=None)
    try:
        query = models.ClickEvent.__table__.insert().values(
            action=action_int,
            timestamp=naive_timestamp
        )
        last_record_id = await models.database.execute(query)
        return {"status": "success", "record_id": last_record_id}
    except Exception as e:
        # Log the exception to console or file
        traceback.print_exc()  # Print the traceback to help debug
        print(f"Error inserting click event: {e}")
        # Optionally, return an error response
        raise HTTPException(status_code=500, detail="Internal server error")