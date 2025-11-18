"""
Chapter 1: Temperature 파라미터 실습
Temperature가 LLM 생성 결과에 미치는 영향 이해
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_with_temperature(prompt: str, temperature: float) -> str:
    """주어진 temperature로 텍스트 생성"""
    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def main():
    """메인 함수"""
    print("\n🌡️ Chapter 1: Temperature 파라미터 실습\n")

    # 보안 시나리오 프롬프트
    prompts = [
        "Describe three common phishing attack techniques.",
        "Write a short security incident response procedure.",
        "Explain how SQL injection works in one paragraph.",
    ]

    # Temperature 값들
    temperatures = [0.0, 0.5, 1.0, 1.5, 2.0]

    for prompt in prompts:
        print(f"\n{'='*60}")
        print(f"Prompt: {prompt}")
        print(f"{'='*60}\n")

        for temp in temperatures:
            print(f"\n--- Temperature: {temp} ---")
            result = generate_with_temperature(prompt, temp)
            print(result[:300] + "..." if len(result) > 300 else result)

        print("\n")

    # Temperature 설명
    print(f"\n{'='*60}")
    print("Temperature 파라미터 이해")
    print(f"{'='*60}")
    print("""
Temperature는 LLM의 생성 결과의 무작위성을 제어합니다:

- Temperature = 0.0
  * 가장 확률이 높은 토큰만 선택 (결정적)
  * 일관되고 예측 가능한 출력
  * 사실 기반 정보, 코드 생성에 적합

- Temperature = 0.5-0.7
  * 균형잡힌 창의성과 일관성
  * 대부분의 작업에 권장되는 기본값
  * 기술 문서, 분석에 적합

- Temperature = 1.0-1.5
  * 높은 무작위성과 창의성
  * 다양한 아이디어 생성
  * 브레인스토밍, 창작에 적합

- Temperature = 2.0
  * 매우 높은 무작위성
  * 예측 불가능하고 때로 비논리적
  * 일반적으로 비권장

보안 작업에서의 권장사항:
- 위협 분석, 정책 문서: 0.0-0.3
- 보안 교육 컨텐츠: 0.5-0.7
- Red Team 시나리오 생성: 0.7-1.0
""")


if __name__ == "__main__":
    main()
