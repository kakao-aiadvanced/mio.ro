from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": """다음은 영어 단어를 한국어로 번역하는 예제입니다. 주어진 단어를 정확히 번역하고, 그 결과를 제공합니다.

예제:
apple:사과  
computer:컴퓨터  
book:책  
water:물  
house:집  

이제 다음 단어를 번역하세요.  
영어: dog"""
        }
    ]
)

print(completion.choices[0].message)