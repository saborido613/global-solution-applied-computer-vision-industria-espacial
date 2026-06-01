import cv2
import numpy as np
import os
import json
import glob
from datetime import datetime

class DetectorIncendioSatelital:
    """
    Classe responsável pelo processamento digital de imagens (PDI) de satélite
    para simulação de órbita, detecção de queimadas e exportação de payloads.
    """
    def __init__(self, pasta_imagens):
        self.pasta_imagens = pasta_imagens
        self.lista_imagens = []
        self.img_original = None
        self.img_hsv = None
        
        # Valores calibrados padrão para o filtro do fogo
        self.h_min, self.s_min, self.v_min = 0, 100, 200
        self.h_max, self.s_max, self.v_max = 25, 255, 255

    def mapear_arquivos_orbita(self):
        """Busca todas as imagens válidas dentro da pasta designada."""
        padrao_busca = os.path.join(self.pasta_imagens, "*.*")
        arquivos = glob.glob(padrao_busca)
        
        # Filtrar apenas formatos de imagem comuns
        self.lista_imagens = [arq for arq in arquivos if arq.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        self.lista_imagens.sort() # Ordena para a simulação ter sequência
        
        print(f"[LOG] Órbita mapeada. {len(self.lista_imagens)} quadrantes terrestres prontos para análise.")
        return len(self.lista_imagens) > 0

    @staticmethod
    def _funcao_vazia(x):
        pass

    def inicializar_painel_controle(self):
        """Cria a janela de trackbars para a calibração fina."""
        cv2.namedWindow("Painel de Controle")
        cv2.resizeWindow("Painel de Controle", 400, 350)

        cv2.createTrackbar("H Minimo", "Painel de Controle", self.h_min, 180, self._funcao_vazia)
        cv2.createTrackbar("S Minimo", "Painel de Controle", self.s_min, 255, self._funcao_vazia)
        cv2.createTrackbar("V Minimo", "Painel de Controle", self.v_min, 255, self._funcao_vazia)
        cv2.createTrackbar("H Maximo", "Painel de Controle", self.h_max, 180, self._funcao_vazia)
        cv2.createTrackbar("S Maximo", "Painel de Controle", self.s_max, 255, self._funcao_vazia)
        cv2.createTrackbar("V Maximo", "Painel de Controle", self.v_max, 255, self._funcao_vazia)

    def atualizar_valores_filtros(self):
        self.h_min = cv2.getTrackbarPos("H Minimo", "Painel de Controle")
        self.s_min = cv2.getTrackbarPos("S Minimo", "Painel de Controle")
        self.v_min = cv2.getTrackbarPos("V Minimo", "Painel de Controle")
        self.h_max = cv2.getTrackbarPos("H Maximo", "Painel de Controle")
        self.s_max = cv2.getTrackbarPos("S Maximo", "Painel de Controle")
        self.v_max = cv2.getTrackbarPos("V Maximo", "Painel de Controle")

    def processar_pipeline_pdi(self):
        self.img_hsv = cv2.cvtColor(self.img_original, cv2.COLOR_BGR2HSV)

        limite_inferior = np.array([self.h_min, self.s_min, self.v_min], dtype="uint8")
        limite_superior = np.array([self.h_max, self.s_max, self.v_max], dtype="uint8")
        mascara_fogo = cv2.inRange(self.img_hsv, limite_inferior, limite_superior)

        kernel = np.ones((3, 3), np.uint8)
        mascara_limpa = cv2.morphologyEx(mascara_fogo, cv2.MORPH_OPEN, kernel)

        contornos, _ = cv2.findContours(mascara_limpa, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return mascara_limpa, contornos

    def registrar_log(self, mensagem):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("historico_satelite.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {mensagem}\n")

    def salvar_alerta_json(self, nome_arquivo, qtd_focos, area_total):
        dados_alerta = {
            "satelite_status": "ALERTA_CRITICO",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "quadrante_analisado": os.path.basename(nome_arquivo),
            "focos_detectados": qtd_focos,
            "area_afetada_pixels": round(area_total, 2),
            "nivel_severidade": "ALTO" if area_total > 500 else "MEDIO"
        }
        with open("alerta_ativo.json", "w", encoding="utf-8") as f:
            json.dump(dados_alerta, f, indent=4, ensure_ascii=False)

    def iniciar_simulacao_orbita(self):
        """Varre a pasta de imagens simulando o deslocamento do satélite."""
        if not self.mapear_arquivos_orbita():
            print("[ERRO] Nenhuma imagem encontrada na pasta 'imagens/'.")
            return

        self.inicializar_painel_controle()
        self.registrar_log("--- NOVA SIMULAÇÃO DE TRANSMISSÃO ORBITAL INICIADA ---")
        
        print("\n🛰️ [SISTEMA] Satélite em órbita baixa iniciado.")
        print("🎮 Comandos das janelas: Press 'n' para avançar de quadrante | Press 'q' para abortar missão.")

        # Loop para percorrer a lista de imagens mapeadas
        for indice, caminho_img in enumerate(self.lista_imagens):
            nome_breve = os.path.basename(caminho_img)
            print(f"\n🌍 [ÓRBITA] Entrando no Quadrante {indice + 1}/{len(self.lista_imagens)}: {nome_breve}")
            
            self.img_original = cv2.imread(caminho_img)
            self.registrar_log(f"Analisando quadrante terrestre: {nome_breve}")

            ultimo_status_impresso = None

            # Loop interno de calibração para o frame/imagem atual
            while True:
                self.atualizar_valores_filtros()
                mascara_limpa, contornos = self.processar_pipeline_pdi()

                img_resultado = self.img_original.copy()
                focos_validos = 0
                area_total_pixels = 0

                for contorno in contornos:
                    area = cv2.contourArea(contorno)
                    if area > 20:
                        focos_validos += 1
                        area_total_pixels += area
                        x, y, largura, altura = cv2.boundingRect(contorno)
                        cv2.rectangle(img_resultado, (x, y), (x + largura, y + altura), (0, 0, 255), 2)
                        cv2.putText(img_resultado, f"FOCO_{focos_validos}", (x, y - 5), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                # Gerenciamento de alertas dinâmicos por imagem
                if focos_validos > 0:
                    self.salvar_alerta_json(caminho_img, focos_validos, area_total_pixels)
                    if ultimo_status_impresso != "ALERTA":
                        self.registrar_log(f"Anomalia em {nome_breve}! Focos: {focos_validos} | Área: {area_total_pixels}px")
                        print(f"   🚨 Foco detectado! Telemetria exportada para 'alerta_ativo.json'.")
                        ultimo_status_impresso = "ALERTA"
                else:
                    if os.path.exists("alerta_ativo.json"):
                        os.remove("alerta_ativo.json")
                    if ultimo_status_impresso != "OK":
                        self.registrar_log(f"Quadrante {nome_breve} está estável e seguro.")
                        print("   ✅ Varredura limpa. Nenhuma assinatura térmica de risco encontrada.")
                        ultimo_status_impresso = "OK"

                # Renderização das etapas visuais
                cv2.imshow("Janela 1 - Imagem Original Satelite", self.img_original)
                cv2.imshow("Janela 2 - Conversao para Espaco HSV", self.img_hsv)
                cv2.imshow("Janela 3 - Mascara Binaria (Filtro Isolado)", mascara_limpa)
                cv2.imshow("Janela 4 - Resultado Final (Deteccao e Alertas)", img_resultado)

                # Monitoramento do teclado
                tecla = cv2.waitKey(1) & 0xFF
                if tecla == ord('n'): # 'n' quebra o loop interno e pula para a próxima imagem da lista
                    print(f"⬇️ [SISTEMA] Movendo órbita para o próximo quadrante...")
                    break
                elif tecla == ord('q'): # 'q' encerra toda a execução do programa
                    print("\n🛑 [SISTEMA] Missão abortada pelo operador de controle.")
                    self.registrar_log("Varredura interrompida pelo painel de controle.")
                    cv2.destroyAllWindows()
                    return

        print("\n🏁 [SISTEMA] Varredura orbital completa! Todos os quadrantes da pasta foram analisados.")
        self.registrar_log("Simulação finalizada com sucesso.")
        cv2.destroyAllWindows()

if __name__ == "__main__":
    pasta_alvo = "imagens"
    simulador = DetectorIncendioSatelital(pasta_alvo)
    simulador.iniciar_simulacao_orbita()