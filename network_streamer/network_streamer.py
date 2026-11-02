# network_streamer.py
import socket
import pygame
import numpy as np

# Configurações de Rede
ESP32_IP = "11.22.33.44"  # Coloque o IP do seu ESP32 aqui
UDP_PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def stream_pygame_surface(surface):
    """
    Captura a tela do Pygame (480x320), converte para RGB565 de 16 bits 
    e envia via blocos UDP de forma ultra-veloz.
    """
    # 1. Converte a superfície para uma matriz de pixels de 32 bits (RGB)
    view = pygame.surfarray.array3d(surface) # Retorna matriz (W, H, 3)
    view = np.transpose(view, (1, 0, 2))     # Ajusta para (H, W, 3) se necessário
    
    # Separando os canais R, G, B
    r = view[:, :, 0].astype(np.uint16)
    g = view[:, :, 1].astype(np.uint16)
    b = view[:, :, 2].astype(np.uint16)
    
    # 2. Compactação matemática bitwise para o formato RGB565 nativo do ILI9488
    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    
    # Transforma em array de bytes (Inverte os bytes se a tela apresentar cores trocadas - Endianness)
    raw_bytes = rgb565.byteswap().tobytes() if rgb565.dtype.byteorder == '>' else rgb565.tobytes()
    
    # 3. Dividir a tela em pedaços (ex: 20 linhas por pacote) para não estourar o limite UDP
    lines_per_packet = 20
    bytes_per_line = 480 * 2
    packet_size = bytes_per_line * lines_per_packet
    
    total_lines = 320
    packet_index = 0
    
    for start_line in range(0, total_lines, lines_per_packet):
        start_byte = start_line * bytes_per_line
        end_byte = start_byte + packet_size
        chunk = raw_bytes[start_byte:end_byte]
        
        # Cabeçalho do pacote: [ID do Pacote, Linha Inicial]
        header = bytes([packet_index, start_line])
        
        # Envia via UDP sem handshake (foco total em FPS)
        sock.sendto(header + chunk, (ESP32_IP, UDP_PORT))
        packet_index += 1