# LLM Agents for Cybersecurity - 고급 실습 가이드

## 📚 개요

이 가이드는 LLM Agent 시스템을 활용한 고급 사이버보안 실습을 다룹니다. Chapter 2 "Adapting LLMs to Downstream Applications"와 Chapter 4 "Conversational Agents"의 내용을 기반으로 실전 Agent를 구현합니다.

## 🎯 학습 목표

- Multi-agent LLM 시스템 설계 및 구현
- Actor-Agent 패턴 이해 및 활용
- Tool Integration을 통한 확장된 기능 구현
- 자율 보안 테스팅 Agent 개발
- Collaborative Defense Agent 시스템 구축

## 🏗️ Agent 아키텍처 개념

### Agent의 기본 구성 요소

1. **Perception**: 환경 인식 (입력 처리)
2. **Reasoning**: 추론 및 계획 (LLM 활용)
3. **Action**: 실행 (도구 사용, 출력 생성)
4. **Memory**: 기억 (컨텍스트 유지)

```python
# examples/agents/base_agent.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import openai

class BaseAgent(ABC):
    """기본 Agent 추상 클래스"""

    def __init__(self, name: str, role: str, model: str = "gpt-5.1-chat-latest"):
        self.name = name
        self.role = role
        self.model = model
        self.client = openai.OpenAI()
        self.memory: List[Dict[str, str]] = []

    def perceive(self, input_data: str) -> str:
        """환경 인식 - 입력 데이터 처리"""
        return input_data

    @abstractmethod
    def reason(self, perception: str) -> str:
        """추론 - LLM을 사용한 의사결정"""
        pass

    @abstractmethod
    def act(self, reasoning_result: str) -> Any:
        """행동 - 실제 작업 수행"""
        pass

    def remember(self, role: str, content: str):
        """메모리에 저장"""
        self.memory.append({"role": role, "content": content})

    def recall(self, limit: int = 10) -> List[Dict[str, str]]:
        """메모리에서 회상"""
        return self.memory[-limit:]

    def run(self, input_data: str) -> Any:
        """Agent 실행 파이프라인"""
        perception = self.perceive(input_data)
        reasoning = self.reason(perception)
        result = self.act(reasoning)
        return result
```

## 🤖 Chapter 4: Conversational Agents 실습

### 실습 4.1: 보안 상담 Agent

```python
# examples/agents/security_advisor_agent.py

class SecurityAdvisorAgent(BaseAgent):
    """보안 상담 Agent"""

    def __init__(self):
        super().__init__(
            name="SecurityAdvisor",
            role="Cybersecurity consultant providing expert advice"
        )
        self.system_prompt = """
        You are a senior cybersecurity consultant with expertise in:
        - Threat analysis and risk assessment
        - Security architecture design
        - Incident response
        - Compliance (GDPR, HIPAA, PCI-DSS)

        Provide detailed, actionable advice with:
        1. Clear explanations
        2. Risk levels
        3. Specific recommendations
        4. Implementation steps
        """

    def reason(self, perception: str) -> str:
        """보안 문제 분석 및 조언 생성"""
        self.remember("user", perception)

        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.recall()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        advice = response.choices[0].message.content
        self.remember("assistant", advice)

        return advice

    def act(self, reasoning_result: str) -> str:
        """조언 반환"""
        return reasoning_result

# 사용 예제
advisor = SecurityAdvisorAgent()

conversation = [
    "We're planning to migrate our database to the cloud. What security considerations should we have?",
    "What about data encryption?",
    "How should we handle access control?"
]

for question in conversation:
    print(f"\n{'='*60}")
    print(f"User: {question}")
    print(f"{'='*60}")
    response = advisor.run(question)
    print(f"Advisor: {response}")
```

### 실습 4.2: Interactive Red Team Agent

```python
# examples/agents/red_team_agent.py

class RedTeamAgent(BaseAgent):
    """대화형 Red Team Agent"""

    def __init__(self):
        super().__init__(
            name="RedTeamAgent",
            role="Ethical hacker simulating attacks for security testing"
        )
        self.system_prompt = """
        You are a professional red team operator conducting authorized security testing.

        Your responsibilities:
        1. Identify potential vulnerabilities
        2. Simulate realistic attack scenarios
        3. Provide detailed attack chains
        4. Suggest remediation strategies

        Always emphasize:
        - This is authorized testing only
        - Ethical guidelines must be followed
        - Document all findings clearly
        """

    def reason(self, perception: str) -> str:
        """공격 시나리오 분석"""
        self.remember("user", perception)

        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.recall()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )

        analysis = response.choices[0].message.content
        self.remember("assistant", analysis)

        return analysis

    def act(self, reasoning_result: str) -> Dict[str, Any]:
        """공격 계획 및 완화 전략 생성"""
        return {
            "analysis": reasoning_result,
            "timestamp": self._get_timestamp()
        }

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

# 대화형 Red Team 세션
red_team = RedTeamAgent()

target_system = """
Web application details:
- Framework: Django 3.2
- Database: PostgreSQL
- Authentication: JWT tokens
- File upload feature enabled
- Admin panel at /admin
"""

print("=== Red Team Assessment ===")
print(f"Target: {target_system}")

questions = [
    f"Analyze this system for vulnerabilities: {target_system}",
    "What would be your attack chain for gaining admin access?",
    "How could we exploit the file upload feature?",
    "What are the recommended security improvements?"
]

for q in questions:
    result = red_team.run(q)
    print(f"\n{'='*60}")
    print(f"Query: {q}")
    print(f"{'='*60}")
    print(result['analysis'])
```

## 🔧 Chapter 2: Actor-Agent Systems 실습

### 실습 2.1: Multi-Agent Coordinator

```python
# examples/agents/multi_agent_coordinator.py

class AgentCoordinator:
    """Multiple Agent들을 조정하는 Coordinator"""

    def __init__(self):
        self.client = openai.OpenAI()
        self.agents = {}
        self.task_history = []

    def register_agent(self, agent: BaseAgent):
        """Agent 등록"""
        self.agents[agent.name] = agent

    def assign_task(self, task: str) -> str:
        """적절한 Agent에 작업 할당"""
        assignment_prompt = f"""
        Given these available agents and their roles:
        {self._get_agent_descriptions()}

        Task: {task}

        Which agent should handle this task? Respond with only the agent name.
        """

        response = self.client.chat.completions.create(
            model="gpt-5.1-chat-latest",
            messages=[{"role": "user", "content": assignment_prompt}]
        )

        selected_agent = response.choices[0].message.content.strip()

        # Find matching agent
        for agent_name in self.agents.keys():
            if agent_name.lower() in selected_agent.lower():
                return agent_name

        return list(self.agents.keys())[0]  # Fallback

    def _get_agent_descriptions(self) -> str:
        """등록된 Agent들의 설명 반환"""
        descriptions = []
        for name, agent in self.agents.items():
            descriptions.append(f"- {name}: {agent.role}")
        return "\n".join(descriptions)

    def execute_task(self, task: str) -> Dict[str, Any]:
        """작업 실행"""
        agent_name = self.assign_task(task)
        agent = self.agents[agent_name]

        result = agent.run(task)

        task_record = {
            "task": task,
            "assigned_to": agent_name,
            "result": result
        }
        self.task_history.append(task_record)

        return task_record

# Security Operations Center (SOC) Agent 팀 구성
class ThreatAnalystAgent(BaseAgent):
    """위협 분석 전문 Agent"""

    def __init__(self):
        super().__init__(
            name="ThreatAnalyst",
            role="Analyzes security threats and creates detailed reports"
        )

    def reason(self, perception: str) -> str:
        prompt = f"""
        As a threat analyst, analyze this security event:
        {perception}

        Provide:
        1. Threat classification
        2. Severity assessment
        3. Indicators of Compromise (IoCs)
        4. Recommended actions
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def act(self, reasoning_result: str) -> str:
        return reasoning_result


class IncidentResponderAgent(BaseAgent):
    """사고 대응 전문 Agent"""

    def __init__(self):
        super().__init__(
            name="IncidentResponder",
            role="Handles security incidents and provides response procedures"
        )

    def reason(self, perception: str) -> str:
        prompt = f"""
        As an incident responder, create a response plan for:
        {perception}

        Include:
        1. Immediate containment steps
        2. Investigation procedures
        3. Recovery actions
        4. Post-incident activities
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def act(self, reasoning_result: str) -> str:
        return reasoning_result


class ComplianceAuditorAgent(BaseAgent):
    """컴플라이언스 감사 Agent"""

    def __init__(self):
        super().__init__(
            name="ComplianceAuditor",
            role="Audits systems for compliance with security standards"
        )

    def reason(self, perception: str) -> str:
        prompt = f"""
        As a compliance auditor, review:
        {perception}

        Check against:
        - GDPR
        - PCI-DSS
        - SOC 2
        - ISO 27001

        Provide compliance status and gaps.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def act(self, reasoning_result: str) -> str:
        return reasoning_result


# SOC Agent 팀 초기화
coordinator = AgentCoordinator()
coordinator.register_agent(ThreatAnalystAgent())
coordinator.register_agent(IncidentResponderAgent())
coordinator.register_agent(ComplianceAuditorAgent())

# 다양한 보안 작업 실행
tasks = [
    "Suspicious login attempts detected from IP 192.168.1.100 with multiple failed passwords",
    "Ransomware detected on file server. Files are being encrypted.",
    "Review our user authentication system for GDPR compliance"
]

print("=== Multi-Agent SOC Simulation ===\n")
for task in tasks:
    print(f"\n{'='*60}")
    print(f"Task: {task}")
    print(f"{'='*60}")

    result = coordinator.execute_task(task)

    print(f"\nAssigned to: {result['assigned_to']}")
    print(f"\nResult:\n{result['result']}")
```

### 실습 2.2: Self-Guided Agent with Critique

```python
# examples/agents/self_guided_agent.py

class SelfGuidedSecurityAgent(BaseAgent):
    """자기 비판 및 개선 기능을 가진 Agent"""

    def __init__(self):
        super().__init__(
            name="SelfGuidedAgent",
            role="Security agent with self-improvement capabilities"
        )

    def generate_response(self, task: str) -> str:
        """초기 응답 생성"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert."},
                {"role": "user", "content": task}
            ]
        )
        return response.choices[0].message.content

    def critique_response(self, task: str, response: str) -> Dict[str, Any]:
        """자신의 응답 비판"""
        critique_prompt = f"""
        Original task: {task}

        Generated response: {response}

        As a senior security expert, critique this response:
        1. Accuracy: Is the information correct?
        2. Completeness: Is anything missing?
        3. Security: Are there any security concerns?
        4. Clarity: Is it clear and actionable?

        Provide:
        - Overall score (1-10)
        - Issues found
        - Suggestions for improvement
        """

        critique = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": critique_prompt}]
        )

        return {
            "critique": critique.choices[0].message.content,
            "original_response": response
        }

    def improve_response(self, task: str, critique_result: Dict[str, Any]) -> str:
        """비판을 바탕으로 응답 개선"""
        improvement_prompt = f"""
        Original task: {task}

        Initial response: {critique_result['original_response']}

        Critique: {critique_result['critique']}

        Provide an improved response that addresses all the issues raised.
        """

        improved = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": improvement_prompt}]
        )

        return improved.choices[0].message.content

    def reason(self, perception: str) -> str:
        """자기 개선 루프 실행"""
        # 초기 응답 생성
        initial_response = self.generate_response(perception)

        # 자기 비판
        critique = self.critique_response(perception, initial_response)

        # 개선된 응답 생성
        improved_response = self.improve_response(perception, critique)

        return improved_response

    def act(self, reasoning_result: str) -> str:
        return reasoning_result


# 사용 예제
agent = SelfGuidedSecurityAgent()

task = "Design a secure password reset mechanism for a web application"

print("=== Self-Guided Agent with Critique ===\n")
print(f"Task: {task}\n")

result = agent.run(task)
print(f"Final Response:\n{result}")
```

## 🛠️ Tool Integration 실습

### 실습: Tool-Augmented Security Agent

```python
# examples/agents/tool_augmented_agent.py

import subprocess
import json
from typing import List, Callable, Dict, Any

class Tool:
    """Agent가 사용할 수 있는 도구"""

    def __init__(self, name: str, description: str, function: Callable):
        self.name = name
        self.description = description
        self.function = function

    def execute(self, *args, **kwargs):
        """도구 실행"""
        return self.function(*args, **kwargs)


class ToolAugmentedAgent(BaseAgent):
    """도구를 사용할 수 있는 Agent"""

    def __init__(self):
        super().__init__(
            name="ToolAgent",
            role="Security agent with access to various tools"
        )
        self.tools: Dict[str, Tool] = {}

    def register_tool(self, tool: Tool):
        """도구 등록"""
        self.tools[tool.name] = tool

    def get_tool_descriptions(self) -> str:
        """사용 가능한 도구 설명"""
        descriptions = []
        for tool in self.tools.values():
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)

    def select_tool(self, task: str) -> str:
        """작업에 적합한 도구 선택"""
        selection_prompt = f"""
        Available tools:
        {self.get_tool_descriptions()}

        Task: {task}

        Which tool should be used? Respond with only the tool name.
        If no tool is needed, respond with 'NONE'.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": selection_prompt}]
        )

        selected = response.choices[0].message.content.strip()

        for tool_name in self.tools.keys():
            if tool_name.lower() in selected.lower():
                return tool_name

        return "NONE"

    def extract_tool_parameters(self, task: str, tool_name: str) -> Dict[str, Any]:
        """도구 실행에 필요한 파라미터 추출"""
        tool = self.tools[tool_name]

        param_prompt = f"""
        Tool: {tool_name}
        Description: {tool.description}

        Task: {task}

        Extract the parameters needed to use this tool.
        Respond with JSON format only.

        Example: {{"param1": "value1", "param2": "value2"}}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": param_prompt}]
        )

        try:
            # Extract JSON from response
            content = response.choices[0].message.content
            # Find JSON in the response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                return json.loads(json_str)
        except:
            pass

        return {}

    def reason(self, perception: str) -> Dict[str, Any]:
        """도구 사용을 포함한 추론"""
        # 도구 선택
        tool_name = self.select_tool(perception)

        if tool_name == "NONE":
            # 도구 없이 직접 응답
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": perception}]
            )
            return {
                "tool_used": None,
                "tool_output": None,
                "final_response": response.choices[0].message.content
            }

        # 도구 파라미터 추출 및 실행
        params = self.extract_tool_parameters(perception, tool_name)
        tool = self.tools[tool_name]
        tool_output = tool.execute(**params)

        # 도구 출력을 바탕으로 최종 응답 생성
        synthesis_prompt = f"""
        Task: {perception}

        Tool used: {tool_name}
        Tool output: {tool_output}

        Synthesize this information into a comprehensive response.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": synthesis_prompt}]
        )

        return {
            "tool_used": tool_name,
            "tool_output": tool_output,
            "final_response": response.choices[0].message.content
        }

    def act(self, reasoning_result: Dict[str, Any]) -> str:
        return reasoning_result["final_response"]


# 보안 도구 정의
def port_scan_tool(target: str) -> str:
    """포트 스캔 시뮬레이션 (실제로는 nmap 등 사용)"""
    # 실제 구현에서는 실제 스캔 수행
    # 여기서는 시뮬레이션
    return f"""
    Port scan results for {target}:
    - Port 22 (SSH): Open
    - Port 80 (HTTP): Open
    - Port 443 (HTTPS): Open
    - Port 3306 (MySQL): Filtered
    - Port 8080 (HTTP-Alt): Closed
    """

def vulnerability_scan_tool(target: str) -> str:
    """취약점 스캔 시뮬레이션"""
    return f"""
    Vulnerability scan results for {target}:
    - CVE-2024-1234: SQL Injection in login form (High)
    - CVE-2024-5678: XSS in comment section (Medium)
    - CVE-2024-9012: Outdated SSL/TLS configuration (Low)
    """

def whois_lookup_tool(domain: str) -> str:
    """WHOIS 조회 시뮬레이션"""
    return f"""
    WHOIS information for {domain}:
    - Registrar: Example Registrar Inc.
    - Created: 2020-01-01
    - Expires: 2025-01-01
    - Name servers: ns1.example.com, ns2.example.com
    """

def threat_intel_tool(ioc: str) -> str:
    """위협 인텔리전스 조회 시뮬레이션"""
    return f"""
    Threat intelligence for {ioc}:
    - Reputation: Malicious
    - Category: Botnet C2
    - First seen: 2024-01-15
    - Related malware: TrickBot
    - Confidence: High (95%)
    """


# Tool-Augmented Agent 초기화
agent = ToolAugmentedAgent()

# 도구 등록
agent.register_tool(Tool(
    name="port_scanner",
    description="Scans open ports on a target system",
    function=port_scan_tool
))

agent.register_tool(Tool(
    name="vulnerability_scanner",
    description="Scans for known vulnerabilities in a target",
    function=vulnerability_scan_tool
))

agent.register_tool(Tool(
    name="whois_lookup",
    description="Looks up domain registration information",
    function=whois_lookup_tool
))

agent.register_tool(Tool(
    name="threat_intelligence",
    description="Queries threat intelligence databases for IOCs",
    function=threat_intel_tool
))

# 도구를 사용한 보안 분석
tasks = [
    "Scan example.com for open ports and analyze the results",
    "Check if IP address 192.168.1.100 is associated with any known threats",
    "Find out who owns the domain malicious-site.com",
]

print("=== Tool-Augmented Security Agent ===\n")
for task in tasks:
    print(f"\n{'='*60}")
    print(f"Task: {task}")
    print(f"{'='*60}\n")

    result = agent.run(task)
    print(result)
```

## 🔄 Autonomous Security Testing Agent

### 실습: Self-Operating Penetration Testing Agent

```python
# examples/agents/autonomous_pentest_agent.py

class AutonomousPentestAgent(BaseAgent):
    """자율적으로 침투 테스트를 수행하는 Agent"""

    def __init__(self):
        super().__init__(
            name="AutoPentest",
            role="Autonomous penetration testing agent"
        )
        self.findings = []
        self.test_plan = []

    def create_test_plan(self, target_info: str) -> List[str]:
        """테스트 계획 수립"""
        planning_prompt = f"""
        Target information:
        {target_info}

        Create a comprehensive penetration testing plan.
        List the tests in order of execution.
        Each test should be a specific, actionable task.

        Format as a numbered list.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": planning_prompt}]
        )

        plan_text = response.choices[0].message.content

        # 계획을 개별 테스트로 파싱
        tests = []
        for line in plan_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # 번호나 bullet point 제거
                test = line.lstrip('0123456789.-) ')
                if test:
                    tests.append(test)

        self.test_plan = tests
        return tests

    def execute_test(self, test_description: str) -> Dict[str, Any]:
        """개별 테스트 실행"""
        execution_prompt = f"""
        Execute this penetration test:
        {test_description}

        Provide:
        1. Test methodology
        2. Commands/techniques used
        3. Results obtained
        4. Security implications
        5. Recommendations

        This is authorized security testing.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": execution_prompt}]
        )

        result = {
            "test": test_description,
            "results": response.choices[0].message.content,
            "status": "completed"
        }

        self.findings.append(result)
        return result

    def generate_report(self) -> str:
        """최종 보고서 생성"""
        report_prompt = f"""
        Generate a professional penetration testing report based on these findings:

        {json.dumps(self.findings, indent=2)}

        Include:
        1. Executive Summary
        2. Methodology
        3. Detailed Findings
        4. Risk Assessment
        5. Recommendations
        6. Conclusion
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": report_prompt}]
        )

        return response.choices[0].message.content

    def reason(self, perception: str) -> Dict[str, Any]:
        """전체 테스트 프로세스 실행"""
        # 1. 테스트 계획 수립
        print("Creating test plan...")
        test_plan = self.create_test_plan(perception)

        # 2. 각 테스트 실행
        print(f"\nExecuting {len(test_plan)} tests...")
        for i, test in enumerate(test_plan, 1):
            print(f"\n[{i}/{len(test_plan)}] {test}")
            result = self.execute_test(test)

        # 3. 보고서 생성
        print("\nGenerating final report...")
        report = self.generate_report()

        return {
            "test_plan": test_plan,
            "findings": self.findings,
            "report": report
        }

    def act(self, reasoning_result: Dict[str, Any]) -> str:
        return reasoning_result["report"]


# 사용 예제
pentest_agent = AutonomousPentestAgent()

target_system = """
Target System Information:
- Name: E-commerce Web Application
- URL: https://shop.example.com
- Technology Stack: LAMP (Linux, Apache, MySQL, PHP)
- Features:
  * User registration and login
  * Product catalog
  * Shopping cart
  * Payment processing
  * Admin panel
- Known components:
  * WordPress 5.8
  * WooCommerce plugin
  * Custom PHP modules

Authorization: Full penetration testing authorized by client
Scope: Web application only, no DoS attacks
"""

print("=== Autonomous Penetration Testing Agent ===\n")
print("Target:", target_system)
print("\n" + "="*60)

report = pentest_agent.run(target_system)

print("\n=== FINAL PENETRATION TEST REPORT ===\n")
print(report)
```

## 🤝 Collaborative Defense Agent System

### 실습: Multi-Agent Defense System

```python
# examples/agents/collaborative_defense.py

class DefenseCoordinator:
    """방어 Agent들을 조정하는 시스템"""

    def __init__(self):
        self.client = openai.OpenAI()
        self.agents = {}
        self.threat_queue = []
        self.response_log = []

    def register_agent(self, agent: BaseAgent):
        """방어 Agent 등록"""
        self.agents[agent.name] = agent

    def detect_threat(self, event: str) -> Dict[str, Any]:
        """위협 탐지 및 분류"""
        detection_prompt = f"""
        Analyze this security event:
        {event}

        Determine:
        1. Is this a security threat? (YES/NO)
        2. Threat type (if applicable)
        3. Severity (Critical/High/Medium/Low)
        4. Affected systems
        """

        response = self.client.chat.completions.create(
            model="gpt-5.1-chat-latest",
            messages=[{"role": "user", "content": detection_prompt}]
        )

        analysis = response.choices[0].message.content

        threat_info = {
            "event": event,
            "analysis": analysis,
            "is_threat": "YES" in analysis.upper(),
            "timestamp": self._timestamp()
        }

        if threat_info["is_threat"]:
            self.threat_queue.append(threat_info)

        return threat_info

    def coordinate_response(self, threat: Dict[str, Any]) -> Dict[str, Any]:
        """여러 Agent를 조정하여 위협에 대응"""

        # 각 Agent에게 위협 정보 전파
        responses = {}
        for agent_name, agent in self.agents.items():
            print(f"\n[{agent_name}] Analyzing threat...")
            response = agent.run(threat["event"])
            responses[agent_name] = response

        # 응답 통합
        synthesis_prompt = f"""
        Threat: {threat['event']}

        Agent responses:
        {json.dumps(responses, indent=2)}

        Synthesize a coordinated defense strategy that:
        1. Combines insights from all agents
        2. Prioritizes actions
        3. Assigns responsibilities
        4. Provides timeline
        """

        synthesis = self.client.chat.completions.create(
            model="gpt-5.1-chat-latest",
            messages=[{"role": "user", "content": synthesis_prompt}]
        )

        coordinated_response = {
            "threat": threat,
            "individual_responses": responses,
            "coordinated_strategy": synthesis.choices[0].message.content,
            "timestamp": self._timestamp()
        }

        self.response_log.append(coordinated_response)

        return coordinated_response

    def _timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()


# 전문 방어 Agent들
class NetworkDefenderAgent(BaseAgent):
    """네트워크 방어 Agent"""

    def __init__(self):
        super().__init__(
            name="NetworkDefender",
            role="Network security specialist"
        )

    def reason(self, perception: str) -> str:
        prompt = f"""
        As a network security specialist, analyze:
        {perception}

        Provide:
        1. Network-level indicators
        2. Traffic analysis
        3. Firewall recommendations
        4. Network segmentation suggestions
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def act(self, reasoning_result: str) -> str:
        return reasoning_result


class EndpointDefenderAgent(BaseAgent):
    """엔드포인트 방어 Agent"""

    def __init__(self):
        super().__init__(
            name="EndpointDefender",
            role="Endpoint security specialist"
        )

    def reason(self, perception: str) -> str:
        prompt = f"""
        As an endpoint security specialist, analyze:
        {perception}

        Provide:
        1. Endpoint indicators of compromise
        2. Malware analysis
        3. Remediation steps
        4. Endpoint hardening recommendations
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def act(self, reasoning_result: str) -> str:
        return reasoning_result


class DataProtectionAgent(BaseAgent):
    """데이터 보호 Agent"""

    def __init__(self):
        super().__init__(
            name="DataProtector",
            role="Data security and privacy specialist"
        )

    def reason(self, perception: str) -> str:
        prompt = f"""
        As a data protection specialist, analyze:
        {perception}

        Provide:
        1. Data exposure risks
        2. Privacy implications
        3. Data loss prevention measures
        4. Encryption recommendations
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def act(self, reasoning_result: str) -> str:
        return reasoning_result


# Collaborative Defense System 초기화
defense_system = DefenseCoordinator()

# Agent 등록
defense_system.register_agent(NetworkDefenderAgent())
defense_system.register_agent(EndpointDefenderAgent())
defense_system.register_agent(DataProtectionAgent())

# 보안 이벤트 시뮬레이션
security_events = [
    """
    Alert: Multiple failed SSH login attempts detected
    Source IP: 203.0.113.45 (External)
    Target: Production server 10.0.1.50
    Time: 100 attempts in 5 minutes
    Usernames tried: root, admin, administrator, user
    """,

    """
    Alert: Suspicious file encryption activity
    Host: DESKTOP-USER01
    Process: unknown_process.exe
    Files affected: 150+ files in Documents folder
    File extensions changed to: .encrypted
    Network activity: Connection to tor-exit-node
    """,

    """
    Alert: Unusual data transfer detected
    Source: Database server 10.0.2.100
    Destination: External IP 198.51.100.75
    Data volume: 5 GB
    Time: 2:00 AM (off-hours)
    Protocol: HTTPS to unknown domain
    """
]

print("=== Collaborative Defense Agent System ===\n")

for i, event in enumerate(security_events, 1):
    print(f"\n{'='*60}")
    print(f"Security Event #{i}")
    print(f"{'='*60}")

    # 위협 탐지
    threat = defense_system.detect_threat(event)

    print(f"\nThreat Detected: {threat['is_threat']}")

    if threat["is_threat"]:
        # 조정된 대응
        response = defense_system.coordinate_response(threat)

        print(f"\n=== Coordinated Defense Strategy ===")
        print(response["coordinated_strategy"])
```

## 📊 Agent 성능 모니터링

```python
# examples/agents/agent_monitoring.py

class AgentMonitor:
    """Agent 성능 및 행동 모니터링"""

    def __init__(self):
        self.metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "average_response_time": 0,
            "task_history": []
        }

    def log_task(self, agent_name: str, task: str, result: Any, duration: float, success: bool):
        """작업 로깅"""
        self.metrics["total_tasks"] += 1

        if success:
            self.metrics["successful_tasks"] += 1
        else:
            self.metrics["failed_tasks"] += 1

        task_record = {
            "agent": agent_name,
            "task": task,
            "result": str(result)[:200],  # 처음 200자만
            "duration": duration,
            "success": success,
            "timestamp": self._timestamp()
        }

        self.metrics["task_history"].append(task_record)

        # 평균 응답 시간 업데이트
        total_time = sum(t["duration"] for t in self.metrics["task_history"])
        self.metrics["average_response_time"] = total_time / self.metrics["total_tasks"]

    def get_statistics(self) -> Dict[str, Any]:
        """통계 반환"""
        success_rate = (
            self.metrics["successful_tasks"] / self.metrics["total_tasks"] * 100
            if self.metrics["total_tasks"] > 0 else 0
        )

        return {
            "total_tasks": self.metrics["total_tasks"],
            "success_rate": f"{success_rate:.2f}%",
            "average_response_time": f"{self.metrics['average_response_time']:.2f}s",
            "recent_tasks": self.metrics["task_history"][-5:]
        }

    def _timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()


# Monitored Agent 래퍼
class MonitoredAgent:
    """모니터링 기능이 추가된 Agent 래퍼"""

    def __init__(self, agent: BaseAgent, monitor: AgentMonitor):
        self.agent = agent
        self.monitor = monitor

    def run(self, input_data: str) -> Any:
        """모니터링을 포함한 Agent 실행"""
        import time

        start_time = time.time()
        success = False
        result = None

        try:
            result = self.agent.run(input_data)
            success = True
        except Exception as e:
            result = f"Error: {str(e)}"
        finally:
            duration = time.time() - start_time
            self.monitor.log_task(
                agent_name=self.agent.name,
                task=input_data,
                result=result,
                duration=duration,
                success=success
            )

        return result
```

## 📚 실습 체크리스트

### Agent 기초
- [ ] BaseAgent 클래스 이해
- [ ] Conversational Agent 구현
- [ ] Red Team Agent 구현

### Multi-Agent Systems
- [ ] Agent Coordinator 구현
- [ ] SOC Agent 팀 구성
- [ ] Self-Guided Agent 구현

### Tool Integration
- [ ] Tool 클래스 구현
- [ ] Tool-Augmented Agent 개발
- [ ] 보안 도구 통합

### 고급 시스템
- [ ] Autonomous Pentest Agent 구현
- [ ] Collaborative Defense System 구축
- [ ] Agent 모니터링 시스템 구현

## 🎓 다음 단계

1. 실제 보안 도구와 Agent 통합 (nmap, Metasploit, etc.)
2. 실시간 위협 인텔리전스 피드 연동
3. 프로덕션 환경에 맞는 확장 및 최적화
4. 멀티 모달 Agent (이미지, 코드 등 통합)

## 🔗 참고 자료

- [LangChain Agent Documentation](https://python.langchain.com/docs/modules/agents/)
- [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT)
- [MetaGPT](https://github.com/geekan/MetaGPT)

---

**Last Updated:** 2025-11-17
**Models Used:** GPT-5.1, GPT-5.1-Thinking
**Framework:** OpenAI API
