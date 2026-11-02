# core/topics.py
from enum import Enum

# core/topics.py (Trecho modificado)
class Topics(Enum):
    COMMAND = "command"
    MONITOR_CONTROL = "monitor:control"
    MONITOR_STATUS_CHANGED = "monitor:status_changed"
    MONITOR_STATE_EMITTED = "monitor:state_emitted"
    AI_INTENT = "ai:intent"
    STATE_CHANGED = "state:changed"           # Mantido exclusivamente para avisar o HUD da mudança real
    SYSTEM_SHUTDOWN = "system:shutdown"
    UI_THEME = "ui:theme"
    
    # NOVO TÓPICO DE CONTROLE
    COMMAND_MODE_OVERRIDE = "command:mode_override" # <--- ADICIONE ESTE
    
    CHAT_USER_MESSAGE = "chat:user_message"
    CHAT_AI_MESSAGE = "chat:ai_message"
    SYSTEM_LOG = "system:log"