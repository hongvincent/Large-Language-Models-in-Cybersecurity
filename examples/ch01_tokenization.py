"""
Chapter 1: Tokenization 실습
LLM의 토큰화 과정을 이해하기 위한 예제
"""

import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_tokenization(text: str):
    """텍스트의 토큰화 분석"""
    print(f"\n{'='*60}")
    print(f"Original Text: {text}")
    print(f"{'='*60}")

    # GPT-5.1을 사용하여 토큰 분석
    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[
            {
                "role": "user",
                "content": f"""Analyze the tokenization of this text: "{text}"

Explain:
1. How many tokens would this be?
2. How would it be split into tokens?
3. Why is tokenization important for LLMs?"""
            }
        ]
    )

    print(f"\nTokenization Analysis:")
    print(response.choices[0].message.content)
    print(f"\n{'='*60}\n")


def main():
    """메인 함수"""
    print("\n🔍 Chapter 1: Tokenization 실습\n")

    # 다양한 텍스트로 토큰화 테스트
    test_texts = [
        "Hello, world!",
        "Large Language Models in Cybersecurity",
        "한글도 토큰화가 어떻게 될까요?",
        "Code: print('Hello')",
        "SQL injection: ' OR '1'='1",
    ]

    for text in test_texts:
        analyze_tokenization(text)


if __name__ == "__main__":
    main()
