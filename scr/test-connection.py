import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

print(openai_api_key)
