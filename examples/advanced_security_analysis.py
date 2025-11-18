"""
Advanced Security Analysis with GPT-5.1 Reasoning
GPT-5.1의 향상된 추론 능력을 활용한 심층 보안 분석
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def deep_security_analysis(system_description: str, code: str = None) -> dict:
    """GPT-5.1 Thinking 모드로 심층 보안 분석"""

    analysis_prompt = f"""Perform a comprehensive, deep security analysis:

System Description:
{system_description}

{f"Code:{chr(10)}```{chr(10)}{code}{chr(10)}```" if code else ""}

Conduct thorough analysis covering:

1. **Threat Modeling**
   - Identify all potential threat actors
   - Map attack surfaces
   - Analyze attack vectors
   - Assess threat likelihood and impact

2. **Architectural Security Review**
   - Component security posture
   - Trust boundaries
   - Data flows
   - Integration points
   - Single points of failure

3. **Deep Vulnerability Assessment**
   - Code-level vulnerabilities
   - Design flaws
   - Configuration issues
   - Dependencies risks
   - Zero-day potential

4. **Attack Scenario Planning**
   - Realistic attack chains
   - Multi-stage attacks
   - Persistence mechanisms
   - Lateral movement possibilities
   - Data exfiltration paths

5. **Defense-in-Depth Analysis**
   - Current controls evaluation
   - Coverage gaps
   - Control effectiveness
   - Compensating controls
   - Recommended improvements

6. **Compliance & Standards**
   - OWASP ASVS
   - NIST Cybersecurity Framework
   - ISO 27001
   - Industry-specific requirements

7. **Prioritized Recommendations**
   - Critical fixes (immediate)
   - High priority (< 30 days)
   - Medium priority (< 90 days)
   - Long-term improvements

Think deeply and reason through each aspect systematically."""

    # Use GPT-5.1 Thinking mode for deeper reasoning
    response = client.chat.completions.create(
        model="gpt-5.1-thinking",  # Reasoning mode
        messages=[
            {
                "role": "system",
                "content": "You are a senior security architect with 20+ years of experience in application security, threat modeling, and security architecture. Think deeply and systematically about all aspects."
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ]
    )

    return {
        "system": system_description,
        "analysis": response.choices[0].message.content
    }


def comparative_security_analysis(scenario: str, approaches: list) -> dict:
    """여러 보안 접근법을 비교 분석"""

    comparison_prompt = f"""Scenario: {scenario}

Compare these security approaches:
{chr(10).join(f"{i+1}. {approach}" for i, approach in enumerate(approaches))}

For each approach, analyze:

1. **Security Effectiveness**
   - Threat coverage
   - Attack prevention
   - Detection capabilities
   - Response effectiveness

2. **Implementation Complexity**
   - Technical difficulty
   - Resource requirements
   - Time to implement
   - Maintenance burden

3. **Performance Impact**
   - Latency
   - Throughput
   - Resource usage
   - Scalability

4. **Cost Analysis**
   - Initial investment
   - Operational costs
   - ROI potential
   - TCO over 3 years

5. **Trade-offs**
   - Security vs usability
   - Cost vs benefit
   - Complexity vs effectiveness

6. **Recommendation**
   - Best approach for different contexts
   - Hybrid strategies
   - Phased implementation

Provide detailed, reasoned comparison."""

    response = client.chat.completions.create(
        model="gpt-5.1-thinking",
        messages=[{"role": "user", "content": comparison_prompt}]
    )

    return {
        "scenario": scenario,
        "approaches": approaches,
        "comparison": response.choices[0].message.content
    }


def main():
    """메인 함수"""
    print("\n🧠 Advanced Security Analysis with GPT-5.1 Reasoning\n")

    print("="*60)
    print("1. Deep Security Analysis - Microservices Architecture")
    print("="*60)

    microservices_system = """
E-commerce Platform Architecture:

Components:
- API Gateway (Kong)
- User Service (Node.js)
- Product Service (Python/Django)
- Order Service (Java/Spring Boot)
- Payment Service (Go)
- Notification Service (Python/Flask)
- Database: PostgreSQL (per service)
- Cache: Redis
- Message Queue: RabbitMQ
- Service Mesh: Istio

Authentication: JWT tokens
Authorization: RBAC with Keycloak
Communication: REST + gRPC
Deployment: Kubernetes on AWS

External Integrations:
- Payment gateways (Stripe, PayPal)
- Shipping APIs
- Email service (SendGrid)
- SMS service (Twilio)
- Analytics (Google Analytics)
"""

    print("\nAnalyzing microservices architecture...\n")

    analysis1 = deep_security_analysis(microservices_system)
    print(analysis1["analysis"])

    print("\n\n" + "="*60)
    print("2. Deep Code Security Analysis")
    print("="*60)

    blockchain_code = """
pragma solidity ^0.8.0;

contract TokenSale {
    address public owner;
    mapping(address => uint256) public balances;
    uint256 public tokenPrice = 0.001 ether;
    uint256 public tokensSold;

    constructor() {
        owner = msg.sender;
    }

    function buyTokens(uint256 _numberOfTokens) public payable {
        require(msg.value == _numberOfTokens * tokenPrice);

        balances[msg.sender] += _numberOfTokens;
        tokensSold += _numberOfTokens;
    }

    function withdraw() public {
        require(msg.sender == owner);
        payable(owner).transfer(address(this).balance);
    }

    function getRefund() public {
        uint256 amount = balances[msg.sender] * tokenPrice;
        balances[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }

    function transfer(address _to, uint256 _value) public {
        require(balances[msg.sender] >= _value);
        balances[msg.sender] -= _value;
        balances[_to] += _value;
    }
}
"""

    code_description = """
Solidity Smart Contract: Token Sale

Purpose: Allow users to purchase tokens with ETH
Features: Buy tokens, get refunds, transfer tokens, owner withdrawal
Deployment: Ethereum mainnet
"""

    print("\nAnalyzing smart contract security...\n")

    analysis2 = deep_security_analysis(code_description, blockchain_code)
    print(analysis2["analysis"])

    print("\n\n" + "="*60)
    print("3. Comparative Analysis - Authentication Methods")
    print("="*60)

    auth_scenario = """
Web application requires user authentication.
User base: 100,000+ users
Compliance: PCI-DSS, SOC 2
Mobile app: Yes
API access: Yes
"""

    auth_approaches = [
        "Session-based authentication with cookies",
        "JWT tokens (stateless)",
        "OAuth 2.0 with external providers",
        "Passwordless (Magic links + WebAuthn)",
        "Multi-factor with TOTP",
    ]

    print("\nComparing authentication approaches...\n")

    comparison1 = comparative_security_analysis(auth_scenario, auth_approaches)
    print(comparison1["comparison"])

    print("\n\n" + "="*60)
    print("4. Comparative Analysis - API Security")
    print("="*60)

    api_scenario = """
Public REST API for mobile banking app
Features: Account info, transactions, transfers, bill pay
Users: 500,000+ active users
Transactions: 1M+ daily
Regulatory: Financial regulations, PSD2
"""

    api_approaches = [
        "API Keys only",
        "OAuth 2.0 Client Credentials",
        "mTLS (Mutual TLS)",
        "API Gateway + Rate Limiting + WAF",
        "Zero Trust with service mesh + attestation",
    ]

    print("\nComparing API security approaches...\n")

    comparison2 = comparative_security_analysis(api_scenario, api_approaches)
    print(comparison2["comparison"])

    print("\n\n" + "="*60)
    print("5. Incident Response Plan Analysis")
    print("="*60)

    ir_prompt = """Analyze and improve this incident response plan:

Current Plan:
1. Detection: SIEM alerts trigger ticket
2. Triage: SOC analyst reviews
3. Escalation: If critical, escalate to IR team
4. Investigation: IR team investigates
5. Containment: Isolate affected systems
6. Eradication: Remove threat
7. Recovery: Restore systems
8. Lessons Learned: Post-mortem meeting

Provide:
1. Gap analysis
2. Detailed improvements
3. Playbooks for common scenarios
4. Automation opportunities
5. Metrics and KPIs
6. Training requirements

Think deeply about all scenarios and edge cases."""

    ir_analysis = client.chat.completions.create(
        model="gpt-5.1-thinking",
        messages=[{"role": "user", "content": ir_prompt}]
    )

    print(ir_analysis.choices[0].message.content)

    print("\n\n" + "="*60)
    print("6. Zero Trust Architecture Design")
    print("="*60)

    zt_prompt = """Design a comprehensive Zero Trust Architecture for:

Organization:
- 5,000 employees
- Global offices (US, EU, APAC)
- Cloud-first (AWS, Azure)
- SaaS applications (50+)
- Legacy on-prem systems (some)
- BYOD policy
- Remote work majority

Requirements:
- Strong authentication
- Micro-segmentation
- Continuous verification
- Least privilege access
- Comprehensive logging
- Incident response integration

Provide:
1. Architecture design
2. Implementation phases
3. Technology selection
4. Migration strategy
5. Security controls mapping
6. Metrics and success criteria

Use deep reasoning to consider all aspects and dependencies."""

    zt_design = client.chat.completions.create(
        model="gpt-5.1-thinking",
        messages=[{"role": "user", "content": zt_prompt}]
    )

    print(zt_design.choices[0].message.content)

    print("\n\n" + "="*60)
    print("Summary: Advanced Security Analysis Benefits")
    print("="*60)
    print("""
GPT-5.1 Reasoning 모드의 이점:

**1. 향상된 추론 능력**

Depth:
- 다층적 분석
- 연쇄적 사고
- 근본 원인 파악
- 간접적 영향 고려

Breadth:
- 종합적 관점
- 다양한 시나리오
- 상호 의존성 파악
- 전체 맥락 이해

**2. 실용적 활용 사례**

Threat Modeling:
- 공격 시나리오 상세 분석
- 공격 체인 구성
- 방어 전략 수립

Architecture Review:
- 설계 결함 발견
- 개선 제안
- 대안 비교

Incident Analysis:
- 근본 원인 분석
- 영향 평가
- 재발 방지

**3. 분석 품질 향상**

Accuracy:
- 더 정확한 취약점 식별
- 오탐 감소
- 미탐 감소

Completeness:
- 포괄적 커버리지
- Edge case 고려
- 복합적 시나리오

Actionability:
- 구체적 권장사항
- 우선순위화
- 실행 가능한 단계

**4. Best Practices**

Prompting:
- 명확한 컨텍스트 제공
- 구체적 질문
- 다단계 추론 요청
- 예제 포함

Validation:
- 다중 관점 확인
- 전문가 검증
- 실제 테스트
- 문서화

Integration:
- 기존 프로세스 통합
- 도구 연계
- 자동화
- 지속적 개선

**5. 한계 인식**

주의사항:
- 모델의 한계 이해
- 블라인드 신뢰 금지
- 인간 전문가 검증 필수
- 특정 도메인 지식 부족 가능

보완 방법:
- 전문가 리뷰
- 자동화 도구 병행
- 지속적 학습
- 피드백 루프

**Resources:**
- GPT-5.1 Documentation
- Security Architecture Patterns
- Threat Modeling Methodologies
- Zero Trust Frameworks
""")


if __name__ == "__main__":
    main()
