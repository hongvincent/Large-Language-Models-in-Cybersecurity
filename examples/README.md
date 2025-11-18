# LLM Cybersecurity - Example Scripts

이 디렉토리는 "Large Language Models in Cybersecurity" 책의 실습 예제 스크립트를 포함합니다.

## 📂 디렉토리 구조

```
examples/
├── README.md                          # 이 파일
├── ch01_tokenization.py               # Chapter 1: 토큰화
├── ch01_temperature.py                # Chapter 1: Temperature 파라미터
├── ch01_memorization.py               # Chapter 1: 메모리제이션 vs 일반화
├── ch02_chain_of_thought.py           # Chapter 2: Chain-of-Thought 프롬프팅
├── ch02_system_prompt.py              # Chapter 2: System Prompt
├── ch02_few_shot.py                   # Chapter 2: Few-shot Learning
├── ch07_info_leakage.py               # Chapter 7: 정보 유출
├── ch07_pii_detection.py              # Chapter 7: PII 감지
├── ch08_phishing_generation.py        # Chapter 8: 피싱 시뮬레이션 (교육용)
├── ch08_phishing_detection.py         # Chapter 8: 피싱 탐지
├── ch09_vulnerable_code.py            # Chapter 9: 취약한 코드 분석
├── ch09_owasp_check.py                # Chapter 9: OWASP Top 10 검사
├── ch10_prompt_injection.py           # Chapter 10: 프롬프트 인젝션
├── ch18_security_training.py          # Chapter 18: 보안 교육
├── ch24_red_teaming.py                # Chapter 24: Red Teaming
├── advanced_security_analysis.py      # GPT-5.1 Reasoning 활용
└── agents/                            # Agent 예제들
    ├── base_agent.py                  # 기본 Agent 클래스
    └── ... (추가 Agent 예제)
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 활성화 (프로젝트 루트에서)
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# .env 파일에 API 키 설정
echo "OPENAI_API_KEY=your-key-here" > ../.env
```

### 2. 예제 실행

```bash
# Part I - LLM 기초
python ch01_tokenization.py
python ch01_temperature.py
python ch02_chain_of_thought.py

# Part II - 보안 위협
python ch07_info_leakage.py
python ch08_phishing_detection.py
python ch09_vulnerable_code.py
python ch10_prompt_injection.py

# Part IV - 완화 기술
python ch18_security_training.py
python ch24_red_teaming.py
python advanced_security_analysis.py

# Agents
python agents/base_agent.py
```

## 📚 Part별 학습 가이드

### Part I: Introduction (초급)

**학습 순서:**
1. `ch01_tokenization.py` - LLM이 텍스트를 처리하는 방법 이해
2. `ch01_temperature.py` - 생성 결과의 무작위성 제어
3. `ch01_memorization.py` - LLM의 기억과 일반화 능력
4. `ch02_chain_of_thought.py` - 추론 능력 향상 기법
5. `ch02_system_prompt.py` - LLM 행동 제어
6. `ch02_few_shot.py` - 예제 기반 학습

**학습 목표:**
- LLM의 작동 원리 이해
- 프롬프트 엔지니어링 기법 습득
- Temperature 등 파라미터 활용

### Part II: Security Threats (중급)

**학습 순서:**
1. `ch07_info_leakage.py` → `ch07_pii_detection.py` - 정보 유출 위험
2. `ch08_phishing_generation.py` → `ch08_phishing_detection.py` - 피싱 공격
3. `ch09_vulnerable_code.py` → `ch09_owasp_check.py` - 코드 취약점
4. `ch10_prompt_injection.py` - 프롬프트 인젝션 공격 & 방어

**학습 목표:**
- LLM의 보안 위험 이해
- 공격 기법과 방어 전략 습득
- 실제 시나리오 분석 능력

### Part IV: Mitigation (고급)

**학습 순서:**
1. `ch18_security_training.py` - 보안 교육 컨텐츠 생성
2. `ch24_red_teaming.py` - Red Team 테스팅
3. `advanced_security_analysis.py` - GPT-5.1 Reasoning 활용

**학습 목표:**
- 완화 기술 구현
- Red Teaming 수행
- 고급 분석 기법

### Agents (전문가)

**agents.md 참조**

## 📝 스크립트 설명

### Part I: Introduction

#### ch01_tokenization.py
- **목적**: LLM의 토큰화 과정 이해
- **주요 기능**:
  - 다양한 텍스트의 토큰화 분석
  - 토큰화가 중요한 이유 설명
  - 한글, 코드, SQL 등 다양한 입력 테스트

#### ch01_temperature.py
- **목적**: Temperature 파라미터의 영향 이해
- **주요 기능**:
  - 0.0 ~ 2.0 범위의 temperature 테스트
  - 보안 시나리오별 권장 설정
  - 일관성 vs 창의성 trade-off

#### ch01_memorization.py
- **목적**: LLM의 메모리제이션과 일반화 능력 테스트
- **주요 기능**:
  - 잘 알려진 정보 기억 테스트
  - 새로운 시나리오 추론 테스트
  - 정보 유출 위험 데모

#### ch02_chain_of_thought.py
- **목적**: Chain-of-Thought 프롬프팅 기법
- **주요 기능**:
  - Simple vs CoT vs Zero-shot CoT 비교
  - 보안 관련 추론 문제 해결
  - 단계별 사고 과정 시연

#### ch02_system_prompt.py
- **목적**: System Prompt로 LLM 행동 제어
- **주요 기능**:
  - 다양한 역할(Security Expert, Auditor 등) 시뮬레이션
  - 안전 규칙 설정
  - 응답 스타일 제어

#### ch02_few_shot.py
- **목적**: Few-shot Learning 기법
- **주요 기능**:
  - 보안 이벤트 분류
  - CVE 심각도 평가
  - 로그 파싱
  - Zero-shot vs Few-shot 비교

### Part II: Security Threats

#### ch07_info_leakage.py
- **목적**: LLM의 정보 유출 위험 테스트
- **주요 기능**:
  - 데이터 패턴 유출 테스트
  - 훈련 데이터 메모리제이션 테스트
  - 간접적 정보 추출
  - 완화 전략

#### ch07_pii_detection.py
- **목적**: PII(개인식별정보) 감지 시스템
- **주요 기능**:
  - LLM 기반 PII 탐지
  - Regex와 비교
  - PII 마스킹/삭제
  - HIPAA Safe Harbor 방법

#### ch08_phishing_generation.py ⚠️
- **목적**: 보안 교육용 피싱 시뮬레이션
- **⚠️ 주의**: 교육 및 승인된 테스트 목적만
- **주요 기능**:
  - 교육용 피싱 이메일 생성
  - 피싱 기법 분석
  - 보안 인식 프로그램 설계

#### ch08_phishing_detection.py
- **목적**: 피싱 이메일 탐지 시스템
- **주요 기능**:
  - LLM 기반 피싱 분석
  - 위험 수준 평가
  - 배치 분석
  - 탐지 메트릭

#### ch09_vulnerable_code.py
- **목적**: LLM 생성 코드의 보안 취약점 분석
- **주요 기능**:
  - 다양한 취약점 유형 테스트
  - 보안 프롬프팅 vs 일반 프롬프팅 비교
  - 자동화된 보안 테스팅 프레임워크

#### ch09_owasp_check.py
- **목적**: OWASP Top 10 기준 코드 검사
- **주요 기능**:
  - 전체 OWASP Top 10 2021 검사
  - 심각도 평가
  - 수정 방안 제시
  - CI/CD 통합 가이드

#### ch10_prompt_injection.py
- **목적**: 프롬프트 인젝션 공격 및 방어
- **주요 기능**:
  - 취약한 vs 보안 강화 Assistant 비교
  - 다양한 인젝션 기법 테스트
  - 입력 검증 시스템
  - 방어 전략

### Part IV: Mitigation

#### ch18_security_training.py
- **목적**: LLM 활용 보안 교육 컨텐츠 생성
- **주요 기능**:
  - 주제별 교육 모듈 생성
  - 역할별 맞춤 교육
  - 피싱 시뮬레이션 프로그램 설계
  - 게이미피케이션
  - 효과 측정 메트릭

#### ch24_red_teaming.py
- **목적**: LLM Red Teaming 프레임워크
- **주요 기능**:
  - 프롬프트 인젝션 테스트
  - Jailbreak 시도
  - 정보 유출 테스트
  - 자동화된 Red Team 보고서 생성

#### advanced_security_analysis.py
- **목적**: GPT-5.1 Reasoning으로 심층 보안 분석
- **주요 기능**:
  - 위협 모델링
  - 아키텍처 보안 리뷰
  - 취약점 평가
  - 비교 분석
  - Zero Trust 설계

## 🔧 스크립트 사용 팁

### 일반 팁

1. **API 키 보안**
   ```bash
   # .env 파일 사용 (절대 커밋하지 말 것)
   OPENAI_API_KEY=your-key-here
   ```

2. **출력 저장**
   ```bash
   python ch09_vulnerable_code.py > results.txt
   ```

3. **특정 섹션만 실행**
   스크립트를 에디터로 열어 `main()` 함수 내 원하는 부분만 주석 해제

### 고급 사용

1. **배치 처리**
   ```bash
   for script in ch01_*.py; do
       python "$script" > "results_${script%.py}.txt"
   done
   ```

2. **커스텀 프롬프트**
   스크립트를 복사하여 자신의 use case에 맞게 수정

3. **자동화**
   스크립트를 크론잡이나 CI/CD에 통합

## ⚠️ 중요 주의사항

### 윤리적 사용

1. **교육 목적으로만**
   - 모든 예제는 학습 및 연구 목적
   - 실제 공격에 사용 금지

2. **승인된 테스트만**
   - 자신이 소유하거나 권한이 있는 시스템에만
   - 피싱 시뮬레이션은 조직 승인 필요

3. **API 비용**
   - GPT-5.1은 비용이 발생
   - 테스트 전 비용 확인
   - Temperature 높이면 토큰 사용 증가 가능

4. **민감 데이터**
   - 실제 PII, 기밀 정보 사용 금지
   - 예제 데이터만 사용

### 문제 해결

**API 키 오류**
```python
# .env 파일 확인
cat ../.env

# 환경 변수 직접 설정
export OPENAI_API_KEY="your-key"
```

**모듈 없음 오류**
```bash
pip install -r ../requirements.txt
```

**Rate Limit 오류**
```python
# 스크립트에 지연 추가
import time
time.sleep(1)  # 요청 사이 1초 대기
```

## 📊 학습 체크리스트

### Part I - 기초
- [ ] 토큰화 이해
- [ ] Temperature 파라미터 활용
- [ ] Chain-of-Thought 프롬프팅
- [ ] System Prompt 작성
- [ ] Few-shot Learning 적용

### Part II - 보안 위협
- [ ] 정보 유출 위험 이해
- [ ] PII 탐지 시스템 구현
- [ ] 피싱 탐지 시스템 구축
- [ ] 코드 취약점 분석
- [ ] 프롬프트 인젝션 방어

### Part IV - 완화
- [ ] 보안 교육 컨텐츠 생성
- [ ] Red Teaming 수행
- [ ] 고급 보안 분석

### Agents
- [ ] Base Agent 이해
- [ ] Multi-agent 시스템 구축
- [ ] Tool integration

## 📚 추가 자료

- **메인 가이드**: [claude.md](../claude.md)
- **Agent 가이드**: [agents.md](../agents.md)
- **프로젝트 README**: [README.md](../README.md)

## 🤝 기여

개선 사항이나 새로운 예제가 있으면 Pull Request를 보내주세요!

## 📝 라이선스

교육 목적. 원본 책은 Creative Commons Attribution 4.0 하에 있습니다.

---

**Last Updated**: 2025-11-17
**Total Scripts**: 16+ examples
**OpenAI Models**: GPT-5.1, GPT-5.1-Thinking
