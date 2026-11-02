# ai/prompt_builder.py

class PromptBuilder:
    # ai/prompt_builder.py (Exemplo de como estruturar o método build)

    def build(self, question: str, metrics: dict, recent_events: dict) -> str:
        # Força os nomes corretos das chaves para a IA não se confundir
        contexto_sistema = f"""
        [STATUS DO SISTEMA]
        Status Geral: {metrics.get('status', 'OK')}
        Uso de CPU: {metrics.get('cpu', 0.0)}%
        Uso de RAM: {metrics.get('ram', 0.0)}%
        Temperatura da CPU: {metrics.get('temp', 0.0)}°C

        [MÉTRICAS DE REDE]
        Dispositivos Totais Cadastrados: {recent_events.get('total_devices', 0)}
        Dispositivos Ativos/Online Autorizados: {recent_events.get('online_devices', 0)}
        Dispositivos Desconhecidos/Anomalias Detectadas: {recent_events.get('unknown_devices', 0)}
        """
        
        # Junte com as instruções de comportamento da Athene
        system_instruction = f"""
        Você é a ATHENE, uma inteligência artificial de monitoramento cibernético tático.
        Responda de forma direta, concisa e use os dados reais fornecidos no contexto.
        Se houver anomalias de rede (dispositivos desconhecidos), alerte o operador imediatamente.
        
        Dados atuais do ambiente:
        {contexto_sistema}
        """
        
        # Retorna a estrutura final para o LLM Client
        return system_instruction + f"\n\nUsuário perguntou: {question}"