from openai import OpenAI

client = OpenAI()

prompt = """
# Intermediate - 1
Solve the following logic puzzle step-by-step:
Three friends, Alice, Bob, and Carol, have different favorite colors: red, blue, and green. We know that:
1. Alice does not like red.
2. Bob does not like blue.
3. Carol likes green.

Determine the favorite color of each friend.

Step-by-Step Solution:
Identify the facts from the problem:

Alice does not like red.
Bob does not like blue.
Carol likes green.
Assign Carol's favorite color:

Since Carol likes green, her favorite color must be green.
Remove green as an option for Alice and Bob:

Alice and Bob cannot have green as their favorite color because Carol already has it.
Determine Bob's favorite color:

Bob does not like blue, so his only remaining option is red. Therefore, Bob's favorite color is red.
Assign Alice's favorite color:

Alice does not like red, and green is already taken by Carol. Therefore, Alice's favorite color must be blue.
Verify the solution:

Alice: blue
(Correct, as Alice does not like red and green is not available.)
Bob: red
(Correct, as Bob does not like blue and green is not available.)
Carol: green
(Correct, as stated in the problem.)
Final Answer:

Alice: blue
Bob: red
Carol: green

----
# Intermediate - 2
Solve the following logic puzzle step-by-step:
Four people (A, B, C, D) are sitting in a row. We know that:
1. A is not next to B.
2. B is next to C.
3. C is not next to D.

Determine the possible seating arrangements.

Step-by-Step Solution:
Understand the problem:

Four people (A, B, C, D) need to be arranged in a row.
Constraints:
A is not next to B.
B is next to C.
C is not next to D.
Interpret the constraints:

Constraint 1: A and B cannot sit next to each other.
Constraint 2: B and C must sit next to each other.
Constraint 3: C and D cannot sit next to each other.
Identify the relationship between B and C:

Since B and C must sit next to each other, possible pairs are BC or CB.
Consider the placement of A and D:

A cannot sit next to B, so A must be separated from the BC pair.
C and D cannot be next to each other, so D must also be separated from the BC pair.
Explore possible arrangements:

Start with the pair BC and place A and D around them:

If A is placed on the left and D on the right: A - B - C - D
This violates Constraint 3 (C is next to D).
Not valid.
If D is placed on the left and A on the right: D - B - C - A
All constraints are satisfied.
Valid arrangement: DBCA
If A is placed on the left and D in the middle: A - D - B - C
This violates Constraint 2 (B is not next to C).
Not valid.
Next, consider the pair CB and place A and D around them:

If A is placed on the left and D on the right: A - C - B - D
All constraints are satisfied.
Valid arrangement: ACBD
If D is placed on the left and A on the right: D - C - B - A
This violates Constraint 3 (C is next to D).
Not valid.
List the valid arrangements:

From the exploration above, the valid arrangements are:
DBCA
ACBD


Answer:
- Possible arrangements: BCAD, CABD


위와 같은 형식으로 아래 문제에 대해 답변하세요.
Temperature, Maximum Tokens, Stop sequences, Top P, Frequency Penalty, Presence Penalty
"""

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)

# Output the result
print(completion.choices[0].message.content)
