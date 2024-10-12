import requests

HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
HUGGING_FACE_API_KEY = "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"

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
}

response = requests.post(HUGGING_FACE_API_URL, headers=headers, json={"inputs": "Explain the significance of machine learning."})


print(response.status_code)
print(response.json())
