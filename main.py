from fastapi import FastAPI, File, Form, UploadFile
from dotenv import load_dotenv
from utils.flow import process_input
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os, json
import tempfile
# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or specify specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def api_check():
    return "API runned successfully"

# Route to handle input data
@app.post("/run_script")
async def run_script(
    role: str = Form(...),
    batch: str = Form(...),
    location: str = Form(...),
    desired_salary: int = Form(...),
    user_email: str = Form(...),
    app_password: str = Form(...),
    email_content: str = Form(...),
    hr_data: str = Form(...),  # Get HR data as a string (we'll parse it)
    resume: UploadFile = File(...),  # Use UploadFile for file handling
):

    try:
        
        try:
            hr_data_list = json.loads(hr_data)
        except json.JSONDecodeError:
            return {"error": "Invalid HR data format"}



        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            temp_file_path = tmp_file.name
            # Save the resume to the temporary file
            with open(temp_file_path, "wb") as f:
                shutil.copyfileobj(resume.file, f)

        output = process_input(role, batch, location, desired_salary, user_email, app_password, email_content, hr_data_list , temp_file_path)
        print(f"Process output: {output}")

        # Remove the temporary file after processing
        os.remove(temp_file_path)
        return {"result": output}
    
    except Exception as e:
        print(f"Error in process_input: {e}")
        return {"error": str(e)}
    # return {"result": "Data received!"}
    
    
