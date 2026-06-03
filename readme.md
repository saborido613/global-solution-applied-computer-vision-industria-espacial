# 🚀 Sistema Orbital de Detecção de Anomalias Térmicas e Resposta Rápida (S.O.D.A.R.)

## 🌌 Contexto da Solução (Global Solution - Indústria Espacial)

No cenário da **New Space**, onde constelações de microssatélites redefinem a economia global, o **S.O.D.A.R.** surge como uma solução de Visão Computacional de ponta. O projeto simula o monitoramento de um satélite de órbita baixa (LEO) para mitigar um dos maiores problemas ambientais e econômicos do planeta: **os incêndios florestais e o desmatamento ilegal**.

Este componente representa o motor de **Applied Computer Vision** do ecossistema integrado desenvolvido pelo nosso grupo, funcionando como um **Gatilho Inteligente**. Ao analisar anomalias térmicas em tempo real, o algoritmo automatiza a resposta e exporta payloads de dados instantâneos para o ecossistema corporativo (Backend/Frontend).

---

## 🛠️ Arquitetura e Pipeline de Processamento Digital de Imagens (PDI)

O motor visual foi totalmente desenvolvido em **Python**, utilizando a biblioteca **OpenCV** e os conceitos fundamentais de matrizes com o **NumPy**, estruturado sob os princípios da Programação Orientada a Objetos (POO) por meio da classe `DetectorIncendioSatelital`.

O fluxo de processamento segue as seguintes etapas:

### 1. Mapeamento Orbital Dinâmico

O sistema utiliza a biblioteca `glob` para varrer a pasta de dados e listar sequencialmente os quadrantes disponíveis, oferecendo suporte nativo às extensões `.jpg`, `.jpeg`, `.png` e `.webp`.

### 2. Conversão de Espaço de Cores (BGR → HSV)

**Justificativa Técnica:**
Imagens digitais convencionais operam em RGB/BGR, onde a iluminação afeta diretamente os canais de cor. No contexto aeroespacial, reflexos solares em nuvens ou copas de árvores poderiam gerar falsos positivos.

Ao converter a imagem para o espaço de cores **HSV (Hue, Saturation, Value)**, o canal de brilho (Value) é isolado dos canais responsáveis pela cor (Hue e Saturation), permitindo uma detecção mais precisa da assinatura térmica associada ao fogo.

### 3. Limiarização Dinâmica (Thresholding)

Aplicação de uma máscara binária baseada em **trackbars**, onde os pixels que correspondem à assinatura térmica do fogo são convertidos para branco (`255`) e o restante da imagem para preto (`0`).

### 4. Filtragem e Limpeza Morfológica

Utilização da operação morfológica de abertura (`MORPH_OPEN`) com um kernel de `3 × 3`, eliminando ruídos isolados de alta frequência provenientes da transmissão ou do processamento da imagem.

### 5. Extração de Contornos e Análise Geométrica

Mapeamento das fronteiras das regiões detectadas por meio da função `findContours`, permitindo:

* Cálculo da área afetada em pixels;
* Identificação dos focos de incêndio;
* Delimitação visual utilizando **Bounding Boxes**.

---

## 🚨 Integração, Telemetria e Governança de Código

O sistema gera saídas padronizadas para auditoria e integração com as demais camadas do projeto.

### 📡 Payload em Tempo Real (`alerta_ativo.json`)

Quando o limiar crítico é ultrapassado, o sistema gera automaticamente um payload JSON contendo:

* Timestamp da detecção;
* Quadrante analisado;
* Quantidade de focos identificados;
* Área total afetada.

Esse arquivo pode ser consumido por APIs Java/C#, dashboards ou aplicações Frontend em tempo real.

Quando a área retorna a um estado seguro, o arquivo é removido automaticamente para liberar o status do ecossistema.

### 📋 Logs de Auditoria Espacial (`historico_satelite.log`)

Registro persistente de eventos operacionais contendo:

* Análises executadas;
* Mudanças de quadrante;
* Detecções realizadas;
* Eventos críticos do sistema.

### 🌳 Governança de Código (Git & GitHub)

O desenvolvimento seguiu práticas modernas de Engenharia de Software:

* Uso de branches de funcionalidade (`feature/simulador-orbita`);
* Abertura e revisão de Pull Requests (PR);
* Integração controlada na branch principal (`main`).

---

## 🗂️ Estrutura do Repositório

```text
detector-incendio-espacial/
│
├── imagens/                # Imagens de teste do satélite
│
├── main.py                 # Código-fonte principal
├── requirements.txt        # Dependências do projeto
├── .gitignore              # Arquivos ignorados pelo Git
├── historico_satelite.log  # Logs gerados em execução
├── alerta_ativo.json       # Payload gerado em caso de alerta
└── README.md               # Documentação técnica
```

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

* Python 3.10 ou superior instalado;
* Pip atualizado.

### 1. Clonar o Repositório

```bash
git clone https://github.com/saborido613/global-solution-applied-computer-vision-industria-espacial.git
cd GS-APPLIED
```

### 2. Instalar as Dependências

```bash
python -m pip install -r requirements.txt
```

### 3. Executar a Simulação Orbital

```bash
python main.py
```

---

## 🎮 Comandos do Simulador de Órbita

Ao iniciar o sistema, serão abertas:

* 4 janelas visuais de processamento;
* 1 painel de controle para calibração.

### 🎚️ Calibração

Utilize os **Trackbars** para ajustar dinamicamente os parâmetros de detecção térmica em tempo real.

### ⏭️ Tecla `N` (Next)

Avança para o próximo quadrante disponível na pasta `imagens/`, atualizando:

* Logs do sistema;
* Telemetria;
* Payload JSON.

### ❌ Tecla `Q` (Quit)

Encerra a simulação com segurança, fechando todas as janelas e finalizando os processos ativos.

---

## 👥 Integrantes do Grupo

| Nome                | RM      |
| ------------------- | ------- |
| João Pedro Saborido | RM98184 |
| Lucca Alexandre     | RMXXXXX |
| Matheus Haruo       | RMXXXXX |
| Pedro Guerra        | RMXXXXX |
| Victor Wittner      | RMXXXXX |

---

## 📚 Tecnologias Utilizadas

* Python 3
* OpenCV
* NumPy
* JSON
* Git
* GitHub

---

## 🎯 Objetivo Acadêmico

Este projeto foi desenvolvido para a disciplina de **Applied Computer Vision**, simulando um cenário real da indústria espacial e aplicando conceitos de:

* Processamento Digital de Imagens (PDI);
* Visão Computacional;
* Programação Orientada a Objetos (POO);
* Telemetria e integração de sistemas;
* Boas práticas de Engenharia de Software.
