import httpx
import openai
import os
import base64

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# This will make any API keys defined in the .env file available through os.environ
# For example, if you have RCHAT_API_KEY=your_key in your .env file,
# it will be accessible via os.environ.get("RCHAT_API_KEY")

url = "https://rchat.nist.gov/api"

model = "Llama-4-Maverick-17B-128E-Instruct-FP8"

test_client = openai.OpenAI(
    base_url=url,
    # api_key="sk-no-key-required",
    api_key=os.environ.get("RCHAT_API_KEY"),
    http_client=httpx.Client(verify=False)
)

text = "What's in this image?"

# Supported content types are: png, jpeg, and webp
image_path = "example.jpg"

with open(image_path, "rb") as image_file:
    image_buffer = image_file.read()
    encoded_image = base64.b64encode(image_buffer).decode("utf-8")

# For png files: f"data:image/png;base64,{encoded_image}"
# For webp files: f"data:image/webp;base64,{encoded_image}"
image_url = f"data:image/jpeg;base64,{encoded_image}"

try:
    response = test_client.chat.completions.create(
        model=model,
        max_tokens=1024,
        temperature=0.7,
        top_p=0.95,
        stream=False,
        messages=[
            {
                "role": "user",
                 "content": [
                    {"type": "text", "text": text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]
    )

    print(response.choices[0].message.content)

except Exception as e:
    # optional handling here, but for now nothing to do
    raise e