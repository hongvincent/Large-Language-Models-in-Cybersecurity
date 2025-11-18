"""
Chapter 2: Few-shot Learning 실습
예제를 통한 LLM의 작업 학습
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def zero_shot(task_description: str, test_input: str) -> str:
    """Zero-shot: 예제 없이 작업 수행"""
    prompt = f"""{task_description}

Input: {test_input}
Output:"""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def few_shot(task_description: str, examples: list, test_input: str) -> str:
    """Few-shot: 예제와 함께 작업 수행"""
    prompt = f"""{task_description}

Here are some examples:

"""

    for i, (input_ex, output_ex) in enumerate(examples, 1):
        prompt += f"Example {i}:\nInput: {input_ex}\nOutput: {output_ex}\n\n"

    prompt += f"Now complete this:\nInput: {test_input}\nOutput:"

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def main():
    """메인 함수"""
    print("\n🎯 Chapter 2: Few-shot Learning 실습\n")

    print("="*60)
    print("Task 1: Security Incident Classification")
    print("="*60)

    task1_description = "Classify security incidents into categories: Phishing, Malware, Intrusion, Data Leak, or Other."

    task1_examples = [
        ("User received email asking to verify account credentials", "Phishing"),
        ("Ransomware encrypted files on file server", "Malware"),
        ("Unauthorized access from foreign IP address", "Intrusion"),
        ("Employee accidentally shared customer database on public cloud", "Data Leak"),
        ("DDoS attack on web server", "Other"),
    ]

    task1_tests = [
        "Suspicious email with link to fake login page",
        "Keylogger detected on CFO's laptop",
        "Failed SSH login attempts from multiple IPs",
        "API keys found in public GitHub repository",
    ]

    print("\n--- Zero-shot Performance ---")
    for test in task1_tests:
        print(f"\nInput: {test}")
        print(f"Output: {zero_shot(task1_description, test)}")

    print("\n--- Few-shot Performance ---")
    for test in task1_tests:
        print(f"\nInput: {test}")
        print(f"Output: {few_shot(task1_description, task1_examples, test)}")

    print("\n\n" + "="*60)
    print("Task 2: CVE Severity Assessment")
    print("="*60)

    task2_description = "Assess the severity of vulnerabilities as: Critical, High, Medium, or Low. Include brief reasoning."

    task2_examples = [
        (
            "Remote code execution in authentication module",
            "Critical - Allows attackers to execute arbitrary code without authentication"
        ),
        (
            "SQL injection in admin panel",
            "High - Allows unauthorized database access but requires admin panel access"
        ),
        (
            "XSS in comment section",
            "Medium - Can steal user sessions but requires user interaction"
        ),
        (
            "Information disclosure in error messages",
            "Low - Reveals some system info but not directly exploitable"
        ),
    ]

    task2_tests = [
        "Buffer overflow in network service allowing remote shell access",
        "CSRF vulnerability in password change function",
        "Outdated SSL/TLS configuration",
    ]

    print("\n--- Zero-shot ---")
    for test in task2_tests:
        print(f"\nVulnerability: {test}")
        print(f"Assessment: {zero_shot(task2_description, test)}")

    print("\n--- Few-shot ---")
    for test in task2_tests:
        print(f"\nVulnerability: {test}")
        print(f"Assessment: {few_shot(task2_description, task2_examples, test)}")

    print("\n\n" + "="*60)
    print("Task 3: Security Log Parsing")
    print("="*60)

    task3_description = "Extract key information from security logs in JSON format."

    task3_examples = [
        (
            "2024-01-15 10:23:45 Failed login attempt for user 'admin' from IP 192.168.1.100",
            '{"timestamp": "2024-01-15 10:23:45", "event": "failed_login", "user": "admin", "ip": "192.168.1.100"}'
        ),
        (
            "2024-01-15 11:30:22 Port scan detected from 203.0.113.45 targeting ports 22,80,443",
            '{"timestamp": "2024-01-15 11:30:22", "event": "port_scan", "source_ip": "203.0.113.45", "target_ports": [22, 80, 443]}'
        ),
        (
            "2024-01-15 14:05:33 Malware signature detected: Trojan.Win32.Generic in file report.pdf",
            '{"timestamp": "2024-01-15 14:05:33", "event": "malware_detected", "signature": "Trojan.Win32.Generic", "file": "report.pdf"}'
        ),
    ]

    task3_tests = [
        "2024-01-16 09:15:44 SQL injection attempt detected in parameter 'id' from IP 198.51.100.23",
        "2024-01-16 10:42:11 Successful privilege escalation for user 'bob' to root access",
        "2024-01-16 12:33:09 Firewall blocked connection from 203.0.113.77 to port 3389",
    ]

    print("\n--- Zero-shot ---")
    for test in task3_tests:
        print(f"\nLog: {test}")
        print(f"Parsed: {zero_shot(task3_description, test)}")

    print("\n--- Few-shot ---")
    for test in task3_tests:
        print(f"\nLog: {test}")
        print(f"Parsed: {few_shot(task3_description, task3_examples, test)}")

    print("\n\n" + "="*60)
    print("Task 4: Security Control Recommendations")
    print("="*60)

    task4_description = "Given a security scenario, recommend appropriate security controls following the format: [Control Type] - [Specific Control] - [Rationale]"

    task4_examples = [
        (
            "Web application vulnerable to SQL injection",
            "Technical - Parameterized Queries - Prevents SQL code injection by separating SQL logic from data\nTechnical - Input Validation - Blocks malicious input patterns at application boundary\nProcess - Security Code Review - Identifies similar vulnerabilities before deployment"
        ),
        (
            "Employees falling for phishing emails",
            "Administrative - Security Awareness Training - Educates users to recognize phishing attempts\nTechnical - Email Filtering - Blocks known phishing domains and suspicious emails\nTechnical - Multi-Factor Authentication - Limits damage if credentials are compromised"
        ),
    ]

    task4_tests = [
        "Production server has unnecessary services running",
        "No audit logging on critical systems",
        "Developers have admin access to production databases",
    ]

    print("\n--- Zero-shot ---")
    for test in task4_tests:
        print(f"\nScenario: {test}")
        print(f"Controls:\n{zero_shot(task4_description, test)}\n")

    print("\n--- Few-shot ---")
    for test in task4_tests:
        print(f"\nScenario: {test}")
        print(f"Controls:\n{few_shot(task4_description, task4_examples, test)}\n")

    print("\n" + "="*60)
    print("Summary: Few-shot Learning for Security Tasks")
    print("="*60)
    print("""
Few-shot Learning의 이점:

**1. 작업 특화 (Task Specialization)**
   - 도메인 특화 분류
   - 일관된 출력 형식
   - 특정 스타일 학습

**2. 정확도 향상**
   - Zero-shot 대비 더 정확한 결과
   - 미묘한 패턴 학습
   - 컨텍스트 이해 향상

**3. 출력 형식 제어**
   - JSON, XML 등 구조화된 형식
   - 템플릿 기반 응답
   - 일관된 포맷

**보안 응용 사례:**
- 로그 분석 및 파싱
- 위협 분류 및 우선순위 지정
- 취약점 평가
- 보안 제어 매핑
- 인시던트 분류

**Few-shot vs Fine-tuning:**
- Few-shot: 즉시 사용 가능, 예제만으로 작동
- Fine-tuning: 더 높은 정확도, 하지만 훈련 필요

**Best Practices:**
1. 다양한 예제 제공 (edge cases 포함)
2. 예제 품질이 중요 (정확하고 대표적)
3. 3-5개 예제가 일반적으로 충분
4. 예제 순서도 영향을 미침
5. 복잡한 작업은 Chain-of-Thought 추가

**다음 단계:**
- Chapter 6: Tasks for LLMs and Their Evaluation
- 더 복잡한 작업은 Fine-tuning 고려
""")


if __name__ == "__main__":
    main()
