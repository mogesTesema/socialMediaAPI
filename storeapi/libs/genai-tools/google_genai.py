from google import genai

client = genai.Client(api_key="AIzaSyAbrWILy1ujwxbHitBR5xuTcpzzgit3ahs")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="generate brand new cute  girl image she is about 15 years old,just generate yourself and give me intended image, not text",
)
print(f"response: {response}")
print(f"response json:{response.json()}")
print(response.text)
