# CRISP-DM: Entendimento de Negócio (Segmentação Renal em Imagens Médicas)

## 1. Problema Clínico
O diagnóstico de carcinoma de células renais (CCR) e o planejamento pré-operatório para nefrectomia parcial exigem volumetria exata de tecido renal sadio e margem cirúrgica do tumor.
A delimitação manual corte a corte em Tomografia Computadorizada (TC) de 512x512 pixels é extremamente lenta e sujeita a alta variabilidade intra-observador.

## 2. Solução Baseada em U-Net
- Normalização Hounsfield Unit (HU) específica para abdome.
- Arquitetura U-Net com skip connections para preservar detalhes morfológicos finos de cápsula renal.
- Coeficiente Dice $> 0.88$ para parênquima renal como critério de aceitação clínica.
