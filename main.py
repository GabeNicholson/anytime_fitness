from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import models

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