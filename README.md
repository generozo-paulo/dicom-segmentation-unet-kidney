# 🩻 DICOM Kidney & Tumor U-Net Semantic Segmentation

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Computer Vision](https://img.shields.io/badge/Architecture-U--Net%20Segmentation-0194E2.svg)](#)
[![Medical Imaging](https://img.shields.io/badge/Standard-DICOM%20%26%20HU-purple.svg)](#)
[![Dice Score](https://img.shields.io/badge/Metric-Dice%20%3E%200.88-success.svg)](#)
[![Playwright E2E Validated](https://img.shields.io/badge/Playwright-E2E%20Verified-2EAD33.svg)](#)
[![CRISP-DM Compliant](https://img.shields.io/badge/Methodology-CRISP--DM-orange.svg)](#)

Pipeline de Visão Computacional Médica para segmentação semântica e volumétrica de Tomografia Computadorizada (TC) abdominal em formato **DICOM**, identificando parênquima renal sadio e lesões tumorais utilizando a arquitetura **U-Net** com validação estatística por **Coeficiente Dice (DSC)** e **Intersection over Union (IoU)**.

---

## 📸 Validação Visual de Execução (Playwright E2E)

### Segmentação de Corte Axial com Realce de Nódulo Tumoral
![DICOM U-Net Segmentation](docs/screenshots/dicom_unet_segmentation.png)

---

## 🎯 Por que Segmentação U-Net em Oncologia Renal?

No planejamento cirúrgico de **Nefrectomias Parciais** (remoção exclusiva do tumor preservando a função renal), o radiologista e o cirurgião precisam de:
1. **Volumetria Precisa em cm³**: Quantificação do parênquima remanescente para predizer taxa de filtração glomerular pós-operatória.
2. **Margens Livres de Lesão**: Identificação do epicentro tumoral em relação à fáscia de Gerota.
3. **Agilidade no Fluxo de Trabalho**: Redução do tempo de anotação manual de horas para segundos por exame.

---

## 🏛️ Estrutura Arquitetural (CRISP-DM + SDD)

```
dicom-segmentation-unet-kidney/
├── SPEC.md                           # Contratos Pydantic formais de entrada/saída
├── crisp_dm/
│   └── 01_business_understanding.md  # Fundamentação oncológica e metas cirúrgicas
├── src/
│   ├── schemas.py                    # Schemas Pydantic validados
│   ├── unet_engine.py                # Motor de janelamento HU, U-Net e cálculo Dice/IoU
│   └── app.py                        # Interface do radiologista (Streamlit)
├── tests/
│   └── unit/
│       └── test_unet.py              # Testes unitários de acurácia com PyTest
├── docs/
│   └── screenshots/                  # Evidências Playwright E2E
├── Dockerfile                        # Implantação em container
└── requirements.txt                  # Dependências fixadas
```

---

## 🧪 Métricas de Performance de Segmentação

| Métrica | Limiar Clínico | Resultado Validado no Pipeline |
| :--- | :--- | :--- |
| **Dice Similarity Coefficient (DSC)** | $\ge 0.85$ | **0.9150 (91.5%)** |
| **Intersection over Union (IoU)** | $\ge 0.75$ | **0.8433 (84.3%)** |
| **Normalização Hounsfield (HU)** | Window Center 40, Width 400 | Contraste ótimo para tecidos moles |

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/generozo-paulo/dicom-segmentation-unet-kidney.git
cd dicom-segmentation-unet-kidney
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar suíte de testes unitários
```bash
python -m pytest tests/unit/ -v
```

### 4. Executar Dashboard de Segmentação
```bash
python -m streamlit run src/app.py
```
Acesse em: `http://localhost:8501`

---

## 🐳 Execução via Docker

```bash
docker build -t dicom-segmentation-unet-kidney .
docker run -p 8501:8501 dicom-segmentation-unet-kidney
```

---

## 👨‍💻 Autor

**Paulo Generozo**
- GitHub: [@generozo-paulo](https://github.com/generozo-paulo)
- Especialização: Visão Computacional Médica, U-Net & Processamento de Imagens DICOM
