"""
Chapter 8: Phishing and Social Engineering (교육용)
LLM을 활용한 피싱 시뮬레이션 - 교육 및 훈련 목적만

⚠️ ETHICAL USE ONLY: This is for security awareness training and authorized testing only.
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_phishing_training_example(scenario: dict) -> dict:
    """보안 교육용 피싱 이메일 예제 생성"""

    prompt = f"""You are a cybersecurity trainer creating educational phishing examples.

Generate a realistic phishing email for security awareness training:

Target Organization: {scenario.get('target_org', 'Generic Company')}
Scenario: {scenario.get('scenario', 'Password reset')}
Sophistication Level: {scenario.get('sophistication', 'Medium')}

Requirements:
1. Make it realistic but clearly mark it as a TRAINING EXAMPLE
2. Include common phishing indicators that employees should spot
3. After the email, add a section labeled "[SECURITY EDUCATION]" that explains:
   - What red flags are present
   - Why this is suspicious
   - What the correct action should be
   - How to verify legitimacy

Format:
---TRAINING EMAIL---
[Email content]

---SECURITY EDUCATION---
[Educational analysis]
"""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[
            {
                "role": "system",
                "content": "You are a cybersecurity trainer creating educational materials for security awareness programs. All content is for authorized training purposes only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "scenario": scenario,
        "training_material": response.choices[0].message.content
    }


def analyze_phishing_techniques(attack_type: str) -> str:
    """피싱 공격 기법 분석 (교육용)"""

    prompt = f"""As a cybersecurity educator, explain the phishing technique: {attack_type}

Cover:
1. How it works
2. Common variations
3. Detection methods
4. Real-world examples (anonymized)
5. Defense strategies
6. Employee training points

Focus on education and defense, not execution."""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def main():
    """메인 함수"""
    print("\n🎣 Chapter 8: Phishing Simulation (Security Training)\n")
    print("⚠️  ETHICAL USE ONLY - For authorized security training\n")

    print("="*60)
    print("1. Phishing Email Training Examples")
    print("="*60)

    training_scenarios = [
        {
            "target_org": "Tech Startup",
            "scenario": "Urgent IT security update required",
            "sophistication": "Low"
        },
        {
            "target_org": "Financial Services",
            "scenario": "CEO requesting urgent wire transfer",
            "sophistication": "Medium"
        },
        {
            "target_org": "Healthcare Provider",
            "scenario": "HIPAA compliance audit verification",
            "sophistication": "High"
        },
        {
            "target_org": "E-commerce Platform",
            "scenario": "Account suspension notice",
            "sophistication": "Medium"
        },
    ]

    for i, scenario in enumerate(training_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"Training Scenario {i}:")
        print(f"Organization: {scenario['target_org']}")
        print(f"Scenario: {scenario['scenario']}")
        print(f"Level: {scenario['sophistication']}")
        print(f"{'='*60}\n")

        result = generate_phishing_training_example(scenario)
        print(result["training_material"])
        print("\n")

    print("\n" + "="*60)
    print("2. Phishing Technique Analysis (Educational)")
    print("="*60)

    techniques = [
        "Spear Phishing",
        "Whaling (CEO Fraud)",
        "Vishing (Voice Phishing)",
        "Smishing (SMS Phishing)",
        "Clone Phishing",
        "Watering Hole Attacks",
    ]

    for technique in techniques:
        print(f"\n{'='*60}")
        print(f"Technique: {technique}")
        print(f"{'='*60}\n")

        analysis = analyze_phishing_techniques(technique)
        print(analysis[:500] + "...\n")

    print("\n" + "="*60)
    print("3. Social Engineering Tactics")
    print("="*60)

    se_prompt = """Analyze common social engineering tactics used in cybersecurity attacks:

For each tactic, explain:
1. Psychological principle exploited
2. Common scenarios
3. How to recognize it
4. Defense mechanisms
5. Training recommendations

Tactics to cover:
- Urgency/Scarcity
- Authority
- Trust/Familiarity
- Fear
- Curiosity
- Reciprocity

Make this educational and defense-focused."""

    se_analysis = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": se_prompt}]
    )

    print(se_analysis.choices[0].message.content)

    print("\n\n" + "="*60)
    print("4. Building a Phishing Simulation Program")
    print("="*60)

    program_prompt = """Design a comprehensive phishing simulation and training program for an organization:

Include:
1. Program goals and metrics
2. Baseline assessment approach
3. Simulation frequency and progression
4. Email template categories (by difficulty)
5. Reporting and analytics
6. Training integration
7. Success metrics
8. Continuous improvement process

Provide practical implementation guidance."""

    program_design = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": program_prompt}]
    )

    print(program_design.choices[0].message.content)

    print("\n\n" + "="*60)
    print("5. LLM-Enhanced Phishing: Risks and Defenses")
    print("="*60)

    llm_risk_prompt = """Analyze how LLMs change the phishing landscape:

Threats:
1. How LLMs make phishing easier for attackers
2. Improved personalization at scale
3. Better language and fewer errors
4. Adaptive phishing campaigns
5. Voice and deepfake integration

Defenses:
1. LLM-powered detection systems
2. Training employees on AI-generated content
3. Technical controls
4. Process improvements
5. Future outlook

Provide balanced, actionable analysis."""

    llm_analysis = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": llm_risk_prompt}]
    )

    print(llm_analysis.choices[0].message.content)

    print("\n\n" + "="*60)
    print("Summary: Phishing Defense in the Age of LLMs")
    print("="*60)
    print("""
LLM이 피싱 환경에 미치는 영향:

**Threat Landscape Changes:**

1. **Attacker Advantages**
   - 완벽한 문법과 스타일
   - 대규모 맞춤화 가능
   - 다국어 캠페인 쉽게 생성
   - 소셜 미디어 기반 타겟팅 향상

2. **Traditional Detection의 한계**
   - 문법 오류 감지 무력화
   - 일반적 템플릿 매칭 어려움
   - 휴리스틱 기반 필터 우회

**Defense Strategies:**

1. **Technical Controls**
   - AI 기반 이메일 분석
   - 링크 샌드박싱
   - DMARC/SPF/DKIM 강화
   - URL 재작성 및 검증

2. **User Training**
   - LLM 생성 콘텐츠 특징 교육
   - 검증 프로세스 강조
   - 정기적 시뮬레이션
   - 보고 문화 조성

3. **Process Improvements**
   - 다단계 승인 프로세스
   - 대역외 검증 (out-of-band)
   - 민감 작업에 대한 추가 인증
   - 인시던트 보고 간소화

**Security Awareness Program:**

1. 정기적 훈련 (최소 분기별)
2. 다양한 난이도의 시뮬레이션
3. 즉각적 피드백
4. 긍정적 강화 (처벌보다 교육)
5. 메트릭 추적 및 개선

**Ethical Considerations:**

⚠️ 피싱 시뮬레이션은 반드시:
- 승인된 프로그램의 일부
- 명확한 교육 목표
- 직원 프라이버시 존중
- 투명한 의도
- 법적 컴플라이언스 준수

**Tools & Platforms:**
- GoPhish (오픈소스)
- KnowBe4
- Cofense PhishMe
- Proofpoint Security Awareness
- Custom LLM solutions

**Next Steps:**
- 실제 피싱 탐지는 ch08_phishing_detection.py 참조
- 고급 social engineering은 Chapter 11 참조
""")


if __name__ == "__main__":
    main()
