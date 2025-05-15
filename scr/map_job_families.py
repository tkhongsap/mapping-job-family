import json
import os
import glob
import argparse
import time
from pathlib import Path
from openai import AzureOpenAI
import dotenv

# Load environment variables from .env file if it exists
try:
    dotenv.load_dotenv()
except:
    pass

endpoint = "https://ai-totrakoolk6076ai346198185670.openai.azure.com/"
model_name = os.getenv("AZURE_OPENAI_MODEL_NAME")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

def load_job_categories():
    """Load job categories from the job-category.json file."""
    with open("job-category.json", "r", encoding="utf-8") as f:
        return json.load(f)

def test_api_connection(client):
    """Test if the API connection is working with the provided key."""
    try:
        response = client.responses.create(
            model=deployment,
            input=[{
                "role": "user",
                "content": "test"
            }]
        )
        return True
    except Exception as e:
        print(f"Error connecting to Azure OpenAI API: {str(e)}")
        return False

def map_job_to_family(position, industry, job_categories, client):
    """
    Use OpenAI API to map a position and industry to a job family and sub-family.
    
    Args:
        position: The job position title
        industry: The industry of the job
        job_categories: Dictionary of job families and their sub-families
        client: OpenAI client instance
    
    Returns:
        Tuple of (job_family, job_sub_family)
    """
    # Create a structured prompt for the model
    job_families = list(job_categories.keys())
    
    system_message = """You are a specialized job classification expert tasked with precisely matching job positions to the SINGLE most relevant job family and job sub-family.

Your task requires extreme precision and careful consideration. You must:
1. Thoroughly examine ALL available job sub-families in each job family
2. Consider both the position title AND industry context
3. Find the SINGLE MOST SPECIFIC and RELEVANT match possible
4. Select ONLY ONE job family and ONE job sub-family - not multiple options
5. Never select a generic category when a more specific match exists
6. Consider job responsibilities, skills, and domain knowledge implied by the position title

Provide your answer ONLY as a JSON object with exactly two fields: "job_family" and "job_sub_family".
Both values MUST exist exactly as written in the provided categories list - do not modify or create new categories.

IMPORTANT: Each position must be assigned to EXACTLY ONE job family and ONE job sub-family - the MOST relevant match."""
    
    prompt = f"""I need to classify the job position: "{position}" in the industry: "{industry}"

Please determine the SINGLE most appropriate job family and job sub-family from the following categories:

"""
    
    # Add all job families and their sub-families
    for family, sub_families in job_categories.items():
        prompt += f"\n## {family}\n"
        for sub_family in sub_families:
            prompt += f"- {sub_family}\n"
    
    prompt += """
Carefully evaluate ALL possible job sub-families to find the ONE closest match to the position title.
Consider the skills, responsibilities, and domain knowledge typically associated with this position.
If the industry context provides additional clues, use that information in your decision.

CRITICAL REQUIREMENTS:
1. Select ONLY ONE job family and ONE job sub-family
2. Choose the MOST relevant match based on the position title and industry
3. DO NOT provide multiple options or alternatives

IMPORTANT: Your response must be a valid JSON object containing ONLY:
{"job_family": "selected job family", "job_sub_family": "selected job sub-family"}

The selected job family and sub-family MUST exactly match one of the options provided above.
"""
    
    try:
        # Call OpenAI API using the response.create() endpoint with proper input format
        response = client.responses.create(
            model=deployment,
            input=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Debug output to understand the response structure
        try:
            # First check if the output attribute exists
            if hasattr(response, 'output_text'):
                response_text = response.output_text
            # If output_text doesn't exist, check if there's an output array with content
            elif hasattr(response, 'output') and response.output:
                # Extract the text from the first message's content
                for item in response.output:
                    if hasattr(item, 'content') and item.content:
                        for content_item in item.content:
                            if hasattr(content_item, 'text'):
                                response_text = content_item.text
                                break
                        if 'response_text' in locals():
                            break
            
            if 'response_text' not in locals():
                print(f"Warning: Could not extract text from response for position '{position}'")
                print(f"Response structure: {response}")
                return None, None
            
            # Try to parse the response text as JSON
            if response_text and '{' in response_text:
                # Extract JSON object from text if it's embedded in other text
                start_index = response_text.find('{')
                end_index = response_text.rfind('}') + 1
                if start_index >= 0 and end_index > start_index:
                    json_str = response_text[start_index:end_index]
                    result = json.loads(json_str)
                else:
                    # If no JSON object found, use the whole text
                    result = json.loads(response_text)
            else:
                print(f"Warning: Response does not contain a JSON object for position '{position}'")
                print(f"Response text: {response_text}")
                return None, None
                
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response for position '{position}': {str(e)}")
            print(f"Response text: {response_text}")
            return None, None
        except Exception as e:
            print(f"Unexpected error processing response for position '{position}': {str(e)}")
            return None, None
        
        # Verify that the response contains valid job family and sub-family
        if "job_family" not in result:
            print(f"Warning: Response missing job_family field for position '{position}'")
            return None, None
            
        if "job_sub_family" not in result:
            print(f"Warning: Response missing job_sub_family field for position '{position}'")
            return None, None
            
        if result["job_family"] not in job_categories:
            print(f"Warning: API returned invalid job family for position '{position}': {result['job_family']}")
            return None, None
            
        if result["job_sub_family"] not in job_categories[result["job_family"]]:
            print(f"Warning: API returned invalid job sub-family for position '{position}': {result['job_sub_family']}")
            return result["job_family"], None
            
        return result["job_family"], result["job_sub_family"]
        
    except Exception as e:
        print(f"Error calling Azure OpenAI API for position '{position}': {str(e)}")
        return None, None

def process_files():
    """Process all row_x.json files in the output directory."""
    # Test the API connection
    print("Testing API connection...")
    if not test_api_connection(client):
        print("Failed to connect to the Azure OpenAI API. Please check your configuration and try again.")
        return
    
    print("API connection successful!")
    
    # Load job categories
    job_categories = load_job_categories()
    
    # Get all row_x.json files
    output_dir = "output"
    files = glob.glob(os.path.join(output_dir, "row_*.json"))
    
    print(f"Found {len(files)} files to process")
    
    for i, file_path in enumerate(files):
        print(f"Processing file {i+1}/{len(files)}: {file_path}")
        
        try:
            # Load the JSON content with UTF-8 encoding
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Extract position and industry
            # Try multiple possible field names for position
            position = None
            position_field_names = ["Position", "[Position]", "position", "ตำแหน่ง"]
            for field_name in position_field_names:
                if field_name in data and data[field_name]:
                    position = data[field_name]
                    break
            
            industry = data.get("Industry", "")
            
            if not position:
                print(f"Warning: No position found in {file_path}, skipping")
                continue
            
            # Map to job family and sub-family
            job_family, job_sub_family = map_job_to_family(position, industry, job_categories, client)
            
            # Update the JSON with mapping
            data["job_family"] = job_family
            data["job_sub_family"] = job_sub_family
            
            # Save the updated file with UTF-8 encoding
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"  Mapped '{position}' to {job_family} / {job_sub_family}")
            
            # Add a small delay to respect API rate limits
            time.sleep(1)
            
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
    
    print("Processing complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map job positions to job families using Azure OpenAI API")
    parser.add_argument("--batch_size", type=int, default=20, help="Number of files to process in one batch.")
    parser.add_argument("--start_index", type=int, default=0, help="Index of the first file to process.")
    
    args = parser.parse_args()
    process_files() 