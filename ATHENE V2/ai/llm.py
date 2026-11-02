# ai/llm.py
import time
from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL

class LLMClient:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def ask(self, prompt: str, retries: int = 3, timeout: float = 10.0) -> str:
        """Tenta consultar o Groq. Suporta até N retentativas antes de falhar."""
        for attempt in range(retries):
            try:
                # O cliente Groq gerencia internamente timeouts baseados nas requisições HTTP
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )
                return completion.choices[0].message.content
            except Exception as e:
                print(f"[LLM RETRY] Tentativa {attempt + 1}/{retries} falhou: {e}")
                if attempt < retries - 1:
                    time.sleep(1.5)  # Pequena pausa antes de tentar de novo
                else:
                    raise e