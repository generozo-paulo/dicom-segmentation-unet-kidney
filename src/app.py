import streamlit as st
import numpy as np
import plotly.express as px
from src.schemas import DicomSlicePayload
from src.unet_engine import UNetKidneySegmentationEngine

st.set_page_config(
    page_title="DICOM Kidney & Tumor U-Net Segmentation",
    page_icon="🩻",
    layout="wide"
)

st.title("🩻 DICOM Kidney & Tumor U-Net Semantic Segmentation")
st.markdown("""
Segmentação volumétrica automatizada de parênquima renal e nódulos/tumores em Tomografia Computadorizada (TC) de abdome com cálculo de **Coeficiente Dice** e **IoU**.
""")

col_ctrl, col_view = st.columns([1, 2])

with col_ctrl:
    st.subheader("⚙️ Configurações do Corte DICOM")
    patient_id = st.text_input("ID do Paciente", "PAC-KIDNEY-082")
    slice_idx = st.slider("Índice do Corte Axial (Z-Axis)", 1, 64, 28)
    sim_tumor = st.checkbox("Simular Lesão Tumoral / Nódulo", value=True)
    wc = st.slider("Window Center (HU)", 0, 100, 40)
    ww = st.slider("Window Width (HU)", 200, 800, 400)

    payload = DicomSlicePayload(
        patient_id=patient_id,
        slice_index=slice_idx,
        window_center_hu=wc,
        window_width_hu=ww,
        simulated_tumor_present=sim_tumor
    )

    metrics, pred_mask = UNetKidneySegmentationEngine.run_inference_segmentation(payload)

    st.markdown("### 📊 Métricas de Validação U-Net")
    st.metric("Coeficiente Dice (DSC)", f"{metrics.dice_coefficient:.2%}")
    st.metric("Intersection over Union (IoU)", f"{metrics.iou_score:.2%}")
    st.metric("Volume Renal Estimado", f"{metrics.kidney_volume_cm3} cm³")
    if metrics.tumor_detected:
        st.error(f"🚨 Tumor Detectado: {metrics.tumor_volume_cm3} cm³ ({metrics.radiologist_alert})")
    else:
        st.success("✅ Parênquima Renal Íntegro (Sem nódulos detectados)")

with col_view:
    st.subheader("Visualização do Corte e Máscara Segmentada")
    ct_img, gt_mask = UNetKidneySegmentationEngine.generate_synthetic_ct_slice(with_tumor=sim_tumor)

    # Criação de visualização com overlay da máscara U-Net
    fig = px.imshow(
        ct_img,
        color_continuous_scale="gray",
        title=f"Corte TC Abdominal com Máscara U-Net ({metrics.slice_id})"
    )
    fig.update_layout(height=500, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Legenda de Segmentação:**
    - Região Cinza Central: Parênquima Renal Normal
    - Região com Contraste Realçado: Lesão Tumoral / Suspeita Cirúrgica
    """)
