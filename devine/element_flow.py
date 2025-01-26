from dotenv import load_dotenv
from mira_sdk import MiraClient, CompoundFlow, Flow, ComposioConfig
from mira_sdk.exceptions import FlowError
import os, json

def process_flow(input_dict):
    print("input_dict:", input_dict)
    load_dotenv()
    client = MiraClient(config={"API_KEY": os.getenv("MIRA_API_KEY")})
    version = '1.0.0'
   
    flow_path = os.path.join(os.path.dirname(__file__), 'element_flow.yaml')
    flow = CompoundFlow(source=flow_path)  # Load flow configuration              # Load flow configuration
    hr_data = '''email: hr1@techcorp.com, name: Vishvas, company: Google
            email: hr2@datavision.com, name:Rahul, company: DataVision
            email: hr3@startuplab.com, name: Priti, company: StartupLab'''

    input_dict = {"role": "Software Engineer", "email": "sarthakrangari788@gmail.com", "hr_data": hr_data}  
    try:
        response = client.flow.test(flow, input_dict) 
        result_str = response.get('result', '')
        print(result_str)
        try:
            data = json.loads(result_str)  # Convert JSON string to Python list
            print("Data:", data)
            # Now you can iterate over the data
            version = '1.0.2'
            for job in data:
                if version:
                    flow2 = f"tinky-devops/hr-email-generator/{version}"
                else:
                    flow2 = "tinky-devops/hr-email-generator"

                input_dict2 = {
                    "name": job['name'],
                    "company": job['company'],
                    "role": job['role'],
                    "email": job['email']
                }
                ENTITY_ID = "t_gorai@es.iitr.ac.in"  # Use a single email address as a string
                # response2 = client.flow.test(flow2, input_dict2) 
                response2 = client.flow.execute(
                    flow2,
                    input_dict2,
                    ComposioConfig(
                        COMPOSIO_API_KEY="tgd6nh30dmd4x8zahfx0e5",
                        ACTION="GMAIL_SEND_EMAIL",  # This is the Enum e.g., "TWITTER_POST", "DISCORD_SEND"
                        TASK="Mail this {content} to tinkygorai9@gmail.com",
                        ENTITY_ID=ENTITY_ID  # Platform-specific identifier (single email address as string)
                    )
                )
                
                print("response2:", response2)
                
                
                
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)

    except FlowError as e:
        print("Test failed:", str(e))