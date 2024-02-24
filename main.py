from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"hello": name}


@app.get("/", response_class=HTMLResponse)
async def get_form():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sign Up for the Gym</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                background-color: #f0f2f5;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
                height: 100vh;
            }
            .container {
                width: 100%;
                max-width: 400px; /* Adjust the width of the form */
                margin-top: 50px; /* Adjust the space between the title and the form */
            }
            form {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            h2 {
                color: #333;
                text-align: center;
                margin-bottom: 20px; /* Adjust space between title and form if needed */
            }
            label, input[type=text], input[type=email], input[type=tel], input[type=submit] {
                display: block; /* Make inputs take the full width */
                width: calc(100% - 20px);
                margin: 10px auto;
            }
            input[type=text], input[type=email], input[type=tel] {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            input[type=submit] {
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            input[type=submit]:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Sign Up Form</h2>
            <form action="/signup" method="post">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
                <label for="phone">Phone Number:</label>
                <input type="tel" id="phone" name="phone" required>
                <input type="submit" value="Submit">
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/signup")
async def form_signup(name: str = Form(), email: str = Form(), phone: str = Form()):
    # Here you can process the data (e.g., save to database)
    print(f"Name: {name}, Email: {email}, Phone: {phone}")  # Example processing
    with open("signup.log", "a") as file:
        file.write(f"Name: {name}, Email: {email}, Phone: {phone} \n")
    return {"message": "Successfully signed up!"}