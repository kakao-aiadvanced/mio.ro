from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": """다음은 영화 리뷰에 대한 감정을 분석하는 예제입니다. 각 문장은 긍정적(positive) 또는 부정적(negative)으로 분류됩니다.

예제:
1. 리뷰: "영화는 환상적이었고 스릴 넘치는 순간들로 가득 차 있었습니다."
   감정: positive
2. 리뷰: "연기는 평범했고 줄거리는 뻔했습니다."
   감정: negative
3. 리뷰: "오랫동안 기억에 남을 걸작입니다."
   감정: positive
4. 리뷰: "특수 효과가 과도하게 사용되어 산만했습니다."
   감정: negative
5. 리뷰: "잘 구성된 캐릭터로 감동적인 여정을 선사했습니다."
   감정: positive

이제 다음 리뷰에 대해 감정을 분석하세요:
리뷰: "줄거리가 재미 있고 감동적 이었습니다."
"""
        }
    ]
)

print(completion.choices[0].message)
