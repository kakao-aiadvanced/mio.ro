from openai import OpenAI

client = OpenAI()

prompt = """
예제1)
Solve the following problem step-by-step: 23 + 47

Step-by-Step solution:
1. 먼저 두 숫자, 23과 47을 확인합니다.
2. 23은 두 자리 숫자이며, 47 또한 두 자리 숫자입니다.
3. 각 자리의 숫자를 더합니다:
   - 일의 자리: 3 + 7 = 10 (1은 올림).
   - 십의 자리: 2 + 4 + 올림(1) = 7.
4. 두 자리의 합계를 계산하여 결과를 얻습니다: 70.
5. 따라서, 23 + 47의 결과는 70입니다.

Answer: 70

예제2)
Solve the following problem step-by-step: 123 - 58

Step-by-Step Solution:
먼저 두 숫자, 123과 58을 확인합니다.
각 자리에서 숫자를 차례로 뺍니다:
일의 자리: 3 - 8은 음수가 되므로, 십의 자리에서 1을 빌려옵니다.
십의 자리에서 1을 빌리면 3은 13이 됩니다.
13 - 8 = 5.
십의 자리: 십의 자리에서 1을 빌려왔으므로, 2는 1이 됩니다.
1 - 5 = 음수가 되므로 백의 자리에서 1을 빌려옵니다.
십의 자리는 11이 되며, 11 - 5 = 6.
백의 자리: 백의 자리에서 1을 빌려왔으므로, 1은 0이 됩니다.
0이 남습니다.
결과를 각 자리별로 조합하면 65가 됩니다.
따라서, 123 - 58의 결과는 65입니다.

Answer: 65


위와 같은 형식으로 345 + 678 - 123 을 계산하세요.
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)

# Output the result
print(completion.choices[0].message.content)
