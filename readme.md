# 🚀 Sistema Orbital de Detecção de Anomalias Térmicas e Resposta Rápida (S.O.D.A.R.)

## 🌌 Contexto da Solução (Global Solution - Indústria Espacial)
No cenário da "New Space", onde constelações de microssatélites redefinem a economia global, o **S.O.D.A.R.** surge como uma solução de Visão Computacional de ponta. O projeto simula o monitoramento de um satélite de órbita baixa (LEO) para mitigar um dos maiores problemas ambientais e econômicos do planeta: **os incêndios florestais e o desmatamento ilegal**.

Este componente representa o motor de **Applied Computer Vision** do ecossistema integrado desenvolvido pelo nosso grupo, funcionando como um "Gatilho Inteligente". Ao analisar anomalias térmicas em tempo real, o algoritmo automatiza a resposta e exporta payloads de dados instantâneos para o ecossistema corporativo (Backend/Frontend).

---

## 🛠️ Arquitetura e Pipeline de Processamento Digital de Imagens (PDI)

O motor visual foi totalmente desenvolvido em **Python** utilizando a biblioteca **OpenCV** e os conceitos fundamentais de matrizes com o **NumPy**, estruturado sob os princípios da Programação Orientada a Objetos (POO) com a classe `DetectorIncendioSatelital`.

O fluxo de processamento (Pipeline) segue rigidamente as seguintes etapas pedagógicas:

1. **Mapeamento Orbital Dinâmico:** O sistema utiliza a biblioteca `glob` para varrer a pasta de dados e listar sequencialmente os quadrantes disponíveis, oferecendo suporte nativo a extensões `.jpg`, `.jpeg`, `.png` e `.webp`.
2. **Conversão de Espaço de Cores (BGR para HSV):** * *Justificativa Técnica:* Imagens digitais normais operam em RGB/BGR (onde a iluminação afeta diretamente os canais de cor). No contexto aeroespacial, reflexos do Sol nas nuvens ou nas copas das árvores gerariam falsos positivos. Ao converter para **HSV (Hue, Saturation, Value)**, isolamos completamente o canal de brilho/luminosidade (V), permitindo focar matematicamente apenas no espectro puro do calor e fogo (H e S).
3. **Limiarização Dinâmica (Thresholding):** Aplicação de uma máscara binária baseada em trackbars, onde pixels que correspondem à assinatura térmica do fogo viram branco (255) e o restante da floresta vira preto (0).
4. **Filtragem e Limpeza Morfológica:** Operação de abertura matemática (`MORPH_OPEN`) com um kernel $3 \times 3$ para eliminar ruídos de alta frequência isolados na transmissão do satélite.
5. **Extração de Contornos e Análise Geométrica:** Mapeamento das fronteiras das manchas térmicas detectadas via `findContours`, calculando a área afetada em pixels e delimitando os focos com caixas de alerta texturizadas (*Bounding Boxes*).

---

## 🚨 Integração, Telemetria e Governança de Código

O sistema gera saídas padronizadas para auditoria e integração com as demais camadas do grupo:
* **Payload em Tempo Real (`alerta_ativo.json`):** Assim que o limiar crítico é ultrapassado, o script gera um payload JSON estruturado contendo o timestamp, o quadrante atual, o número de focos e a área calculada, ideal para ser consumido por APIs em Java/C# ou exibido em mapas no Frontend. Se a área é normalizada, o arquivo é deletado para liberar o status do ecossistema.
* **Logs de Auditoria Espacial (`historico_satelite.log`):** Gravação de eventos persistentes que registram todas as ações e análises executadas pelo satélite para fins de conformidade regulatória.
* **Governança de Código (Git & GitHub):** O desenvolvimento seguiu estritamente as boas práticas de Engenharia de Software, utilizando ramificações de funcionalidades (`feature/simulador-orbita`) e a abertura/resolução de *Pull Requests (PR)* antes da integração final com a branch de produção (`main`).

---

## 🗂️ Estrutura do Repositório da Disciplina

```text
detector-incendio-espacial/
│
├── imagens/                # Repositório de quadrantes/imagens de teste do satélite (jpg, webp, etc.)
│
├── main.py                 # Código-fonte principal estruturado em POO (Classe Detector)
├── requirements.txt        # Dependências de bibliotecas do projeto (OpenCV, NumPy)
├── .gitignore              # Filtro de arquivos locais e caches (ignora venv, logs e json ativos)
├── historico_satelite.log  # Arquivo gerado dinamicamente com logs de execução (ignorado no git)
├── alerta_ativo.json       # Payload JSON gerado dinamicamente em caso de incêndio (ignorado no git)
└── README.md               # Documentação técnica do projeto

# 🚀 Como Executar o Projeto

## Pré-requisitos
Certifique-se de ter o Python instalado no seu sistema (recomenda-se a versão 3.10 ou superior).

### 1. Clonar e Acessar o Projeto
```bash
git clone https://github.com/saborido613/global-solution-applied-computer-vision-industria-espacial.git
cd GS-APPLIED

### 2. Instalar as Dependências Técnicas
Utilize o instalador de pacotes do Python para instalar o OpenCV e o NumPy listados no arquivo de requisitos:

```bash
python -m pip install -r requirements.txt

## 3. Rodar a simulação Orbital
Execute o arquivo principal para abrir a interface gráfica de processamento:

```bash
python main.py

🎮 Comandos do Simulador de Órbita
Ao executar o código, 4 Janelas Visuais e 1 Painel de Controle serão abertos na sua tela.

Calibração: Você pode arrastar os seletores deslizantes (Trackbars) no Painel de Controle para calibrar os sensores do satélite em tempo real.

Tecla n (Next): Avança o satélite para o próximo quadrante terrestre da pasta imagens/, atualizando logs e gerando o novo JSON de telemetria correspondente.

Tecla q (Quit): Aborta a missão com segurança, fechando todas as janelas e encerrando os processos do satélite.

👥 Integrantes do Grupo (Engenharia de Software - 4º Ano)
João Pedro Saborido - RM98184

Lucca Alexandre - RMXXXXX

Matheus Haruo - RMXXXXX

Pedro Guerra - RMXXXXX

Victor Wittner - RMXXXXX