# 🚀 Sistema Orbital de Detecção de Anomalias Térmicas e Resposta Rápida (S.O.D.A.R.)

> 📢 **LINK DO VÍDEO DE APRESENTAÇÃO (PITCH):** https://youtu.be/QZWA2FYBBvA

## 🌌 Contexto da Solução (Global Solution - Indústria Espacial)
No cenário da "New Space", onde constelações de microssatélites redefinem a economia global, o **S.O.D.A.R.** surge como uma solução de Inteligência Artificial de ponta. O projeto simula o monitoramento de um satélite de órbita baixa (LEO) para classificar imagens terrestres e mitigar um dos maiores problemas ambientais e econômicos do planeta: **os incêndios florestais e o desmatamento ilegal**.

Este componente representa o motor de **Applied Computer Vision** do ecossistema integrado desenvolvido pelo nosso grupo, atuando através de uma arquitetura híbrida que une Processamento Digital de Imagens (PDI) na borda e classificação autônoma por Deep Learning na base.

---

## 🛠️ Arquitetura Híbrida do Sistema

### 1. Processamento Digital de Imagens de Borda (`main.py`)
Utilizando **OpenCV** e **NumPy** sob os princípios de POO (`DetectorIncendioSatelital`), esta frente simula o satélite em órbita executando tarefas de baixo consumo computacional (ideal para restrições de bateria no espaço):
* **Filtro Espacial:** Conversão de BGR para o espaço de cores **HSV** para isolar o canal de brilho (Value) de reflexos solares nas nuvens e focar no espectro térmico puro (Hue e Saturation).
* **Morfologia Matemática:** Operação de abertura (`MORPH_OPEN`) com kernel $3 \times 3$ para eliminação de ruídos de transmissão.
* **Extração de Contornos:** Rastreamento dinâmico via `findContours` para delimitar geograficamente e extrair áreas de possíveis focos em tempo real com *Bounding Boxes*.

### 2. Classificação de Imagens por Deep Learning (`.ipynb`)
Desenvolvido em **TensorFlow/Keras** com aceleração por GPU T4 no Google Colab, o sistema processa os alvos suspeitos através de Redes Neurais Convolucionais próprias. Foram criadas **duas arquiteturas do zero**, sem modelos pré-treinados:
* **CNN Simples (Modelo 1):** Duas camadas convolucionais sequenciais com ativação ReLU e `MaxPooling2D`. Apresentou oscilações na curva de perda.
* **CNN Robusta (Modelo 2):** Três camadas convolucionais progressivas (filtros 32, 64 e 128) incorporando uma estratégia de regularização por **Dropout (30%)**. O Dropout mitigou com sucesso o *overfitting*, forçando a rede a generalizar a assinatura real do fogo em diferentes terrenos vegetais.

---

## 📊 Avaliação Técnica de Desempenho e Métricas

O treinamento foi acompanhado ao longo de 15 épocas e avaliado de forma quantitativa e qualitativa:

* **Acurácia Superior a 88%:** Conforme exigido pela demanda, a **CNN Robusta (Modelo 2)** alcançou estabilidade ideal ultrapassando a meta de referência no conjunto de validação.
* **Matriz de Confusão (`matriz_confusao.png`):** Exportada diretamente do pipeline de validação, demonstra precisão total na segregação das classes `floresta` e `incendio`, sem a ocorrência de falsos positivos ou falsos negativos.
* **Análise Qualitativa (`exemplos_predicao.png`):** O notebook renderiza cards visuais de amostras inéditas do dataset confrontando o rótulo real com a predição certeira da IA (identificados em verde no relatório visual).

---

## 🗂️ Estrutura Final do Repositório

```text
GS-APPLIED/
│
├── imagens/                    # Imagens originais de quadrantes para o simulador OpenCV
│
├── main.py                     # Motor de processamento OpenCV (Simulador de Órbita de Borda)
├── SODAR_Treinamento_CNN.ipynb # Jupyter Notebook completo (Construção, Treino e Métricas da IA)
├── modelo_cnn_robusto.h5       # Pesos salvos do melhor modelo treinado (Obrigatório)
│
├── comparacao_modelos_cnn.png  # Gráfico de evolução de Acurácia e Loss
├── matriz_confusao.png         # Gráfico com a matriz de confusão do modelo vencedor
├── exemplos_predicao.png       # Amostra qualitativa de acertos/erros da predição
│
├── requirements.txt            # Dependências do projeto (TensorFlow, OpenCV, NumPy, Matplotlib)
└── README.md                   # Documentação técnica oficial e identificação
```

---

# 🚀 Como Executar o Projeto

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de possuir:

* Python **3.10** ou superior;
* Acesso ao **Google Colab** ou a um ambiente **Jupyter Notebook** local;
* Git instalado na máquina.

---

## 📥 1. Clonar o Repositório

Clone o projeto e acesse o diretório:

```bash
git clone https://github.com/saborido613/global-solution-applied-computer-vision-industria-espacial.git
cd GS-APPLIED
```

---

## 🛰️ 2. Executar o Simulador Orbital (OpenCV)

Instale as dependências do projeto:

```bash
python -m pip install -r requirements.txt
```

Em seguida, execute a aplicação:

```bash
python main.py
```

### 🎮 Controles

| Tecla | Ação                                       |
| ----- | ------------------------------------------ |
| `n`   | Avança o satélite para o próximo quadrante |
| `q`   | Encerra a aplicação com segurança          |

A interface utiliza **trackbars do OpenCV** para realizar a calibração e ajuste da detecção de bordas em tempo real.

---

## 🤖 3. Executar o Pipeline de Deep Learning

1. Abra o **Google Colab**;
2. Faça o upload do arquivo:

```text
SODAR_Treinamento_CNN.ipynb
```

3. Ative a aceleração por GPU:

```text
Ambiente de execução
└── Alterar tipo de ambiente de execução
    └── GPU T4
```

4. Execute todas as células em sequência.

### 📊 Resultados Gerados

O notebook permite:

* Gerar dados sintéticos para calibração;
* Treinar a rede neural convolucional (CNN);
* Produzir matrizes de confusão;
* Gerar métricas de desempenho;
* Elaborar relatórios analíticos dos resultados.

---

# 👥 Integrantes do Grupo

| Integrante          | RM      |
| ------------------- | ------- |
| João Pedro Saborido | RM98184 |
| Matheus Haruo       | RM97663 |
| Pedro Guerra        | RM99526 |
| Victor Wittner      | RM98667 |

---

# 🛠️ Tecnologias Utilizadas

* Python 3
* OpenCV
* NumPy
* JSON
* Git
* GitHub
* Google Colab
* Jupyter Notebook

---

# 🎯 Objetivo Acadêmico

Este projeto foi desenvolvido para a disciplina de **Applied Computer Vision**, simulando um cenário inspirado na indústria espacial e aplicando conceitos fundamentais de:

* Processamento Digital de Imagens (PDI);
* Visão Computacional;
* Programação Orientada a Objetos (POO);
* Telemetria e integração de sistemas;
* Inteligência Artificial e Deep Learning;
* Boas práticas de Engenharia de Software.

---

## 🌌 Sobre o Projeto

O sistema integra técnicas de **Visão Computacional** e **Aprendizado Profundo** para simular processos de monitoramento e análise de dados em um contexto espacial, combinando:

* Simulação orbital com OpenCV;
* Processamento e calibração de imagens;
* Geração de datasets sintéticos;
* Treinamento de modelos CNN;
* Avaliação automatizada de desempenho.

O objetivo é demonstrar, de forma prática, a aplicação de conceitos estudados ao longo da disciplina em um cenário próximo aos desafios encontrados na indústria aeroespacial.
