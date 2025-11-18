"""
Chapter 18: Enhancing Security Awareness and Education for LLMs
LLM을 활용한 보안 교육 컨텐츠 생성
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_security_training_module(topic: str, difficulty: str = "beginner", format: str = "interactive") -> dict:
    """보안 교육 모듈 생성"""

    prompt = f"""Create a comprehensive security awareness training module:

Topic: {topic}
Difficulty Level: {difficulty} (beginner/intermediate/advanced)
Format: {format} (interactive/presentation/hands-on)

Include:

1. **Learning Objectives**
   - What participants will learn
   - Skills they will gain
   - How this applies to their role

2. **Threat Overview**
   - What is this threat?
   - Why does it matter?
   - Real-world impact and examples
   - Current statistics/trends

3. **How It Works**
   - Step-by-step explanation
   - Attack lifecycle
   - Attacker motivations
   - Common variations

4. **Recognition & Detection**
   - Warning signs
   - Red flags
   - How to spot it
   - Common indicators

5. **Prevention & Response**
   - Best practices
   - What to do if encountered
   - Who to contact
   - Reporting procedures

6. **Practical Scenarios**
   - 3-5 realistic scenarios
   - What would you do?
   - Correct responses
   - Learning points

7. **Knowledge Check (Quiz)**
   - 5-10 questions
   - Multiple choice and scenarios
   - Answer key with explanations

8. **Key Takeaways**
   - Summary of main points
   - Action items
   - Resources for more learning

9. **Additional Resources**
   - Links to policies
   - Further reading
   - Tools and references

Make it engaging, practical, and tailored to the difficulty level."""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": "You are an experienced cybersecurity trainer creating engaging educational content. Make complex topics accessible and actionable."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "topic": topic,
        "difficulty": difficulty,
        "format": format,
        "training_module": response.choices[0].message.content
    }


def create_role_specific_training(role: str, topics: list) -> dict:
    """역할별 맞춤 보안 교육"""

    prompt = f"""Create a tailored security training program for: {role}

Topics to cover:
{chr(10).join(f"- {topic}" for topic in topics)}

For this role, design:

1. **Role-Specific Risks**
   - Threats most relevant to this role
   - Why they're targeted
   - Impact on their work

2. **Relevant Security Practices**
   - Daily security habits
   - Tools they should use
   - Processes to follow

3. **Realistic Scenarios**
   - Job-specific attack scenarios
   - How they might encounter threats
   - Practical decision-making exercises

4. **Quick Reference Guide**
   - DO's and DON'Ts
   - Emergency contacts
   - Common questions

5. **Integration with Workflow**
   - How security fits into their daily tasks
   - Time-efficient security practices
   - Minimal disruption approaches

Make it highly relevant and practical for this specific role."""

    response = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "role": role,
        "topics": topics,
        "training_program": response.choices[0].message.content
    }


def main():
    """메인 함수"""
    print("\n🎓 Chapter 18: Security Awareness Training with LLMs\n")

    print("="*60)
    print("1. General Security Training Modules")
    print("="*60)

    # 주요 보안 주제들
    training_topics = [
        ("Phishing Emails", "beginner", "interactive"),
        ("Password Security and MFA", "beginner", "interactive"),
        ("Social Engineering", "intermediate", "interactive"),
        ("Ransomware", "intermediate", "presentation"),
        ("Data Classification and Handling", "beginner", "hands-on"),
        ("Secure Remote Work", "beginner", "interactive"),
    ]

    for topic, difficulty, format_type in training_topics:
        print(f"\n{'='*60}")
        print(f"Module: {topic} ({difficulty})")
        print(f"{'='*60}\n")

        module = generate_security_training_module(topic, difficulty, format_type)
        print(module["training_module"][:800] + "...\n")

    print("\n" + "="*60)
    print("2. Role-Specific Training Programs")
    print("="*60)

    # 역할별 교육 프로그램
    role_programs = [
        {
            "role": "Software Developers",
            "topics": [
                "Secure Coding Practices",
                "Code Review for Security",
                "Dependency Management",
                "API Security",
                "LLM-Generated Code Risks"
            ]
        },
        {
            "role": "Finance Team",
            "topics": [
                "Business Email Compromise (BEC)",
                "Wire Transfer Fraud",
                "Invoice Scams",
                "Financial Data Protection",
                "Regulatory Compliance"
            ]
        },
        {
            "role": "Executive Leadership",
            "topics": [
                "Whaling Attacks",
                "Strategic Decision Security",
                "Third-Party Risk",
                "Incident Response Governance",
                "Security Investment Priorities"
            ]
        },
        {
            "role": "Human Resources",
            "topics": [
                "PII Protection",
                "Recruitment Scams",
                "Employee Onboarding/Offboarding Security",
                "Background Check Data Handling",
                "GDPR/Privacy Compliance"
            ]
        },
    ]

    for program in role_programs:
        print(f"\n{'='*60}")
        print(f"Role: {program['role']}")
        print(f"{'='*60}\n")

        training = create_role_specific_training(program["role"], program["topics"])
        print(training["training_program"][:600] + "...\n")

    print("\n" + "="*60)
    print("3. Interactive Phishing Simulation Generator")
    print("="*60)

    simulation_prompt = """Design an interactive phishing simulation training system:

Components:

1. **Simulation Campaign Structure**
   - Baseline assessment
   - Progressive difficulty levels
   - Frequency and timing
   - Target groups

2. **Email Template Categories**
   - Simple phishing (obvious red flags)
   - Moderate phishing (some red flags)
   - Sophisticated phishing (very realistic)
   - Spear phishing (personalized)

3. **Simulation Metrics**
   - Click-through rate
   - Reporting rate
   - Time to click/report
   - Repeat offenders

4. **Immediate Education**
   - Landing page content for clickers
   - Positive reinforcement for reporters
   - Just-in-time training

5. **Reporting & Analytics**
   - Department-level results
   - Trending analysis
   - Risk scoring
   - Improvement tracking

6. **Integration**
   - HR systems
   - Training platforms
   - SIEM/Security tools
   - Management dashboards

Provide practical implementation guide."""

    simulation = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": simulation_prompt}]
    )

    print(simulation.choices[0].message.content)

    print("\n\n" + "="*60)
    print("4. Gamification in Security Training")
    print("="*60)

    gamification_prompt = """Design a gamified security awareness program:

Elements to include:

1. **Game Mechanics**
   - Points and scoring
   - Badges and achievements
   - Leaderboards
   - Challenges and quests
   - Team competitions

2. **Learning Pathways**
   - Beginner to expert progression
   - Specialized tracks
   - Certification levels
   - Continuing education

3. **Engagement Features**
   - Daily challenges
   - Monthly tournaments
   - Surprise scenarios
   - Peer learning

4. **Reward System**
   - Virtual rewards
   - Real-world incentives
   - Recognition programs
   - Career development ties

5. **Assessment Integration**
   - Skills verification
   - Knowledge retention
   - Behavioral change metrics
   - Long-term impact

Provide creative, engaging design."""

    gamification = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": gamification_prompt}]
    )

    print(gamification.choices[0].message.content)

    print("\n\n" + "="*60)
    print("5. Measuring Training Effectiveness")
    print("="*60)

    metrics_prompt = """Define comprehensive metrics for security awareness training:

Framework should include:

1. **Kirkpatrick's Four Levels**
   Level 1: Reaction (Did they like it?)
   Level 2: Learning (Did they learn?)
   Level 3: Behavior (Do they apply it?)
   Level 4: Results (Does it reduce risk?)

2. **Leading Indicators**
   - Training completion rates
   - Assessment scores
   - Simulation performance
   - Engagement metrics

3. **Lagging Indicators**
   - Security incidents
   - User-reported threats
   - Policy violations
   - Audit findings

4. **Behavioral Metrics**
   - Password hygiene
   - MFA adoption
   - Software updates
   - Secure communication use

5. **ROI Calculation**
   - Training costs
   - Incident reduction
   - Time saved
   - Risk mitigation value

6. **Continuous Improvement**
   - Feedback collection
   - A/B testing
   - Content iteration
   - Program evolution

Provide practical measurement approach."""

    metrics = client.chat.completions.create(
        model="gpt-5.1-chat-latest",
        messages=[{"role": "user", "content": metrics_prompt}]
    )

    print(metrics.choices[0].message.content)

    print("\n\n" + "="*60)
    print("Summary: Building Effective Security Awareness Programs")
    print("="*60)
    print("""
Security Awareness Training Best Practices:

**1. Program Structure**

Foundation:
- Baseline assessment
- Risk-based prioritization
- Role-specific content
- Multiple delivery formats
- Regular reinforcement

Content Principles:
- Relevant to daily work
- Practical and actionable
- Engaging and interactive
- Culturally appropriate
- Language-accessible

**2. Training Methods**

Traditional:
- Classroom training
- E-learning modules
- Videos and presentations
- Posters and emails
- Newsletters

Modern:
- Microlearning (bite-sized)
- Gamification
- Simulations
- Social learning
- Mobile-first
- LLM-powered personalization

**3. Engagement Strategies**

✅ Make it relevant
✅ Tell stories
✅ Use real examples
✅ Keep it short
✅ Make it interactive
✅ Provide feedback
✅ Celebrate success

❌ Death by PowerPoint
❌ Technical jargon overload
❌ Fear-based messaging only
❌ One-size-fits-all
❌ Set-and-forget

**4. LLM Advantages**

Personalization at Scale:
- Role-specific scenarios
- Language translation
- Difficulty adaptation
- Learning pace adjustment

Content Generation:
- Fresh, relevant examples
- Diverse scenarios
- Updated threat intelligence
- Interactive dialogues

Assessment:
- Automated scoring
- Detailed feedback
- Adaptive questioning
- Progress tracking

**5. Program Components**

Mandatory Annual Training:
- Core security concepts
- Policy updates
- Compliance requirements
- Certification/attestation

Ongoing Reinforcement:
- Monthly awareness campaigns
- Phishing simulations
- Security tips and reminders
- Incident lessons learned

Specialized Training:
- New hire onboarding
- Role changes
- New system rollouts
- Incident response

**6. Success Metrics**

Participation:
- > 95% completion rate
- High engagement scores
- Active participation

Learning:
- > 80% pass rate on assessments
- Knowledge retention over time
- Skill demonstration

Behavior:
- Increased threat reporting
- Reduced click rates in simulations
- Better password hygiene
- Policy compliance

Business Impact:
- Reduced incidents
- Faster detection
- Lower risk exposure
- Cost savings

**7. Common Pitfalls**

❌ Training as checkbox compliance
❌ Boring or irrelevant content
❌ No executive sponsorship
❌ Punitive approach
❌ Ignoring feedback
❌ No measurement
❌ Inconsistent messaging

**8. Implementation Roadmap**

Month 1-2: Foundation
□ Assess current state
□ Define objectives
□ Secure budget/resources
□ Build core content

Month 3-4: Launch
□ Executive kickoff
□ Baseline training rollout
□ Initial simulations
□ Feedback collection

Month 5-6: Optimization
□ Analyze metrics
□ Refine content
□ Expand coverage
□ Increase engagement

Ongoing: Maturation
□ Continuous content updates
□ Advanced topics
□ Specialized training
□ Culture transformation

**9. Tools & Platforms**

Learning Management Systems:
- KnowBe4
- Proofpoint Security Awareness
- Infosec IQ
- SANS Security Awareness

Phishing Simulation:
- GoPhish (open source)
- Cofense PhishMe
- Terranova Security

Custom Solutions:
- LLM-powered platforms
- Internal development
- Integrated SIEM/SOAR

**10. Culture Building**

Security Champions Program:
- Peer advocates
- Department liaisons
- Early adopters
- Feedback providers

Recognition:
- Spotlight good behavior
- Celebrate reporters
- Reward improvement
- Share success stories

Communication:
- Regular updates
- Transparent incidents
- Learning opportunities
- Open dialogue

**Resources:**
- NIST Cybersecurity Framework
- SANS Security Awareness Roadmap
- ENISA Training Materials
- OWASP Security Culture

**Next Steps:**
- Chapter 24: Red Teaming (testing effectiveness)
- Advanced LLM-powered training platforms
- Behavioral security analytics
""")


if __name__ == "__main__":
    main()
