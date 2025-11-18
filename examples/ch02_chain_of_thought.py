"""
Chapter 2: Chain-of-Thought 프롬프팅 실습
추론 능력을 향상시키는 프롬프팅 기법
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def simple_prompt(question: str) -> str:
    """일반적인 프롬프트"""
    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content


def chain_of_thought_prompt(question: str) -> str:
    """Chain-of-Thought 프롬프트"""
    cot_question = f"""{question}

Let's solve this step by step:"""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": cot_question}]
    )
    return response.choices[0].message.content


def zero_shot_cot_prompt(question: str) -> str:
    """Zero-shot Chain-of-Thought"""
    zs_cot_question = f"""{question}

Let's think step by step:"""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": zs_cot_question}]
    )
    return response.choices[0].message.content


def main():
    """메인 함수"""
    print("\n🧠 Chapter 2: Chain-of-Thought 프롬프팅 실습\n")

    # 보안 관련 문제로 테스트
    questions = [
        "A server has ports 22, 80, 443, and 3306 open. What security risks does this pose?",
        "If an attacker has access to a SQL injection vulnerability, what steps would they take to exploit it?",
        "How would you prioritize patching these vulnerabilities: XSS (CVSS 6.5), SQL Injection (CVSS 9.1), and Outdated SSL (CVSS 5.3)?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"Question {i}: {question}")
        print(f"{'='*60}")

        print("\n--- Simple Prompt ---")
        print(simple_prompt(question))

        print("\n--- Chain-of-Thought Prompt ---")
        print(chain_of_thought_prompt(question))

        print("\n--- Zero-shot CoT Prompt ---")
        print(zero_shot_cot_prompt(question))

        print("\n")


if __name__ == "__main__":
    main()
