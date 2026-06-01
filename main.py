import cv2
import numpy as np
import os
import json
from datetime import datetime

class DetectorIncendioSatelital:
    """
    Classe responsável pelo processamento digital de imagens (PDI) de satélite
    para a deteção automática, calibração e exportação de alertas de incêndio.
    """
    def __init__(self, caminho_imagem):
        self.caminho_imagem = caminho_imagem
        self.img_original = None
        self.img_hsv = None
        
        # Limites iniciais padrão para o filtro do fogo (calibrados anteriormente)
        self.h_min, self.s_min, self.v_min = 0, 100, 200
        self.h_max, self.s_max, self.v_max = 25, 255, 255

    def carregar_imagem(self):
        """Carrega a imagem do disco e verifica a sua existência."""
        if not os.path.exists(self.caminho_imagem):
            print(f"[ERRO] Imagem não encontrada: {caminho_imagem}")
            return False
        
        self.img_original = cv2.imread(self.caminho_imagem)
        self.registrar_log(f"Imagem carregada com sucesso. Dimensões: {self.img_original.shape}")
        return True

    @staticmethod
    def _funcao_vazia(x):
        """Função de callback obrigatória para as Trackbars do OpenCV."""
        pass

    def inicializar_painel_controle(self):
        """Cria a janela de trackbars para a calibração dos filtros."""
        cv2.namedWindow("Painel de Controle")
        cv2.resizeWindow("Painel de Controle", 400, 350)

        # Registrar os seletores dinâmicos
        cv2.createTrackbar("H Minimo", "Painel de Controle", self.h_min, 180, self._funcao_vazia)
        cv2.createTrackbar("S Minimo", "Painel de Controle", self.s_min, 255, self._funcao_vazia)
        cv2.createTrackbar("V Minimo", "Painel de Controle", self.v_min, 255, self._funcao_vazia)
        cv2.createTrackbar("H Maximo", "Painel de Controle", self.h_max, 180, self._funcao_vazia)
        cv2.createTrackbar("S Maximo", "Painel de Controle", self.s_max, 255, self._funcao_vazia)
        cv2.createTrackbar("V Maximo", "Painel de Controle", self.v_max, 255, self._funcao_vazia)

    def atualizar_valores_filtros(self):
        """Lê os valores atuais das barras de calibração."""
        self.h_min = cv2.getTrackbarPos("H Minimo", "Painel de Controle")
        self.s_min = cv2.getTrackbarPos("S Minimo", "Painel de Controle")
        self.v_min = cv2.getTrackbarPos("V Minimo", "Painel de Controle")
        self.h_max = cv2.getTrackbarPos("H Maximo", "Painel de Controle")
        self.s_max = cv2.getTrackbarPos("S Maximo", "Painel de Controle")
        self.v_max = cv2.getTrackbarPos("V Maximo", "Painel de Controle")

    def processar_pipeline_pdi(self):
        """Executa os passos de conversão, máscara morfológica e contornos."""
        self.img_hsv = cv2.cvtColor(self.img_original, cv2.COLOR_BGR2HSV)

        limite_inferior = np.array([self.h_min, self.s_min, self.v_min], dtype="uint8")
        limite_superior = np.array([self.h_max, self.s_max, self.v_max], dtype="uint8")
        mascara_fogo = cv2.inRange(self.img_hsv, limite_inferior, limite_superior)

        kernel = np.ones((3, 3), np.uint8)
        mascara_limpa = cv2.morphologyEx(mascara_fogo, cv2.MORPH_OPEN, kernel)

        contornos, _ = cv2.findContours(mascara_limpa, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return mascara_limpa, contornos

    def registrar_log(self, mensagem):
        """Grava logs de auditoria técnica em um arquivo texto."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha_log = f"[{timestamp}] {mensagem}\n"
        with open("historico_satelite.log", "a", encoding="utf-8") as f:
            f.write(linha_log)

    def salvar_alerta_json(self, qtd_focos, area_total):
        """Exporta os dados da anomalia térmica em formato JSON para integração com a equipe."""
        dados_alerta = {
            "satelite_status": "ALERTA_CRITICO",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "quadrante_analisado": os.path.basename(self.caminho_imagem),
            "focos_detectados": qtd_focos,
            "area_afetada_pixels": round(area_total, 2),
            "nivel_severidade": "ALTO" if area_total > 500 else "MEDIO"
        }
        with open("alerta_ativo.json", "w", encoding="utf-8") as f:
            json.dump(dados_alerta, f, indent=4, ensure_ascii=False)

    def renderizar_e_detectar(self):
        """Inicia o loop principal de monitoramento e exibição do pipeline."""
        if not self.carregar_imagem():
            return

        self.inicializar_painel_controle()
        self.registrar_log("Monitoramento orbital iniciado via interface de calibração.")
        
        print("\n[SISTEMA] Satélite operacional. Gerando logs e payloads de integração...")
        print("[SISTEMA] Pressione 'q' para encerrar.")

        # Variável para controlar os prints no terminal e não inundar a tela
        ultimo_alerta_status = None

        while True:
            self.atualizar_valores_filtros()
            mascara_limpa, contornos = self.processar_pipeline_pdi()

            img_resultado = self.img_original.copy()
            focos_validos = 0
            area_total_pixels = 0

            for idx, contorno in enumerate(contornos):
                area = cv2.contourArea(contorno)
                if area > 20:
                    focos_validos += 1
                    area_total_pixels += area
                    x, y, largura, altura = cv2.boundingRect(contorno)
                    cv2.rectangle(img_resultado, (x, y), (x + largura, y + altura), (0, 0, 255), 2)
                    cv2.putText(img_resultado, f"FOCO_{focos_validos}", (x, y - 5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            # Lógica de disparo e gravação de arquivos baseada nos achados
            if focos_validos > 0:
                self.salvar_alerta_json(focos_validos, area_total_pixels)
                if ultimo_alerta_status != "ALERTA":
                    self.registrar_log(f"INCÊNDIO DETECTADO! Focos: {focos_validos} | Área: {area_total_pixels}px")
                    print(f"\n🚨 [ALERTA] Payload de telemetria exportado para 'alerta_ativo.json'!")
                    ultimo_alerta_status = "ALERTA"
            else:
                # Se não há fogo, remove o JSON de alerta crítico para limpar o status do backend
                if os.path.exists("alerta_ativo.json"):
                    os.remove("alerta_ativo.json")
                if ultimo_alerta_status != "OK":
                    self.registrar_log("Nenhuma anomalia térmica detectada no quadrante.")
                    print("\n✅ [STATUS] Quadrante normalizado. Arquivo de alerta limpo.")
                    ultimo_alerta_status = "OK"

            # Renderização das janelas passo a passo
            cv2.imshow("Janela 1 - Imagem Original Satelite", self.img_original)
            cv2.imshow("Janela 2 - Conversao para Espaco HSV", self.img_hsv)
            cv2.imshow("Janela 3 - Mascara Binaria (Filtro Isolado)", mascara_limpa)
            cv2.imshow("Janela 4 - Resultado Final (Deteccao e Alertas)", img_resultado)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.registrar_log("Monitoramento encerrado pelo operador orbital.")
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    caminho = os.path.join("imagens", "satelite_fogo.jpg")
    detector = DetectorIncendioSatelital(caminho)
    detector.renderizar_e_detectar()