from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.flow import process_input
from fastapi.middleware.cors import CORSMiddleware
# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Allow all origins, or specify specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Define the data model for request input
class InputData(BaseModel):
    role: str
    batch: str
    location: str
    desired_salary: int
    user_email: str
    app_password: str
    email_content: str

@app.get("/")
async def api_check():
    return "API runned successfully"

# Route to handle input data
@app.post("/run_script")
async def run_script(data: InputData):
    print("API called!")
    role = data.role
    batch = data.batch
    location = data.location
    desired_salary = data.desired_salary
    user_email = data.user_email
    app_password = data.app_password
    email_content = data.email_content

    try:
        #ex:- process_input(role: str, batch:str, location:str, desired_salary:int, user_email: str)
        # process_input("Software Engineer", "2025", "", 12, "sarthakrangari788@gmail.com")
        output = process_input(role, batch, location, desired_salary, user_email, app_password, email_content)
        return {"result": output}
    
    except Exception as e:
        return {"error": str(e)}
    # return {"result": "Data received!"}
    
    
