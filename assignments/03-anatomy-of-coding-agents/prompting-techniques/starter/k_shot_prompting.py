"""K-shot prompting — ticket classification.

Task: classify a customer message into one of: billing, shipping, returns,
technical, other. Use in-context EXAMPLES (k-shot) so the model outputs exactly the
label, lowercase, with no extra text.

Only edit YOUR_SYSTEM_PROMPT.
Run:  python k_shot_prompting.py
"""
from ollama import chat

MODEL = "llama3.1:8b"
NUM_RUNS = 5



YOUR_SYSTEM_PROMPT = """You are a customer support ticket classifier for an online store.

Classify each customer message into exactly one of these five categories:
billing, shipping, returns, technical, other.

Category definitions:
- billing: Payments, charges, invoices, or payment errors.
- shipping: Package tracking, delivery times, or missing shipments.
- returns: Returning items, exchanges, or refund requests for returned products.
- technical: Website, app, login, or software problems.
- other: Messages that do not fit the four categories above.

Examples:

Customer: I was charged three times for the same purchase.
Label: billing

Customer: My parcel has not arrived yet.
Label: shipping

Customer: How can I exchange a shirt that is too small?
Label: returns

Customer: The checkout page keeps freezing.
Label: technical

Customer: Do you sell gift wrapping?
Label: other

Now classify the next customer message.

Output exactly one lowercase category label.
Do not include explanations, punctuation, or any additional text."""


CASES = [
    ("My card was charged twice for order 4412.", "billing"),
    ("Where is my package? It's been two weeks.", "shipping"),
    ("I want to send the shoes back for a refund.", "returns"),
    ("The app crashes every time I open my cart.", "technical"),
]


def classify(system_prompt: str, message: str) -> str:
    resp = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        options={"temperature": 0.0},
    )
    return resp.message.content.strip().lower()


def run() -> bool:
    passed = 0
    for message, expected in CASES:
        got = classify(YOUR_SYSTEM_PROMPT, message)
        ok = got == expected
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {message!r} -> got {got!r}, expected {expected!r}")
    print(f"{passed}/{len(CASES)} correct")
    return passed == len(CASES)


if __name__ == "__main__":
    run()
