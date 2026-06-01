# 🚀 Sistema Orbital de Detecção de Anomalias Térmicas e Resposta Rápida (S.O.D.A.R.)

## 🌌 Contexto da Solução (Global Solution - Indústria Espacial)
No cenário da "New Space", onde constelações de microssatélites redefinem a economia global, o **S.O.D.A.R.** surge como uma solução de Visão Computacional de ponta. O projeto utiliza imagens e dados satelitais de órbita baixa (LEO) para monitorar e mitigar um dos maiores problemas ambientais e econômicos do planeta: **os incêndios florestais e o desmatamento ilegal**.

Este componente representa o motor de **Applied Computer Vision** do ecossistema integrado desenvolvido pelo nosso grupo, funcionando como um "Gatilho Inteligente". Ao analisar anomalias térmicas em tempo real, o algoritmo automatiza a resposta e exporta payloads de dados instantâneos para o ecossistema corporativo (Backend/Frontend).

---

## 🛠️ Arquitetura e Pipeline de Processamento Digital de Imagens (PDI)

O motor visual foi totalmente desenvolvido em **Python** utilizando a biblioteca **OpenCV** e os conceitos fundamentais de matrizes com o **NumPy**, estruturado sob as melhores práticas da Programação Orientada a Objetos (POO).

O fluxo de processamento (Pipeline) segue rigidamente as seguintes etapas pedagógicas:

1. **Leitura e Validação Orbital:** Carregamento seguro da imagem matricial da superfície terrestre a partir do disco, prevenindo falhas de execução (*crashes*).
2. **Conversão de Espaço de Cores (BGR para HSV):** * *Justificativa Técnica:* Imagens digitais normais operam em RGB/BGR (onde a iluminação afeta diretamente os canais de cor). No contexto aeroespacial, reflexos do Sol nas nuvens ou nas copas das árvores gerariam falsos positivos. Ao converter para **HSV (Hue, Saturation, Value)**, isolamos completamente o canal de brilho/luminosidade ($V$), permitindo focar matematicamente apenas no espectro puro do calor e fogo ($H$ e $S$).
3. **Limiarização Dinâmica (Thresholding):** Aplicação de uma máscara binária onde pixels que correspondem à assinatura térmica do fogo viram branco ($255$) e o restante da floresta vira preto ($0$).
4. **Filtragem e Limpeza Morfológica:** Operação de abertura matemática (`MORPH_OPEN`) para eliminar ruídos de alta frequência isolados na transmissão do satélite.
5. **Extração de Contornos e Análise Geométrica:** Mapeamento das fronteiras das manchas térmicas detectadas, calculando a área afetada em pixels e delimitando os focos com caixas de alerta texturizadas (*Bounding Boxes*).

---

## 🚨 Integração e Telemetria (O Diferencial de Resposta Rápida)

O sistema não se limita a exibir imagens. Ele gera saídas padronizadas para auditoria e integração com os sistemas do resto do grupo:
* **Payload em Tempo Real (`alerta_ativo.json`):** Assim que o limiar crítico é ultrapassado, o script gera um payload JSON estruturado contendo o timestamp, o número de focos e a área calculada, ideal para ser consumido por APIs em Java/C# ou exibido em mapas no Frontend (React). Se a área é normalizada, o arquivo é deletado para liberar o status.
* **Logs de Auditoria Espacial (`historico_satelite.log`):** Gravação de eventos persistentes que registram todas as ações e análises executadas pelo satélite para fins de histórico e conformidade regulatória.

---

## 🗂️ Estrutura do Repositório da Disciplina

```text
detector-incendio-espacial/
│
├── imagens/                # Repositório de quadrantes/imagens de teste do satélite
│   └── satelite_fogo.jpg   # Imagem de calibração base
│
├── main.py                 # Código-fonte principal estruturado em POO (Classe Detector)
├── requirements.txt        # Dependências de bibliotecas do projeto (OpenCV, NumPy)
├── historico_satelite.log  # Arquivo gerado dinamicamente com logs de execução
├── alerta_ativo.json       # Payload JSON gerado dinamicamente em caso de incêndio ativo
└── README.md               # Documentação técnica do projeto

🚀 Como Executar o Projeto
Pré-requisitos
Certifique-se de ter o Python instalado no seu sistema (recomenda-se a versão 3.10 ou superior).

1. Clonar e Acessar o Projeto
Bash
git clone 
cd GS-APPLIED
2. Instalar as Dependências Técnicas
Utilize o instalador de pacotes do Python para instalar o OpenCV e o NumPy listados no arquivo de requisitos:

Bash
python -m pip install -r requirements.txt
3. Rodar o Monitoramento e Painel de Calibração
Execute o arquivo principal para abrir a interface gráfica de processamento:

Bash
python main.py
🎮 Como operar a Interface de Calibração
Ao executar o código, 4 Janelas Visuais e 1 Painel de Controle serão abertos na sua tela.

Você pode arrastar os seletores deslizantes (Trackbars) de H, S, V Mínimo e Máximo no Painel de Controle para calibrar os sensores do satélite em tempo real, ajustando a sensibilidade para diferentes tipos de vegetação ou iluminação terrestre.

Para encerrar o monitoramento de forma segura, foque em qualquer uma das janelas e pressione a tecla q no seu teclado.

👥 Integrantes do Grupo (Engenharia de Software - 4º Ano)
João Pedro Saborido - RM98184

Lucca Alexandre - RMXXXXX

Matheus Haruo - RMXXXXX

Pedro Guerra - RMXXXXX

Victor Wittner - RMXXXXX