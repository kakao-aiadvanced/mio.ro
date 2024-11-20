from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": """원하는 문장을 전달하면 해당하는 쿼리를 생성하는 sql을 만들어줘.

예제:
"급여가 50,000달러 이상인 모든 직원 정보를 조회하세요.":
SELECT * FROM employees WHERE salary > 50000;

"재고가 없는 모든 상품을 나열하세요.":
SELECT * FROM products WHERE stock = 0;

"수학 시험에서 90점 이상을 받은 학생들의 이름을 가져오세요.":
SELECT name FROM students WHERE math_score > 90;

"지난 30일 동안 주문된 모든 주문을 가져오세요.":
SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);

"도시별 고객 수를 표시하세요.":
SELECT city, COUNT(*) FROM customers GROUP BY city;

다음 요청에 대해서 SQL을 만들어줘.
리뷰: "회사 연봉 테이블에서 연봉이 제일 높은 순서대로 직원들 이름과 연봉을 출력해줘."
"""
        }
    ]
)

print(completion.choices[0].message)
