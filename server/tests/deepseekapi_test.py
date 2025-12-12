from openai import OpenAI


client = OpenAI(api_key="", base_url="https://api.deepseek.com")

resp = client.chat.completions.create(
    model="deepseek-reasoner", messages=[{"role": "user", "content": "Hello, test."}]
)

print(resp)
