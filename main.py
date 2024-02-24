from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Set up template directory
templates = Jinja2Templates(directory="templates")

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("signup_form.html", {"request": request})


@app.post("/signup")
async def form_signup(name: str = Form(), email: str = Form(), phone: str = Form()):
    # Here you can process the data (e.g., save to database)
    print(f"Name: {name}, Email: {email}, Phone: {phone}")  # Example processing
    with open("signup.log", "a") as file:
        file.write(f"Name: {name}, Email: {email}, Phone: {phone} \n")
    return {"message": "Successfully signed up!"}