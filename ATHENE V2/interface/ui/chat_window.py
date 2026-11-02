# interface/ui/chat_window.py
import tkinter as tk
from tkinter import scrolledtext
import threading
from core.topics import Topics

class AtheneChatWindow:
    def __init__(self, event_bus):
        self.bus = event_bus
        self.root = None
        self.forced_mode = False  # Flag para travar o modo se usado o --force
        
        self.bus.subscribe(Topics.CHAT_AI_MESSAGE, self.on_ai_message)
        self.bus.subscribe(Topics.SYSTEM_LOG, self.on_system_log)

    def start(self):
        threading.Thread(target=self._create_window, daemon=True).start()

    def _create_window(self):
        self.root = tk.Tk()
        self.root.title("ATHENE - AI Terminal Context")
        self.root.geometry("480x620")
        self.root.configure(bg="#050705")

        # Layout do Terminal
        self.txt_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, bg="#0a0f0a", fg="#1aff1a", 
            insertbackground="#1aff1a", font=("Consolas", 10),
            selectbackground="#004400"
        )
        self.txt_area.pack(padx=12, pady=12, fill=tk.BOTH, expand=True)
        self.txt_area.insert(tk.END, "[SYSTEM]: TERMINAL INTERATIVO ONLINE. INSIRA DIRETRIZES OU COMANDOS DE MODO.\n\n")
        self.txt_area.configure(state='disabled')

        bottom_frame = tk.Frame(self.root, bg="#050705")
        bottom_frame.pack(padx=12, pady=(0, 12), fill=tk.X)

        # interface/ui/chat_window.py (Trecho modificado dentro de _create_window)

        # CORRIGIDO: Removido o argumento inválido 'placeholder'
        self.entry_box = tk.Entry(
            bottom_frame, bg="#0d140d", fg="#ffffff", 
            insertbackground="#1aff1a", font=("Consolas", 11), 
            borderwidth=1, relief=tk.FLAT
        )
        self.entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        # E altere a inicialização do botão RUN tirando o "px" que é inválido no Tkinter (o correto é padx)
        btn_send = tk.Button(
            bottom_frame, text="RUN", bg="#1aff1a", fg="#050705", 
            font=("Consolas", 9, "bold"), activebackground="#00cc00",
            relief=tk.FLAT, command=self.send_message, padx=10  # <- CORRIGIDO DE px PARA padx
        )
        btn_send.pack(side=tk.RIGHT, padx=(6, 0))

        self.root.mainloop()

    def send_message(self):
        message = self.entry_box.get().strip()
        if not message:
            return

        self.entry_box.delete(0, tk.END)
        self._append_text(f"athene@core:~$ {message}\n", "user")

        # INTERCEPTADOR DE COMANDOS DE SISTEMA: /mode <nome> [--force]
        if message.startswith("/mode"):
            self._handle_mode_command(message)
            return
        
        # Se o sistema estiver em modo forçado, avisa o operador mas processa o texto normalmente
        if self.forced_mode:
            self.bus.publish(Topics.SYSTEM_LOG, "[WARN]: IA respondendo sob subsistema de confinamento de modo (--force).")

        self.bus.publish(Topics.CHAT_USER_MESSAGE, message)

    def _handle_mode_command(self, cmd_string: str):
        parts = cmd_string.split()
        if len(parts) < 2:
            self._append_text("[SYSTEM ERROR]: Sintaxe incorreta. Use: /mode <idle|server|warning|alert> [--force]\n", "system")
            return
            
        target_mode = parts[1].lower()
        force_flag = "--force" in parts

        # Mapeia a string para o Enum de modos do seu core
        from core.modes import Mode
        mode_mapping = {
            "idle": Mode.SERVER,  # Modo ocioso visual mapeia para o estado padrão
            "server": Mode.SERVER,
            "warning": Mode.WARNING,
            "alert": Mode.ALERT
        }

        if target_mode in mode_mapping:
            selected_enum = mode_mapping[target_mode]
            self.forced_mode = force_flag
            
            payload = {"mode": selected_enum, "forced": force_flag, "forced_name": target_mode}
            
            # CORRIGIDO: Publicando no canal exclusivo de comandos dedicados
            self.bus.publish(Topics.COMMAND_MODE_OVERRIDE, payload) 
            
            log_txt = f"[SYSTEM]: Modo alterado para {target_mode.upper()} "
            log_txt += "[FORCEMENT LOCK ACTIVE]\n" if force_flag else "[DYNAMIC TELEMETRY AUTOOVERRIDE ALLOWED]\n"
            self._append_text(log_txt, "system")
        else:
            self._append_text(f"[SYSTEM ERROR]: Modo '{target_mode}' não reconhecido pela diretriz da ATHENE.\n", "system")

    def on_ai_message(self, message):
        self.root.after(0, self._type_text, message, 0)

    def _type_text(self, text, index):
        if index == 0:
            self.txt_area.configure(state='normal')
            self.txt_area.insert(tk.END, "[ATHENE]: ")
            self.txt_area.configure(state='disabled')
        
        if index < len(text):
            self.txt_area.configure(state='normal')
            self.txt_area.insert(tk.END, text[index])
            self.txt_area.configure(state='disabled')
            self.txt_area.see(tk.END)
            self.root.after(25, self._type_text, text, index + 1)
        else:
            self.txt_area.configure(state='normal')
            self.txt_area.insert(tk.END, "\n\n")
            self.txt_area.configure(state='disabled')
            self._apply_style("ai")

    def on_system_log(self, log_msg):
        self._append_text(f"{log_msg}\n", "system")

    def _append_text(self, text, tag_type):
        if self.root:
            self.root.after(0, self._safe_append, text, tag_type)

    def _safe_append(self, text, tag_type):
        self.txt_area.configure(state='normal')
        self.txt_area.insert(tk.END, text)
        
        end_idx = self.txt_area.index(tk.END + "-1c")
        start_idx = self.txt_area.index(f"{end_idx} linestart")
        
        if tag_type == "user":
            self.txt_area.tag_add("user_style", start_idx, end_idx)
            self.txt_area.tag_config("user_style", foreground="#88ff88")
        elif tag_type == "ai":
            self.txt_area.tag_add("ai_style", "end-250c", tk.END)
            self.txt_area.tag_config("ai_style", foreground="#ffffff")
        elif tag_type == "system":
            self.txt_area.tag_add("sys_style", start_idx, end_idx)
            self.txt_area.tag_config("sys_style", foreground="#00aa00")
            
        self.txt_area.configure(state='disabled')
        self.txt_area.see(tk.END)