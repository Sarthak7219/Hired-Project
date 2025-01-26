from mira_sdk import MiraClient, Flow, ComposioConfig
from dotenv import load_dotenv
import os

ENTITY_ID = "t_gorai@es.iitr.ac.in"  # Use a single email address as a string

def process_flow(input_dictt):
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the API key from the environment
    api_key = os.getenv("MIRA_API_KEY")
    # Initialize Mira client with your API key
    client = MiraClient(config={"API_KEY": api_key})

    # Get your existing flow
    version = "1.0.1"

    # If no version is provided, the latest version is used by default
    if version:
        flow = f"tinky-devops/job-hr-info-matcher/{version}"
    else:
        flow = "tinky-devops/job-hr-info-matcher"

    role = input_dictt['role']
    # Set up your flow's input parameters
    input_dict = {
        "job_data": {
            "title": role,
            "company": "TechCorp",
            "location": "Bangalore",
            "batch": "2023",
            "stream": "Computer Science"
        },
    }

    # Execute flow with Composio integration
    try:
        response = client.flow.execute(
            flow,
            input_dict,
            ComposioConfig(
                COMPOSIO_API_KEY="tgd6nh30dmd4x8zahfx0e5",
                ACTION="GMAIL_SEND_EMAIL",  # This is the Enum e.g., "TWITTER_POST", "DISCORD_SEND"
                TASK="Mail this {content} to tinkygorai9@gmail.com",
                ENTITY_ID=ENTITY_ID  # Platform-specific identifier (single email address as string)
            )
        )
        print("Response:", response)
        result_str = response.get('result', '')
        if result_str:
            print("Result:", result_str)
        else:
            print("No result returned from the flow.")
    except Exception as e:
        print("An error occurred:", str(e))

# Example usage (this part should be removed or commented out in production)
if __name__ == "__main__":
    input_dict = {"role": "Software Engineer"}
    process_flow(input_dict)