# Large Language Models in Cybersecurity - 실습 환경

이 레포지토리는 "Large Language Models in Cybersecurity" 책의 내용을 직접 실습하며 학습하기 위한 환경입니다.

## 📚 책 정보

- **제목**: Large Language Models in Cybersecurity: Threats, Exposure and Mitigation
- **저자**: Andrei Kucharavy, Octave Plancherel, Valentin Mulder, Alain Mermoud, Vincent Lenders
- **출판**: Springer (2024)
- **라이선스**: Open Access (Creative Commons Attribution 4.0)
- **링크**: https://link.springer.com/book/10.1007/978-3-031-54827-7

## 🎯 프로젝트 구조

```
Large-Language-Models-in-Cybersecurity/
├── README.md                          # 이 파일
├── claude.md                          # Claude 실습 가이드
├── agents.md                          # LLM Agents 고급 가이드
├── requirements.txt                   # Python 패키지 의존성
├── .env.example                       # 환경 변수 예시
├── Large-Language-Models-in-Cybersecurity.txt  # 원본 책 내용
├── examples/                          # 실습 예제 코드
│   ├── ch01_tokenization.py
│   ├── ch02_chain_of_thought.py
│   ├── ch07_info_leakage.py
│   ├── ch08_phishing_detection.py
│   ├── ch09_vulnerable_code.py
│   ├── ch10_prompt_injection.py
│   ├── agents/                        # Agent 예제
│   │   ├── base_agent.py
│   │   ├── security_advisor_agent.py
│   │   ├── multi_agent_coordinator.py
│   │   └── autonomous_pentest_agent.py
│   └── ...
└── notebooks/                         # Jupyter notebooks (선택사항)
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# Python 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. API 키 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 API 키를 입력합니다:

```bash
cp .env.example .env
```

`.env` 파일 편집:
```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### 3. 첫 실습 실행

```bash
# Chapter 1: 토큰화 실습
python examples/ch01_tokenization.py

# Chapter 2: Chain-of-Thought 프롬프팅
python examples/ch02_chain_of_thought.py
```

## 📖 학습 경로

### 초급: LLM 기초 (Part I)

1. **[claude.md](./claude.md)** - Claude와 함께하는 기본 실습
   - Chapter 1: LLM의 작동 원리
   - Chapter 2: 프롬프트 엔지니어링
   - Chapter 3-6: LLM 가족과 평가

### 중급: 보안 위협 이해 (Part II)

2. **보안 위협 실습**
   - Chapter 7: 정보 유출
   - Chapter 8: 피싱 및 소셜 엔지니어링
   - Chapter 9: 코드 취약점
   - Chapter 10: 프롬프트 인젝션

### 고급: Agent 시스템 (Part II + Part IV)

3. **[agents.md](./agents.md)** - LLM Agent 고급 실습
   - Multi-agent 시스템
   - Tool-augmented agents
   - Autonomous security testing
   - Collaborative defense

### 전문가: 완화 기술 (Part IV)

4. **완화 및 방어**
   - Red Teaming
   - Privacy-preserving training
   - Security awareness

## 🛠️ API 정보

### OpenAI Models (2025년 1월 기준)

이 프로젝트는 최신 OpenAI API를 사용합니다:

- **GPT-5.1** (`gpt-5.1-chat-latest`) - 최신 대화형 모델
- **GPT-5.1 Thinking** (`gpt-5.1-thinking`) - 향상된 추론 모델
- **GPT-5** (`gpt-5-chat-latest`) - 기본 GPT-5 모델
- **o3-mini** - 추론 전문 모델

### API 사용량 관리

```python
# 사용 예시
import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-5.1-chat-latest",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

## 📝 주요 실습 파일

### Part I: Introduction

| 파일 | 설명 | 난이도 |
|------|------|--------|
| `ch01_tokenization.py` | 토큰화 이해 | ⭐ |
| `ch01_temperature.py` | Temperature 파라미터 | ⭐ |
| `ch02_chain_of_thought.py` | Chain-of-Thought | ⭐⭐ |
| `ch02_system_prompt.py` | System Prompt | ⭐⭐ |

### Part II: Security Threats

| 파일 | 설명 | 난이도 |
|------|------|--------|
| `ch07_info_leakage.py` | 정보 유출 테스트 | ⭐⭐ |
| `ch08_phishing_detection.py` | 피싱 탐지 | ⭐⭐⭐ |
| `ch09_vulnerable_code.py` | 취약점 코드 분석 | ⭐⭐⭐ |
| `ch10_prompt_injection.py` | 프롬프트 인젝션 | ⭐⭐⭐ |

### Advanced: Agents

| 파일 | 설명 | 난이도 |
|------|------|--------|
| `agents/base_agent.py` | Agent 기본 클래스 | ⭐⭐ |
| `agents/security_advisor_agent.py` | 보안 상담 Agent | ⭐⭐⭐ |
| `agents/multi_agent_coordinator.py` | Multi-agent 조정 | ⭐⭐⭐⭐ |
| `agents/autonomous_pentest_agent.py` | 자율 침투 테스트 | ⭐⭐⭐⭐⭐ |

## 🔒 보안 및 윤리

### ⚠️ 중요한 주의사항

1. **교육 목적으로만 사용**: 모든 예제는 학습 및 연구 목적입니다
2. **허가된 시스템에만**: 자신이 소유하거나 테스트 권한이 있는 시스템에만 사용
3. **API 키 보안**: `.env` 파일을 절대 공개 저장소에 커밋하지 마세요
4. **책임감 있는 공개**: 발견한 취약점은 적절한 경로로 보고
5. **법적 준수**: 해당 지역의 사이버보안 관련 법률 준수

### .gitignore 필수 설정

```gitignore
# API Keys and secrets
.env
*.key
secrets/

# Virtual environment
venv/
env/

# Logs
logs/
*.log

# Python
__pycache__/
*.pyc
```

## 🧪 테스트

```bash
# 모든 테스트 실행
pytest tests/

# 특정 테스트
pytest tests/test_agents.py

# 커버리지 포함
pytest --cov=examples tests/
```

## 📚 추가 자료

### 공식 문서

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI GPT-5 Models](https://platform.openai.com/docs/models)
- [Anthropic Claude](https://www.anthropic.com/claude)

### 보안 리소스

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [LLM Security Guide](https://llmsecurity.net/)

### 커뮤니티

- [GitHub Discussions](../../discussions)
- [Issues](../../issues)

## 🤝 기여하기

이 프로젝트는 학습 목적의 오픈소스 프로젝트입니다.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 교육 목적으로 작성되었습니다. 원본 책은 Creative Commons Attribution 4.0 International License 하에 있습니다.

## 📞 문의

질문이나 제안사항이 있으시면 Issues를 열어주세요.

---

**Last Updated**: 2025-11-17
**Book Version**: 2024 Edition
**Python Version**: 3.8+
**OpenAI API**: GPT-5/GPT-5.1 (Latest)
