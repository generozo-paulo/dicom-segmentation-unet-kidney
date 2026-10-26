from pydantic import BaseModel, Field
from typing import Literal

class DicomSlicePayload(BaseModel):
    patient_id: str
    slice_index: int
    window_center_hu: float = 40.0
    window_width_hu: float = 400.0
    simulated_tumor_present: bool = True

class SegmentationMetricsResult(BaseModel):
    slice_id: str
    dice_coefficient: float = Field(ge=0.0, le=1.0)
    iou_score: float = Field(ge=0.0, le=1.0)
    kidney_volume_cm3: float
    tumor_detected: bool
    tumor_volume_cm3: float
    radiologist_alert: Literal["NORMAL", "SUSPICIOUS_MASS_STAGE_1", "ADVANCED_TUMOR"]
