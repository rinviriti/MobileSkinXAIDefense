# Defense inventory

## Ten editable tables

- `evaluation/metrics_tables/Table_01_Dataset_Composition_and_Frozen_Splits.csv` plus Markdown version
- `evaluation/metrics_tables/Table_02_Historical_Full_PAD_Source_Only_Results.csv` plus Markdown version
- `evaluation/metrics_tables/Table_03_Final_E1_Source_Only_Test_Results.csv` plus Markdown version
- `evaluation/metrics_tables/Table_04_Final_E2_Joint_Domain_Test_Results.csv` plus Markdown version
- `evaluation/metrics_tables/Table_05_Complete_Four_Setting_Classification_Comparison.csv` plus Markdown version
- `evaluation/metrics_tables/Table_06_PAD_Improvements_and_ISIC_Tradeoffs.csv` plus Markdown version
- `evaluation/metrics_tables/Table_07_PAD_Classwise_Precision_Recall_and_F1.csv` plus Markdown version
- `evaluation/metrics_tables/Table_08_Melanoma_and_SCC_Exact_Detections.csv` plus Markdown version
- `evaluation/metrics_tables/Table_09_Model_Efficiency_Training_and_Selected_Checkpoints.csv` plus Markdown version
- `evaluation/metrics_tables/Table_10_Prior_Ablations_and_Teacher_Qualification.csv` plus Markdown version

## Research figures (56 PNGs) and editable SVGs

- `evaluation/ablations/CA_MACL_Matched_Seed_Validation_Stability.png`
- `evaluation/ablations/CA_MACL_Source_Development_Component_Findings.png`
- `evaluation/ablations/Original_Enhancement_Ablation_Findings.png`
- `evaluation/classwise/Classwise_F1_and_BCC_Minority_Tradeoffs.png`
- `evaluation/classwise/Four_Class_PAD_Recall_E1_vs_E2.png`
- `evaluation/classwise/Melanoma_and_SCC_Exact_Detections_E1_vs_E2.png`
- `evaluation/confusion_matrices/ConvNeXt-Tiny_E1_vs_E2_Confusion_Matrix.png`
- `evaluation/confusion_matrices/EfficientNet-Lite0_E1_vs_E2_Confusion_Matrix.png`
- `evaluation/confusion_matrices/MobileNetV3-Small_E1_vs_E2_Confusion_Matrix.png`
- `evaluation/confusion_matrices/MobileNetV4-Conv-Small_E1_vs_E2_Confusion_Matrix.png`
- `evaluation/confusion_matrices/MobileSkinXAI-Enhanced_E1_vs_E2_Confusion_Matrix.png`
- `evaluation/confusion_matrices/MobileSkinXAI-Enhanced_LR_Control_E1_vs_E2_Confusion_Matrix.png`
- `evaluation/cross_dataset/Four_Setting_Cross_Dataset_Macro_F1.png`
- `evaluation/cross_dataset/Historical_Full_PAD_vs_Current_Fixed_PAD_Source_Only.png`
- `evaluation/cross_dataset/PAD_Adaptation_Gains_and_ISIC_Tradeoffs.png`
- `evaluation/cross_dataset/Source_Target_Differences_and_Tradeoff.png`
- `evaluation/efficiency/Inference_Parameters_and_MACs.png`
- `evaluation/efficiency/PAD_Validation_Performance_vs_Inference_Complexity.png`
- `evaluation/efficiency/Training_Cost_and_Shared_Parents.png`
- `evaluation/metrics_tables/Table_01_Dataset_Composition_and_Frozen_Splits.png`
- `evaluation/metrics_tables/Table_05_Complete_Four_Setting_Classification_Comparison.png`
- `evaluation/metrics_tables/Table_08_Melanoma_and_SCC_Exact_Detections.png`
- `evaluation/model_comparisons/ISIC_Test_Classification_Comparison.png`
- `evaluation/model_comparisons/Six_Model_E1_vs_E2_PAD_Classification.png`
- `evaluation/model_comparisons/Validation_Selection_vs_PAD_Test_Point_Estimates.png`
- `evaluation/roc_curves/ConvNeXt-Tiny_Fixed_PAD_PR.png`
- `evaluation/roc_curves/ConvNeXt-Tiny_Fixed_PAD_ROC.png`
- `evaluation/roc_curves/EfficientNet-Lite0_Fixed_PAD_PR.png`
- `evaluation/roc_curves/EfficientNet-Lite0_Fixed_PAD_ROC.png`
- `evaluation/roc_curves/MobileNetV3-Small_Fixed_PAD_PR.png`
- `evaluation/roc_curves/MobileNetV3-Small_Fixed_PAD_ROC.png`
- `evaluation/roc_curves/MobileNetV4-Conv-Small_Fixed_PAD_PR.png`
- `evaluation/roc_curves/MobileNetV4-Conv-Small_Fixed_PAD_ROC.png`
- `evaluation/roc_curves/MobileSkinXAI-Enhanced_Fixed_PAD_PR.png`
- `evaluation/roc_curves/MobileSkinXAI-Enhanced_Fixed_PAD_ROC.png`
- `evaluation/roc_curves/MobileSkinXAI-Enhanced_LR_Control_Fixed_PAD_PR.png`
- `evaluation/roc_curves/MobileSkinXAI-Enhanced_LR_Control_Fixed_PAD_ROC.png`
- `evaluation/training_curves/Joint_Training_and_Validation_Loss_Curves.png`
- `evaluation/training_curves/PAD_Validation_Learning_and_LR_Control.png`
- `figures/architecture/ConvNeXt-Tiny_architecture.png`
- `figures/architecture/EfficientNet-Lite0_architecture.png`
- `figures/architecture/MobileNetV3-Small_architecture.png`
- `figures/architecture/MobileNetV4-Conv-Small_architecture.png`
- `figures/architecture/MobileSkinXAI-Enhanced_LR_Control_architecture.png`
- `figures/architecture/MobileSkinXAI-Enhanced_architecture.png`
- `figures/dataset/Frozen_Dataset_Partitions.png`
- `figures/dataset/ISIC_vs_PAD_Class_Distribution.png`
- `figures/dataset/PAD_Patient_Disjoint_Class_and_Melanoma_Support.png`
- `figures/flutter_screenshots/Existing_Home_Headless.png`
- `figures/gradcam/MobileSkinXAI-Enhanced_LR_Control_BCC_Correct_Grad_CAM.png`
- `figures/gradcam/MobileSkinXAI-Enhanced_LR_Control_MEL_Correct_Grad_CAM.png`
- `figures/gradcam/MobileSkinXAI-Enhanced_LR_Control_MEL_Incorrect_Grad_CAM.png`
- `figures/gradcam/MobileSkinXAI-Enhanced_LR_Control_NV_Correct_Grad_CAM.png`
- `figures/gradcam/MobileSkinXAI-Enhanced_LR_Control_SCC_Correct_Grad_CAM.png`
- `figures/gradcam/MobileSkinXAI-Enhanced_LR_Control_SCC_Incorrect_Grad_CAM.png`
- `figures/training_samples/PAD_Training_Examples.png`

## Source layout

Original training/evaluation paths are intentionally preserved. `training/configs/` contains six exact E2 configs; architecture factory and original training code are included. `final_training/`, `research/thesis_assets/`, and `scripts/` retain original controllers and provenance. No trained weights, membership manifests or raw datasets are included.

Existing Flutter platforms: Android, iOS, Linux, macOS, Windows and web scaffolding. Runtime service imports dart:io/FFI and is intended for native targets; web scaffolding is not a verified web inference implementation.

App screenshots: three existing project PNGs under app/flutter/screenshots; one actual headless capture under figures/flutter_screenshots. None establishes physical-device success.
