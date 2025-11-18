"""
Chapter 7: PII (Personally Identifiable Information) Detection
LLM을 활용한 PII 감지 시스템 구현
"""

import os
import re
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def detect_pii_with_llm(text: str) -> dict:
    """LLM을 사용한 PII 감지"""
    prompt = f"""Analyze the following text and identify all Personally Identifiable Information (PII):

Text: {text}

Identify and categorize:
1. Names (full names, first/last names)
2. Email addresses
3. Phone numbers
4. Physical addresses
5. Social Security Numbers (SSN)
6. Credit card numbers
7. Dates of birth
8. IP addresses
9. Account numbers
10. Any other sensitive identifiers

For each PII found, provide:
- Category
- Value (or masked value if sensitive)
- Location in text
- Risk level (Low/Medium/High/Critical)

Format as structured output."""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "text": text,
        "pii_analysis": response.choices[0].message.content
    }


def detect_pii_with_regex(text: str) -> dict:
    """정규표현식을 사용한 PII 감지 (비교용)"""
    patterns = {
        "Email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "Phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
        "Credit Card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "IPv4": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        "Date": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
    }

    findings = {}
    for category, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            findings[category] = matches

    return findings


def redact_pii(text: str, pii_categories: list = None) -> dict:
    """PII 마스킹/삭제"""
    if pii_categories is None:
        pii_categories = ["email", "phone", "ssn", "credit_card", "name"]

    prompt = f"""Redact all PII from this text while maintaining readability:

Text: {text}

Redaction rules:
- Replace emails with [EMAIL]
- Replace phone numbers with [PHONE]
- Replace names with [NAME]
- Replace addresses with [ADDRESS]
- Replace SSNs with [SSN]
- Replace credit cards with [CREDIT_CARD]
- Keep the overall meaning intact

Provide:
1. Redacted text
2. List of redactions made
3. Count of each PII type found"""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "original": text,
        "redacted_output": response.choices[0].message.content
    }


def main():
    """메인 함수"""
    print("\n🔍 Chapter 7: PII Detection 시스템\n")

    # 테스트 샘플 데이터
    test_samples = [
        # Sample 1: Customer Support Email
        """
        Dear Support Team,

        My name is John Doe and I'm having trouble accessing my account.
        My email is john.doe@example.com and my phone number is 555-123-4567.
        My account number is ACC-98765432.

        I live at 123 Main Street, Anytown, CA 90210.
        My date of birth is 01/15/1985 and my SSN is 123-45-6789.

        Please help me reset my password.

        Best regards,
        John
        """,

        # Sample 2: Application Form
        """
        Applicant Information:
        Full Name: Jane Smith
        Email: jane.smith@company.com
        Mobile: (555) 987-6543
        Credit Card: 4532-1234-5678-9010

        Previous Address: 456 Oak Ave, Springfield, IL 62701
        Emergency Contact: Mike Smith, mike.smith@email.com, 555-111-2222
        """,

        # Sample 3: Server Log
        """
        2024-01-15 10:23:45 - User login: alice@techcorp.com from IP 192.168.1.100
        2024-01-15 10:24:12 - API access token: sk-1234567890abcdefghijklmnop
        2024-01-15 10:25:33 - Database query for SSN 987-65-4321
        2024-01-15 10:26:01 - Payment processed: Card ****1234, Amount $99.99
        """,
    ]

    print("="*60)
    print("1. LLM-based PII Detection")
    print("="*60)

    for i, sample in enumerate(test_samples, 1):
        print(f"\n{'='*60}")
        print(f"Sample {i}:")
        print(f"{'='*60}")
        print(sample[:200] + "..." if len(sample) > 200 else sample)

        result = detect_pii_with_llm(sample)
        print(f"\n📊 PII Analysis:")
        print(result["pii_analysis"])

    print("\n\n" + "="*60)
    print("2. Regex-based PII Detection (Comparison)")
    print("="*60)

    for i, sample in enumerate(test_samples, 1):
        print(f"\n{'='*60}")
        print(f"Sample {i} - Regex Detection:")
        print(f"{'='*60}")

        regex_findings = detect_pii_with_regex(sample)
        if regex_findings:
            for category, matches in regex_findings.items():
                print(f"{category}: {matches}")
        else:
            print("No PII detected by regex")

    print("\n\n" + "="*60)
    print("3. PII Redaction")
    print("="*60)

    for i, sample in enumerate(test_samples, 1):
        print(f"\n{'='*60}")
        print(f"Sample {i} - Redaction:")
        print(f"{'='*60}")

        redaction_result = redact_pii(sample)
        print(f"\n📝 Redacted Output:")
        print(redaction_result["redacted_output"])

    print("\n\n" + "="*60)
    print("4. Privacy-Preserving Data Sharing")
    print("="*60)

    privacy_scenario = """
    Scenario: A healthcare company wants to share patient data with researchers
    while maintaining HIPAA compliance.

    Original Record:
    Patient: Mary Johnson
    DOB: 03/22/1978
    SSN: 555-44-3333
    Address: 789 Elm St, Boston, MA 02101
    Email: mary.j@email.com
    Phone: 555-333-4444
    Diagnosis: Type 2 Diabetes
    Prescription: Metformin 500mg
    Insurance: BlueCross Policy #BC-123456789
    """

    print(f"\n{privacy_scenario}")

    anonymization_prompt = f"""{privacy_scenario}

Create an anonymized version suitable for research that:
1. Removes all direct identifiers (HIPAA Safe Harbor method)
2. Preserves medical research value
3. Uses generalization where appropriate (e.g., age ranges)
4. Explains each anonymization decision

Provide both the anonymized record and the anonymization report."""

    anonymization = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": anonymization_prompt}]
    )

    print(f"\n🔒 Anonymization Result:")
    print(anonymization.choices[0].message.content)

    print("\n\n" + "="*60)
    print("5. PII Detection Accuracy Comparison")
    print("="*60)

    comparison_prompt = """Compare LLM-based PII detection vs traditional regex/rule-based approaches:

Analyze:
1. Accuracy (false positives, false negatives)
2. Coverage (types of PII detected)
3. Context awareness
4. Performance/speed
5. Maintenance requirements
6. Cost

Provide recommendations for different use cases."""

    comparison = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": comparison_prompt}]
    )

    print(comparison.choices[0].message.content)

    print("\n\n" + "="*60)
    print("Summary: PII Detection Best Practices")
    print("="*60)
    print("""
PII Detection 전략:

**Detection Methods:**

1. **Regex/Pattern Matching**
   ✅ 빠르고 정확한 형식 기반 탐지
   ✅ 낮은 비용
   ❌ 컨텍스트 이해 부족
   ❌ 변형에 취약

2. **Named Entity Recognition (NER)**
   ✅ 이름, 장소 등 엔티티 탐지
   ✅ 컨텍스트 활용
   ❌ 도메인 특화 학습 필요

3. **LLM-based Detection**
   ✅ 높은 컨텍스트 이해
   ✅ 다양한 PII 유형 탐지
   ✅ 유연한 규칙 적용
   ❌ 높은 비용
   ❌ 느린 처리 속도

**Hybrid Approach (권장):**
1. Regex로 1차 스크리닝
2. LLM으로 컨텍스트 분석
3. 사람이 최종 검증

**Compliance Frameworks:**
- GDPR: 개인정보 보호
- HIPAA: 건강 정보 (18개 식별자)
- PCI-DSS: 결제 정보
- CCPA: 캘리포니아 소비자 프라이버시

**Implementation Tips:**
1. 정기적 패턴 업데이트
2. 다층 방어 (detection + redaction + encryption)
3. 감사 로그 유지
4. 인시던트 대응 계획
5. 정기적 테스팅

**Tools & Libraries:**
- Microsoft Presidio (PII detection/anonymization)
- AWS Comprehend (PII detection)
- Google DLP API
- spaCy NER
- Custom LLM solutions
""")


if __name__ == "__main__":
    main()
