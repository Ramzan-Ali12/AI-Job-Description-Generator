from langchain_openai import OpenAI  # Or the specific model you are using
from django.conf import settings
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
import getpass

# Define the desired data structure for the job description
class JobDescription(BaseModel):
    job_title: str = Field(description="Title of the job position")
    company_overview: str = Field(description="Overview of the company")
    role_overview: str = Field(description="Overview of the job role")
    key_responsibilities: str = Field(description="Key responsibilities of the job")
    qualifications: str = Field(description="Qualifications required for the job")
    why_work_with_us: str = Field(description="Reasons to work with the company")


def format_response(parsed_response: JobDescription):
    """
    Formats the parsed response to ensure consistent bullet points in the output.
    
    Args:
        parsed_response (JobDescription): The parsed job description response from the language model.
    
    Returns:
        dict: A dictionary containing the formatted job description.
    """
    # Format each field of the parsed response, ensuring bullet points are correctly formatted
    formatted_response = {
        "Position": parsed_response.job_title,
        "Company Overview": parsed_response.company_overview,
        "Role Overview": parsed_response.role_overview,
        "Key Responsibilities": parsed_response.key_responsibilities.replace('\n', ' '),
        "Qualifications": parsed_response.qualifications.replace('\n', ' '),
        "Why Work with Us?": parsed_response.why_work_with_us.replace('\n', ' ')
    }
    return formatted_response

def setup_langchain():
    """
    Initializes the language model with the OpenAI API key.
    
    Returns:
        OpenAI: An instance of the OpenAI language model initialized with the API key.
    
    Raises:
        EnvironmentError: If the 'OPENAI_API_KEY' is not found in the Django settings.
    """
    api_key = settings.OPENAI_API_KEY  # Fetch the API key from Django settings
    if not api_key:
        raise EnvironmentError("Missing 'OPENAI_API_KEY'. You must provide an API key.")

    return OpenAI(api_key=api_key)  # Initialize the OpenAI model with the API key
    
def generate_job_description(
    job_title, company_name, company_overview, role_overview, 
    key_responsibilities, qualifications, why_work_with_us
):
    """
    Generates a detailed job description using a language model based on the provided inputs.
    
    Args:
        job_title (str): The title of the job position.
        company_name (str): The name of the company.
        company_overview (str): A brief overview of the company.
        role_overview (str): A brief overview of the job role.
        key_responsibilities (str): Key responsibilities associated with the job.
        qualifications (str): Qualifications required for the job.
        why_work_with_us (str): Reasons to work with the company.
    
    Returns:
        dict: A dictionary containing the formatted job description, or an error message if an exception occurs.
    """
    # Inatialize the llm
    try:
        llm = setup_langchain()
    except AttributeError as e:
        print(f"Error fetching OpenAI API key: {e}")
        return {"error": str(e)}   
    # Construct a prompt to generate the job description in a structured JSON format
    prompt = f"""
    Position: {job_title}
    Company Name: {company_name}
    Company Overview: {company_overview}
    Role Overview: {role_overview}
    Key Responsibilities: {key_responsibilities}
    Qualifications: {qualifications}
    Why Work with Us? {why_work_with_us}

    Generate a detailed and engaging job description based on the above information.
    Ensure the response is in JSON format with the following keys:
    - job_title
    - company_overview
    - role_overview
    - key_responsibilities
    - qualifications
    - why_work_with_us

    Format the output in bullet points, with each point starting on a new line, beginning with a bullet symbol (•). Do not include extra newlines between bullet points.
    """
    print(f"Generating job description with prompt: {prompt}")
    try:
        # Call the language model with the constructed prompt
        response = llm(prompt, max_tokens=1500).strip()  # Fetch the response and strip any surrounding whitespace
        print("response--->", response)

        # Parse the JSON response using the output parser
        parser = PydanticOutputParser(pydantic_object=JobDescription)
        parsed_response = parser.parse(response)
        print("parsed_response--->", parsed_response)
        
        # Format and return the parsed response
        return format_response(parsed_response)

    except Exception as e:
        # Print and return an error message if an exception occurs
        print("error--->", e)
        return {"error": str(e)}
