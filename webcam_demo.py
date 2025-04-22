import cv2
import time
from datetime import datetime
import os
import requests

# Configurações éticas do projeto
AVISO = """
=========================================
  ** ATENÇÃO: Este programa é uma demonstração **
=========================================
  Este script foi projetado para capturar imagens da webcam 
  e salvá-las localmente. As imagens serão armazenadas na pasta 
  'demo_images' e, caso o programa seja encerrado, elas serão 
  enviadas para um servidor.

  ** Importante: **
  Por favor, tenha em mente que este código deve ser utilizado 
  com total consentimento e responsabilidade. A privacidade dos dados 
  deve sempre ser respeitada.
=========================================
"""

def verificar_consentimento():
    print(AVISO)
    consentimento = input("Deseja continuar? Para prosseguir, confirme com 's' (sim) ou 'n' (não): ").lower()
    if consentimento != 's':
        print("Operação abortada: Consentimento não fornecido.")
        exit()

def webcam_demo():
    # Cria diretório para imagens (se não existir)
    if not os.path.exists('demo_images'):
        os.makedirs('demo_images')
    
    # Inicia a webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erro: Webcam não encontrada")
        return
    
    print("Pressione 'q' para encerrar")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Mostra o vídeo ao vivo (com aviso)
            cv2.putText(frame, "DEMONSTRACAO ", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow('Webcam Demo ', frame)
            
            # Salva frame a cada 5 segundos (para demonstração)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if int(time.time()) % 5 == 0:
                filename = f"demo_images/webcam_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Frame salvo: {filename} (Simulacao)")
            
            # Encerra ao pressionar 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        enviar_pasta_para_servidor('demo_images', 'http://127.0.0.1:5000/upload')
        print("Demonstração encerrada")

def enviar_pasta_para_servidor(pasta, url_destino):
    for nome_arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, nome_arquivo)

        if os.path.isfile(caminho_arquivo):
            with open(caminho_arquivo, 'rb') as f:
                arquivos = {'file': (nome_arquivo, f)}
                try:
                    resposta = requests.post(url_destino, files=arquivos)
                    print(f"{nome_arquivo} enviado. Status: {resposta.status_code}")
                except Exception as e:
                    print(f"Erro ao enviar {nome_arquivo}: {e}")

if __name__ == "__main__":
    verificar_consentimento()
    webcam_demo()