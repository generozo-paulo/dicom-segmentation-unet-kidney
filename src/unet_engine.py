import numpy as np
from typing import Tuple, Dict
from src.schemas import DicomSlicePayload, SegmentationMetricsResult

class UNetKidneySegmentationEngine:
    """
    Motor de processamento de imagem médica e segmentação volumétrica renal (U-Net).
    """

    @staticmethod
    def generate_synthetic_ct_slice(size: int = 128, with_tumor: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """Gera imagem sintética de CT abdominal e respectiva máscara de anotação médica (Ground Truth)."""
        # Fundo anatômico (0 = ar/músculo base)
        ct_slice = np.zeros((size, size), dtype=np.float32) + 20.0
        mask_gt = np.zeros((size, size), dtype=np.int32) # 0: Fundo, 1: Rim, 2: Tumor

        # Rim Esquerdo (elipse anatômica)
        y, x = np.ogrid[:size, :size]
        center_y, center_x = size // 2, size // 3
        kidney_area = ((x - center_x)**2 / (size*0.18)**2 + (y - center_y)**2 / (size*0.32)**2) <= 1.0
        ct_slice[kidney_area] = 120.0 # atenuação de tecido renal em HU
        mask_gt[kidney_area] = 1

        if with_tumor:
            tumor_y, tumor_x = center_y + 10, center_x + 8
            tumor_area = ((x - tumor_x)**2 / (size*0.08)**2 + (y - tumor_y)**2 / (size*0.08)**2) <= 1.0
            ct_slice[tumor_area] = 160.0 # hiperecogenicidade/contraste tumoral
            mask_gt[tumor_area] = 2

        # Adiciona ruído gaussiano típico de TC de baixa dosagem
        noise = np.random.normal(loc=0, scale=8.0, size=(size, size))
        ct_slice = np.clip(ct_slice + noise, -100, 300)
        return ct_slice, mask_gt

    @staticmethod
    def calculate_dice_iou(ground_truth: np.ndarray, prediction: np.ndarray) -> Tuple[float, float]:
        """Calcula Coeficiente Dice e IoU binários."""
        intersection = np.logical_and(ground_truth > 0, prediction > 0).sum()
        total_gt = (ground_truth > 0).sum()
        total_pred = (prediction > 0).sum()

        if total_gt + total_pred == 0:
            return 1.0, 1.0

        dice = (2.0 * intersection) / (total_gt + total_pred)
        union = total_gt + total_pred - intersection
        iou = intersection / union if union > 0 else 0.0
        return float(dice), float(iou)

    @staticmethod
    def run_inference_segmentation(payload: DicomSlicePayload) -> Tuple[SegmentationMetricsResult, np.ndarray]:
        ct, mask_gt = UNetKidneySegmentationEngine.generate_synthetic_ct_slice(with_tumor=payload.simulated_tumor_present)

        # Simulação de predição U-Net com acurácia alta (Dice ~0.92)
        prediction = mask_gt.copy()
        # Adiciona pequenas perturbações de borda cirúrgica
        perturbation = np.random.rand(*prediction.shape) < 0.04
        prediction[perturbation] = 0

        dice, iou = UNetKidneySegmentationEngine.calculate_dice_iou(mask_gt, prediction)

        kidney_pixels = (prediction == 1).sum()
        tumor_pixels = (prediction == 2).sum()

        # Conversão de pixels para cm3 (assumindo espaçamento de 0.8mm x 0.8mm e slice thickness de 2mm)
        voxel_vol_cm3 = (0.08 * 0.08 * 0.2)
        kidney_vol = round(float(kidney_pixels * voxel_vol_cm3), 2)
        tumor_vol = round(float(tumor_pixels * voxel_vol_cm3), 2)

        has_tumor = tumor_pixels > 0
        if tumor_vol >= 15.0:
            alert = "ADVANCED_TUMOR"
        elif has_tumor:
            alert = "SUSPICIOUS_MASS_STAGE_1"
        else:
            alert = "NORMAL"

        metrics = SegmentationMetricsResult(
            slice_id=f"SLICE-{payload.patient_id}-{payload.slice_index:03d}",
            dice_coefficient=round(dice, 4),
            iou_score=round(iou, 4),
            kidney_volume_cm3=kidney_vol,
            tumor_detected=has_tumor,
            tumor_volume_cm3=tumor_vol,
            radiologist_alert=alert
        )

        return metrics, prediction
