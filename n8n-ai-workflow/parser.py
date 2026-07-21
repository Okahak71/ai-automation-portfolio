import json
import os
from dotenv import load_dotenv

load_dotenv()

def process_webhook_payload(payload):
    """
    Pre-processes incoming webhook payload for n8n AI execution.
    Cleans text input and structures an optimized prompt for downstream LLM nodes.
    """
    try:
        raw_email = payload.get("email", "")
        raw_message = payload.get("message", "")
        email = raw_email.strip().lower() if raw_email else "unknown@domain.com"
        message = raw_message.strip()

        if not message:
            return {
                "status": "error",
                "reason": "Empty message body received."
            }
        formatted_prompt = (
            f"Analyze the following customer support inquiry:\n\n"
            f"Message: \"{message}\"\n\n"
            f"Task:\n"
            f"1. Assign urgency category: (High, Medium, Low)\n"
            f"2. Summarize the core issue in exactly 1 sentence."
        )

        return {
            "status": "success",
            "client_email": email,
            "processed_message": message,
            "ai_prompt": formatted_prompt
        }

    except Exception as e:
        return {
            "status": "error",
            "reason": str(e)
        }

if __name__ == "__main__":
    sample_webhook_input = {
        "email": " Support@ClientBusiness.com ",
        "message": " Our payment API integration is dropping transactions continuously! Need urgent fix. "
    }
    
    print("📡 Testing Webhook Pre-processor Node...")
    result = process_webhook_payload(sample_webhook_input)
    print("\n✅ Processed Output Payload:")
    print(json.dumps(result, indent=2))