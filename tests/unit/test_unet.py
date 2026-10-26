import pytest
import numpy as np
from src.schemas import DicomSlicePayload
from src.unet_engine import UNetKidneySegmentationEngine

def test_ct_generation():
    ct, mask = UNetKidneySegmentationEngine.generate_synthetic_ct_slice(size=64, with_tumor=True)
    assert ct.shape == (64, 64)
    assert mask.shape == (64, 64)
    assert 1 in mask # rim
    assert 2 in mask # tumor

def test_dice_iou_calculation():
    m1 = np.ones((10, 10))
    m2 = np.ones((10, 10))
    dice, iou = UNetKidneySegmentationEngine.calculate_dice_iou(m1, m2)
    assert dice == 1.0
    assert iou == 1.0

def test_segmentation_inference_with_tumor():
    payload = DicomSlicePayload(patient_id="TEST-01", slice_index=15, simulated_tumor_present=True)
    metrics, pred = UNetKidneySegmentationEngine.run_inference_segmentation(payload)
    assert metrics.dice_coefficient >= 0.85
    assert metrics.iou_score >= 0.75
    assert metrics.tumor_detected is True
    assert metrics.kidney_volume_cm3 > 0.0
