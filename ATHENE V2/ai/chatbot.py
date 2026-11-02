# ai/chatbot.py
import threading
from core.topics import Topics
from ai.llm import LLMClient
from ai.prompt_builder import PromptBuilder
from ai.parser import ResponseParser, ResponseType

class AtheneChatbot:
    def __init__(self, event_bus, datastore):
        self.bus = event_bus
        self.datastore = datastore
        self.llm = LLMClient()
        self.prompt_builder = PromptBuilder()
        self.parser = ResponseParser()
        
        # Inscreve o chatbot para escutar as mensagens que o usuário digita
        self.bus.subscribe(Topics.CHAT_USER_MESSAGE, self.on_user_message_received)

    def on_user_message_received(self, message: str):
        """Callback do barramento. Inicia uma thread para não travar a interface gráfica."""
        threading.Thread(target=self._process_message, args=(message,), daemon=True).start()

    def _process_message(self, message: str):
        self.bus.publish(Topics.AI_INTENT, {"type": "thinking"})
        self.bus.publish(Topics.SYSTEM_LOG, "[SYSTEM]: AI está processando o prompt...")
        
        try:
            # CORRIGIDO: Trocado de get_telemetry_snapshot() para get_snapshot()
            snapshot = self.datastore.get_snapshot()
            
            prompt = self.prompt_builder.build(
                question=message,
                metrics=snapshot["metrics"],
                # Como seu snapshot retorna "network", vamos mapear com segurança aqui
                recent_events=snapshot.get("network", {}) 
            )
            
            raw_response = self.llm.ask(prompt)
            resp_type, payload = self.parser.parse(raw_response)
            
            if resp_type == ResponseType.COMMAND:
                self.bus.publish(Topics.COMMAND, payload)
                self.bus.publish(Topics.SYSTEM_LOG, f"[COMMAND]: Executando ação direcionada.")
                
            elif resp_type == ResponseType.TEXT:
                self.bus.publish(Topics.AI_INTENT, {"type": "speaking"})
                # Em vez do print(), publicamos no barramento
                ai_text = payload.get('text', '')
                self.bus.publish(Topics.CHAT_AI_MESSAGE, ai_text)
                
        except Exception as e:
            error_msg = "Não consegui acessar minha camada cognitiva no momento."
            self.bus.publish(Topics.CHAT_AI_MESSAGE, error_msg)
            self.bus.publish(Topics.SYSTEM_LOG, f"[ERROR]: Falha crítica na LLM: {e}")
            
        self.bus.publish(Topics.AI_INTENT, {"type": "done"})