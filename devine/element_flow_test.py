from mira_sdk import MiraClient, CompoundFlow
from mira_sdk.exceptions import FlowError

client = MiraClient(config={"API_KEY": "sb-662643fda34babc9a4864c051586526c"})     # Initialize Mira Client
flow = CompoundFlow(source="./element_flow.yaml")           # Load flow configuration

test_input = {                                              # Prepare test inputs
    "role": "Software Engineer|Backend Developer",
    "email": "t_gorai@es.iitr.ac.in",
    "hr_data": "email: hr1@techcorp.com, name: Vishvas, company: TechCorp, roles: Software Engineer|Backend Developer"
}

try:
    response = client.flow.test(flow, test_input)           # Test entire pipeline
    print("Test response:", response)
except FlowError as e:
    print("Test failed:", str(e))                           # Handle test failure
