"""llm invocation"""

from fastapi import APIRouter
import cohere
from dotenv import load_dotenv
import os
import importlib.metadata



router = APIRouter(
    prefix="/get_llm_joke",
    tags=["get_llm_joke"]
)

# Load variables from .env file
load_dotenv()

api_key = os.getenv("COHERE_API_TOKEN")



@router.get("/")
def call_llm():
    """Create a cohere client and tell a joke"""
    
    if not api_key:
        return {"error": "COHERE_API_TOKEN not set"}
    
    try:
        # Create client
        co_v2 = cohere.ClientV2(api_key=api_key)
        
        # Test with a simple call - if this works, client is valid
        response = co_v2.chat(
            model="command-a-plus-05-2026",
            messages=[{"role": "user", "content": "Tell me a joke!"}],
            thinking={
                "type":"disabled"
            }
        )
        
        # If we get here, client is valid
        return {"llm_response": response.message.content[0].text}
        
    except Exception as e:
        return {"error": f"Client validation failed: {str(e)}"}