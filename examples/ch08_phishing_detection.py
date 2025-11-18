"""
Chapter 8: Phishing Detection
LLM을 활용한 피싱 이메일 탐지 시스템
"""

import os
from dotenv import load_dotenv
import openai
import json

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def detect_phishing_llm(email_content: dict) -> dict:
    """LLM을 사용한 피싱 탐지"""

    email_text = f"""
Subject: {email_content.get('subject', 'N/A')}
From: {email_content.get('from', 'N/A')}
To: {email_content.get('to', 'N/A')}
Date: {email_content.get('date', 'N/A')}

Body:
{email_content.get('body', '')}

Links: {email_content.get('links', [])}
Attachments: {email_content.get('attachments', [])}
"""

    prompt = f"""Analyze this email for phishing indicators:

{email_text}

Provide detailed analysis:

1. **Risk Assessment**
   - Overall Risk Level: Safe / Suspicious / Likely Phishing / Definite Phishing
   - Confidence Score: 0-100%

2. **Suspicious Indicators Found**
   - Sender authenticity issues
   - Urgency/pressure tactics
   - Suspicious links or attachments
   - Grammar/spelling (if LLM-generated, may be perfect)
   - Requests for sensitive information
   - Spoofing attempts
   - Other red flags

3. **Detailed Analysis**
   - What makes this suspicious?
   - Comparison to legitimate emails
   - Potential attack goals

4. **Recommended Actions**
   - Immediate steps
   - Verification methods
   - Reporting procedures

5. **Technical Indicators** (if applicable)
   - Email header analysis suggestions
   - Link/domain checks needed
   - Attachment warnings

Format as structured output."""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[
            {
                "role": "system",
                "content": "You are an expert cybersecurity analyst specializing in phishing detection. Provide thorough, actionable analysis."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "email": email_content,
        "analysis": response.choices[0].message.content
    }


def batch_phishing_analysis(emails: list) -> list:
    """여러 이메일을 배치로 분석"""

    results = []
    for email in emails:
        result = detect_phishing_llm(email)
        results.append(result)

    return results


def main():
    """메인 함수"""
    print("\n🛡️ Chapter 8: Phishing Detection System\n")

    # 테스트 이메일 샘플
    test_emails = [
        # Sample 1: Classic Phishing
        {
            "subject": "URGENT: Verify Your Account Within 24 Hours",
            "from": "security@paypa1-verify.com",
            "to": "user@company.com",
            "date": "2024-01-15 03:22:45",
            "body": """Dear Valued Customer,

We have detected unusual activity on your account. For your security, your account has been temporarily suspended.

To restore access, please verify your identity immediately by clicking the link below:

http://paypal-verify-secure.tk/login

Failure to verify within 24 hours will result in permanent account closure.

Thank you for your immediate attention to this matter.

PayPal Security Team
""",
            "links": ["http://paypal-verify-secure.tk/login"],
            "attachments": []
        },

        # Sample 2: Spear Phishing
        {
            "subject": "Re: Q4 Budget Review - Updated Spreadsheet",
            "from": "cfo@company.com",
            "to": "finance-team@company.com",
            "date": "2024-01-15 14:30:22",
            "body": """Hi Team,

I've updated the Q4 budget spreadsheet based on our meeting yesterday.

Please review the attached file and provide your feedback by end of day.

The password to open the file is: Budget2024

Best regards,
Sarah Chen
CFO
""",
            "links": [],
            "attachments": ["Q4_Budget_Final_v2.xlsx.exe"]
        },

        # Sample 3: Legitimate Email
        {
            "subject": "Your AWS Monthly Bill is Ready",
            "from": "no-reply@email.aws.com",
            "to": "billing@company.com",
            "date": "2024-01-15 09:00:00",
            "body": """Hello,

Your AWS monthly billing statement for December 2023 is now available.

Account: 1234-5678-9012
Amount: $1,247.83

To view your bill, sign in to your AWS account at https://aws.amazon.com

Best regards,
Amazon Web Services
""",
            "links": ["https://aws.amazon.com"],
            "attachments": []
        },

        # Sample 4: CEO Fraud
        {
            "subject": "Urgent Wire Transfer Needed",
            "from": "john.smith@company.com",
            "to": "finance@company.com",
            "date": "2024-01-15 16:45:11",
            "body": """Hi,

I'm in a meeting with our acquisition target and we need to send a wire transfer immediately to secure the deal.

Amount: $50,000
Account details:
Bank: International Trust Bank
Account: 9876543210
Swift: ITBKUS33

This is time-sensitive. Please process this immediately and confirm when done.

Thanks,
John Smith
CEO

Sent from my iPhone
""",
            "links": [],
            "attachments": []
        },

        # Sample 5: LLM-Generated Sophisticated Phishing
        {
            "subject": "IT Security: Mandatory Multi-Factor Authentication Update",
            "from": "it-security@company.com",
            "to": "all-employees@company.com",
            "date": "2024-01-15 11:20:33",
            "body": """Dear Colleagues,

As part of our ongoing commitment to cybersecurity excellence, we are implementing an enhanced multi-factor authentication system across all corporate applications.

Action Required:
All employees must register their devices with the new authentication system by January 20, 2024.

Registration Process:
1. Visit: https://company-mfa-registration.com
2. Enter your corporate credentials
3. Follow the step-by-step setup wizard
4. Verify your mobile device

This upgrade is mandatory and complies with our updated Information Security Policy (ISP-2024-01). Accounts that are not registered by the deadline will be temporarily disabled for security purposes.

For assistance, contact the IT Help Desk at extension 5555 or helpdesk@company.com.

Thank you for your cooperation in maintaining our security posture.

Best regards,
Information Security Team
Company IT Department
""",
            "links": ["https://company-mfa-registration.com"],
            "attachments": []
        },
    ]

    print("="*60)
    print("1. Individual Email Analysis")
    print("="*60)

    for i, email in enumerate(test_emails, 1):
        print(f"\n{'='*60}")
        print(f"Email {i}:")
        print(f"Subject: {email['subject']}")
        print(f"From: {email['from']}")
        print(f"{'='*60}\n")

        result = detect_phishing_llm(email)
        print(result["analysis"])
        print("\n")

    print("\n" + "="*60)
    print("2. Batch Analysis Summary")
    print("="*60)

    batch_results = batch_phishing_analysis(test_emails)

    summary_prompt = f"""Analyze these phishing detection results and provide:

1. Detection accuracy insights
2. Common phishing indicators found
3. False positive/negative risks
4. Recommendations for improving detection

Results:
{json.dumps([{"subject": r["email"]["subject"], "analysis": r["analysis"][:200]} for r in batch_results], indent=2)}
"""

    summary = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": summary_prompt}]
    )

    print(summary.choices[0].message.content)

    print("\n\n" + "="*60)
    print("3. Advanced Detection Features")
    print("="*60)

    advanced_features_prompt = """Design advanced phishing detection features using LLMs:

1. **Behavioral Analysis**
   - Unusual sending patterns
   - Email chain context
   - Communication history

2. **Content Analysis**
   - Sentiment analysis
   - Urgency detection
   - Authority claims
   - LLM-generated content detection

3. **Technical Indicators**
   - Header analysis integration
   - Link reputation checking
   - Domain age and registration
   - SSL certificate validation

4. **Machine Learning Enhancement**
   - Training on confirmed phishing
   - Adaptive threshold adjustment
   - Organization-specific patterns

5. **Integration Points**
   - Email gateway integration
   - SIEM/SOAR integration
   - User reporting workflows
   - Automated response actions

Provide implementation guidance."""

    advanced_features = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": advanced_features_prompt}]
    )

    print(advanced_features.choices[0].message.content)

    print("\n\n" + "="*60)
    print("4. Detection Performance Metrics")
    print("="*60)

    metrics_prompt = """Define key performance metrics for a phishing detection system:

Metrics to cover:
1. True Positive Rate (Sensitivity)
2. False Positive Rate
3. Precision
4. F1 Score
5. Detection Time
6. Mean Time to Detection (MTTD)
7. User Reporting Rate
8. Click-through Rate (in simulations)

For each metric:
- Definition
- Target threshold
- Measurement method
- Improvement strategies

Also discuss balancing security vs. usability."""

    metrics = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": metrics_prompt}]
    )

    print(metrics.choices[0].message.content)

    print("\n\n" + "="*60)
    print("Summary: Building an Effective Phishing Detection System")
    print("="*60)
    print("""
Phishing 탐지 시스템 구축 가이드:

**1. Multi-Layer Defense Strategy**

Layer 1: Email Gateway Filtering
- SPF/DKIM/DMARC validation
- Known malicious sender blocking
- Attachment scanning
- Link reputation checking

Layer 2: Content Analysis (LLM-based)
- Suspicious pattern detection
- Social engineering tactics identification
- Context and intent analysis
- LLM-generated content detection

Layer 3: User-level Protection
- Warning banners on suspicious emails
- Link preview/sanitization
- Delayed delivery for high-risk emails
- One-click reporting

Layer 4: Post-delivery Monitoring
- User reporting analysis
- Incident response automation
- Threat intelligence integration
- Continuous learning

**2. LLM Advantages in Phishing Detection**

✅ Context Understanding
✅ Subtle pattern recognition
✅ Multilingual support
✅ Adaptive to new tactics
✅ Explanation generation

❌ Computational cost
❌ Latency concerns
❌ Potential for adversarial attacks
❌ Requires careful prompt engineering

**3. Hybrid Approach (Recommended)**

1. Traditional filters for obvious threats (fast, cheap)
2. LLM analysis for ambiguous cases (accurate)
3. User education and reporting (human intelligence)
4. Continuous feedback loop (improvement)

**4. Implementation Checklist**

□ Define risk tolerance and SLAs
□ Integrate with email infrastructure
□ Establish baseline metrics
□ Create escalation workflows
□ Train users on reporting
□ Set up monitoring dashboards
□ Plan incident response procedures
□ Schedule regular tuning and review

**5. Emerging Threats**

⚠️ LLM-Generated Phishing:
- Perfect grammar and spelling
- Highly personalized at scale
- Multi-language campaigns
- Context-aware responses

Defense requires:
- AI-powered detection
- Behavioral analysis
- Process-based controls
- Enhanced user training

**Tools & Technologies:**
- Email security gateways (Proofpoint, Mimecast)
- SIEM integration (Splunk, ELK)
- Threat intelligence platforms
- Custom LLM solutions
- User reporting tools

**Success Factors:**
1. Executive sponsorship
2. User participation and trust
3. Rapid response to reports
4. Regular training and testing
5. Metrics-driven improvement
6. Cross-team collaboration

**Related Topics:**
- Chapter 7: Information Leakage (data protection)
- Chapter 11: Social Media Influence Operations
- Chapter 18: Security Awareness Education
- Chapter 24: Red Teaming
""")


if __name__ == "__main__":
    main()
