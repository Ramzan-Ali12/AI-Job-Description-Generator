from langchain_openai import OpenAI  # Or the specific model you are using
from django.conf import settings
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

class JobDescription(BaseModel):
    job_title: str = Field(description="Title of the job position")
    company_overview: str = Field(description="Overview of the company")
    role_overview: str = Field(description="Overview of the job role")
    key_responsibilities: str = Field(description="Key responsibilities of the job")
    qualifications: str = Field(description="Qualifications required for the job")
    why_work_with_us: str = Field(description="Reasons to work with the company")

# write a function that converts the key responsibilities, qualifications, and why work with us to bullet points to start with new line


def generate_job_description(job_title, company_name, company_overview, role_overview, key_responsibilities, qualifications, why_work_with_us):
    llm = setup_langchain()
    
    # Create a prompt with JSON structure instruction
    prompt = f"""
    Position: {job_title}

    Company Name: {company_name}

    Company Overview:
    {company_overview}

    Role Overview:
    {role_overview}

    Key Responsibilities:
    {key_responsibilities}

    Qualifications:
    {qualifications}

    Why Work with Us?
    {why_work_with_us}

    Generate a detailed and engaging job description based on the above information.
    Ensure that the response is in JSON format with the following keys:
    - job_title
    - company_overview
    - role_overview
    - key_responsibilities
    - qualifications
    - why_work_with_us

    Please format the output in bullet points, ensuring each point startingis with a new line, starting with a bullet symbol (•). Do not include extra newlines between bullet points.
    """


    try:
        # Call the language model with the prompt
        response = llm(prompt, max_tokens=1500)
        print("response--->", response.strip())

        # Create the output parser
        parser = PydanticOutputParser(pydantic_object=JobDescription)

        # Parse the response using the output parser
        parsed_response = parser.parse(response.strip())
        print("parsed_response--->", parsed_response)
        
        # Ensure all fields, including company_name, are correctly formatted
        formatted_response = {
            "Position": parsed_response.job_title,
            "Company Overview": parsed_response.company_overview,
            "Role Overview": parsed_response.role_overview,
            "Key Responsibilities": parsed_response.key_responsibilities.replace('\n', ' '),
            "Qualifications": parsed_response.qualifications.replace('\n', ' '),
            "Why Work with Us?": parsed_response.why_work_with_us.replace('\n', ' ')
        }
        return formatted_response

    except Exception as e:
        print("error--->", e)
        return {"error": str(e)}

   

def setup_langchain():
    # Configure and return an instance of the language model (e.g., OpenAI)
    # Ensure to replace 'your_api_key' with the actual API key for your model
    # get the api key from the settings
    OPENAI_API_KEY="Your OpenAI API key"
    api_key=OPENAI_API_KEY
    if not api_key:
        raise EnvironmentError("Missing 'OPENAI_API_KEY' environment variable.")
    llm = OpenAI(api_key=api_key)
    return llm