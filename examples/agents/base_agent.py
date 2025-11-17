"""
Base Agent 클래스
모든 Agent의 기본 구조를 정의
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import openai

load_dotenv()


class BaseAgent(ABC):
    """기본 Agent 추상 클래스"""

    def __init__(self, name: str, role: str, model: str = "gpt-5.1-chat-latest"):
        """
        Args:
            name: Agent 이름
            role: Agent 역할 설명
            model: 사용할 LLM 모델
        """
        self.name = name
        self.role = role
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.memory: List[Dict[str, str]] = []

    def perceive(self, input_data: str) -> str:
        """
        환경 인식 - 입력 데이터 처리

        Args:
            input_data: 입력 데이터

        Returns:
            처리된 입력
        """
        return input_data

    @abstractmethod
    def reason(self, perception: str) -> str:
        """
        추론 - LLM을 사용한 의사결정

        Args:
            perception: 인식된 데이터

        Returns:
            추론 결과
        """
        pass

    @abstractmethod
    def act(self, reasoning_result: str) -> Any:
        """
        행동 - 실제 작업 수행

        Args:
            reasoning_result: 추론 결과

        Returns:
            행동 결과
        """
        pass

    def remember(self, role: str, content: str):
        """
        메모리에 저장

        Args:
            role: 메시지 역할 (user/assistant/system)
            content: 메시지 내용
        """
        self.memory.append({"role": role, "content": content})

    def recall(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        메모리에서 회상

        Args:
            limit: 반환할 최대 메시지 수

        Returns:
            최근 메시지 목록
        """
        return self.memory[-limit:]

    def clear_memory(self):
        """메모리 초기화"""
        self.memory = []

    def run(self, input_data: str) -> Any:
        """
        Agent 실행 파이프라인

        Args:
            input_data: 입력 데이터

        Returns:
            최종 결과
        """
        # 1. Perceive
        perception = self.perceive(input_data)

        # 2. Reason
        reasoning = self.reason(perception)

        # 3. Act
        result = self.act(reasoning)

        return result

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', role='{self.role}')"


# Example implementation
class EchoAgent(BaseAgent):
    """간단한 Echo Agent 예제"""

    def __init__(self):
        super().__init__(
            name="EchoAgent",
            role="Simple agent that echoes input with LLM enhancement"
        )

    def reason(self, perception: str) -> str:
        """LLM을 사용하여 입력 강화"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Enhance this message with a friendly greeting: {perception}"
                }
            ]
        )
        return response.choices[0].message.content

    def act(self, reasoning_result: str) -> str:
        """결과 반환"""
        return reasoning_result


if __name__ == "__main__":
    # EchoAgent 테스트
    print("Testing BaseAgent with EchoAgent...\n")

    agent = EchoAgent()
    print(f"Agent: {agent}\n")

    result = agent.run("Hello, world!")
    print(f"Result: {result}")
