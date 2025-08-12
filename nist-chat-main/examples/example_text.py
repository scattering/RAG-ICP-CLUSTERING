import httpx
import openai
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# This will make any API keys defined in the .env file available through os.environ
# For example, if you have RCHAT_API_KEY=your_key in your .env file,
# it will be accessible via os.environ.get("RCHAT_API_KEY")

url = "https://rchat.nist.gov/api" 


model = "Llama-4-Maverick-17B-128E-Instruct-FP8"



# Create a non-async client to test the connection
test_client = openai.OpenAI(
    base_url=url,
    api_key=os.environ.get("RCHAT_API_KEY"),
    http_client=httpx.Client(verify=False)
)

content = "This is a test, please say \"the cake is a lie\""

try:
    response = test_client.chat.completions.create(
                    model=model,
                    max_tokens=128,
                    temperature=0.7,
                    top_p=0.95,
                    stream=False,
                    messages=[
                        {"role": "user", "content": content}
                    ]
                )
    print(response.choices[0].message.content)
except Exception as e:
    # optional handling here, but for now nothing to do
    raise e