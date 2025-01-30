from utils.data_scraper import data_scraper
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv, os

## Merge the jobs and hr data--------------->
def merge_jobs_and_hrs(jobs: list[dict], hrs: list[dict]) -> list[dict]:

    hr_data = {hr["company"].strip().lower(): {"hr_name": hr["name"], "hr_email": hr["email"]} for hr in hrs}
    
    merged_data = []
    for job in jobs:
        job_company = " ".join(job["company"].strip().lower().split())
        if job_company in hr_data:
            merged_data.append({
                "company": job["company"],
                "role": job["title"],
                "hr_name": hr_data[job_company]["hr_name"],
                "hr_email": hr_data[job_company]["hr_email"],
                "job_url": job['url'],
            })
    
    return merged_data


##Email sender function ----------->
def send_emails(job_hr_data_filtered: list[dict], sender_email: str, user_email:str, sender_password: str, file_path: str, job_data: list[dict], email_content: str):
    # Connect to the SMTP server
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Use your SMTP provider's details
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)

        all_jobs_csv_file = "all_jobs_csv_file.csv"
        hr_jobs_csv_file = "hr_jobs_csv_file.csv"

        try:
            with open(all_jobs_csv_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=job_data[0].keys())
                writer.writeheader()
                writer.writerows(job_data)
            

            # Create the email content to send the user's email
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = user_email
            message["Subject"] = "Job opportunities for you"
            body = """Dear Job Seeker,
We hope this email finds you well. We have compiled a list of exciting job opportunities that may interest you. Please find the details below:

The file 'All_Job_Opportunities.csv' contains all the relevant job opportunities and 'Mailed_Jobs.csv' contains jobs where cold email is sent to the HRs"""
            message.attach(MIMEText(body, "plain"))

            # Attach the CSV file
            with open(all_jobs_csv_file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename=All_Job_Opportunities.csv")
                message.attach(part)
            

            if job_hr_data_filtered:

                try:
                    with open(hr_jobs_csv_file, mode='w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=job_hr_data_filtered[0].keys())
                        writer.writeheader()
                        writer.writerows(job_hr_data_filtered)
                    with open(hr_jobs_csv_file, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename=Mailed_Jobs.csv")
                        message.attach(part)
                except Exception as e:
                    print(f"Error creating CSV file: {e}")

            # Send the email
            server.sendmail(sender_email, user_email, message.as_string())
            print(f"Email sent to the user {user_email} with the attached files.")
        except Exception as e:
            print(f"Error creating CSV file: {e}")
        

        for entry in job_hr_data_filtered:
            # Extract information for the email
            hr_email = entry["hr_email"]
            hr_name = entry["hr_name"]
            role = entry["role"]
            company = entry["company"]

            # Create the email content
            subject = f"Application for the {role} role at {company}"
            body = email_content.format(hr_name=hr_name, role=role, company=company)
            # Create the email
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = hr_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Attach the file (resume)
            try:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename={file_path.split('/')[-1]}")
                    message.attach(part)
            except Exception as e:
                print(f"Error attaching file: {e}")
            
            # Send the email
            try:
                server.sendmail(sender_email, hr_email, message.as_string())
                # print(f"Email sent to {hr_email} for {role} at {company}")
            except Exception as e:
                print("An error occurred while sending mail:", e)

    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the connection to the server
        server.quit()
        if os.path.exists(all_jobs_csv_file):
            os.remove(all_jobs_csv_file)
        if os.path.exists(hr_jobs_csv_file):
            os.remove(hr_jobs_csv_file)


def process_input(role: str, batch:str, location:str, desired_salary:int, user_email: str, app_password: str, email_content:str, hr_data: list[dict], temp_file_path: str) -> str:
# -----Flow1-----
   
    jobs = data_scraper(role, batch, location, desired_salary) #--> List of dict
    # print("Relevant jobs: ",jobs)


    job_hr_data_filtered = merge_jobs_and_hrs(jobs, hr_data)
    if not job_hr_data_filtered:
        print("HR data didn't match any jobs posting")

    ##Send mail to all the HRs
    if jobs:
        send_emails(job_hr_data_filtered, user_email, user_email, app_password, temp_file_path, jobs, email_content)
    else: 
        return "No relevant jobs found!"
    
    return "Emails sent successfully!"


# ###Calling the function
# process_input("Software Engineer", "2025", "", 12, "sarthakrangari788@gmail.com")