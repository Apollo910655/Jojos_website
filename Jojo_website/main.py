from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI(title="Valentine's Proposal ❤️")

# Mount static files directory for CSS, JS, and images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

class DateRequest(BaseModel):
    selected_date: str

class DateChoice(BaseModel):
    date: str
    choice: int

# Your email configuration
EMAIL_ADDRESS = "cristianrazo910@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "qoxl yhzr usvt edqz"     # Replace with your app password
RECIPIENT_EMAIL = "crazo@ucsb.edu" # Replace with your email

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "name": "Jojo"}
    )

@app.get("/calendar", response_class=HTMLResponse)
async def calendar(request: Request):
    return templates.TemplateResponse(
        "calendar.html",
        {"request": request}
    )

@app.post("/save-date")
async def save_date(date_request: DateRequest):
    # For now, just return success
    return {"message": "Date saved successfully"}

@app.get("/date-choices", response_class=HTMLResponse)
async def date_choices(request: Request, date: str):
    return templates.TemplateResponse(
        "dates.html",  # Make sure this file exists in templates folder
        {"request": request, "selected_date": date}
    )

@app.post("/save-date-choice")
async def save_date_choice(choice: DateChoice):
    # For now, just return success
    return {"message": "Choice saved successfully"}

@app.get("/confirmation", response_class=HTMLResponse)
async def confirmation(request: Request, date: str, choice: int):
    activities = {
        1: "LA Tokyo and Art night ⛩️🖼️",
        2: "Knotts Berry Farm 🎡",
        3: "A home cooked meal + pjs and a movie 🎦"
    }
    return templates.TemplateResponse(
        "confirmation.html",
        {
            "request": request, 
            "selected_date": date,
            "activity_name": activities[choice]
        }
    )

@app.post("/confirm-choice")
async def confirm_choice(choice: DateChoice):
    activities = {
        1: "LA Tokyo and Art night ⛩️🖼️",
        2: "Knotts Berry Farm 🎡",
        3: "A home cooked meal + pjs and a movie 🎦"
    }
    
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = "Valentine's Date Confirmed! ❤️"
    
    body = f"""
    Wonderful news! Jojo has confirmed her Valentine's date choice:
    
    Date: {choice.date}
    Activity: {activities[choice.choice]}
    
    Time to start planning! 🌹
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return {"message": "Confirmation sent successfully"}
    except Exception as e:
        print(f"Error sending email: {e}")
        return {"message": "Error sending email", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)