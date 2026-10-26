# Especificação Contratual (SDD) - DICOM Segmentation U-Net for Kidney & Tumor

## 1. Escopo & Objetivos
Pipeline de visão computacional médica para segmentação semântica volumétrica de Tomografia Computadorizada (CT) abdominal em formato DICOM.
Segmenta parênquima renal e lesões císticas/tumorais utilizando arquitetura U-Net com cálculo rigoroso de coeficiente Dice (**Dice Similarity Coefficient - DSC**) e Intersection over Union (**IoU**).

## 2. Contratos de Entrada (Pydantic)

### 2.1 Requisição de Segmentação DICOM (`DicomSlicePayload`)
- `patient_id`: str
- `slice_index`: int
- `window_center_hu`: float = 40.0 # Hounsfield Units para tecido mole
- `window_width_hu`: float = 400.0
- `simulated_tumor_present`: bool = True

## 3. Contratos de Saída (Pydantic)

### 3.1 Métricas de Segmentação (`SegmentationMetricsResult`)
- `slice_id`: str
- `dice_coefficient`: float = Field(ge=0.0, le=1.0)
- `iou_score`: float = Field(ge=0.0, le=1.0)
- `kidney_volume_cm3`: float
- `tumor_detected`: bool
- `tumor_volume_cm3`: float
- `radiologist_alert`: Literal["NORMAL", "SUSPICIOUS_MASS_STAGE_1", "ADVANCED_TUMOR"]
