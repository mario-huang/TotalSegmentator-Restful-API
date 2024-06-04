from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from totalsegmentator.python_api import totalsegmentator

class RequestBody(BaseModel):
    input: str = Field(..., description="CT nifti image or folder of dicom slices")
    output: str = Field(None, description="Output directory for segmentation masks")
    ml: bool = Field(True, description="Save one multilabel image for all classes")
    nr_thr_resamp: int = Field(1, description="Nr of threads for resampling")
    nr_thr_saving: int = Field(6, description="Nr of threads for saving segmentations")
    fast: bool = Field(False, description="Run faster lower resolution model (3mm)")
    nora_tag: str = Field("None", description="tag in nora as mask. Pass nora project id as argument.")
    preview: bool = Field(False, description="Generate a png preview of segmentation")
    task: str = Field("total", description="Select which model to use. This determines what is predicted. Choices: total, body, lung_vessels, cerebral_bleed, hip_implant, coronary_arteries, pleural_pericard_effusion, test, appendicular_bones, tissue_types, heartchambers_highres, face, vertebrae_body")
    roi_subset: str = Field(None, description="Define a subset of classes to save (space separated list of class names). If running 1.5mm model, will only run the appropriate models for these rois.")
    statistics: bool = Field(False, description="Calc volume (in mm3) and mean intensity. Results will be in statistics.json")
    radiomics: bool = Field(False, description="Calc radiomics features. Requires pyradiomics. Results will be in statistics_radiomics.json")
    crop_path: str = Field(None, description="Custom path to masks used for cropping. If not set will use output directory.")
    body_seg: bool = Field(False, description="Do initial rough body segmentation and crop image to body region")
    force_split: bool = Field(False, description="Process image in 3 chunks for less memory consumption. (do not use on small images)")
    output_type: str = Field("nifti", description="Select if segmentations shall be saved as Nifti or as Dicom RT Struct image. Choices: nifti, dicom")
    quiet: bool = Field(False, description="Print no intermediate outputs")
    verbose: bool = Field(False, description="Show more intermediate output")
    test: int = Field(0, description="Only needed for unittesting. Choices: 0, 1, 3")
    skip_saving: bool = Field(False, description="Skip saving of segmentations for faster runtime if you are only interested in statistics.")
    device: str = Field("gpu", description="Device to run on (default: gpu). Choices: gpu, cpu, mps")
    license_number: str = Field(None, description="Set license number. Needed for some tasks. Only needed once, then stored in config file.")
    statistics_exclude_masks_at_border: bool = Field(True, description="Normally statistics are only calculated for ROIs which are not cut off by the beginning or end of image. Use this option to calc anyways.")
    no_derived_masks: bool = Field(False, description="Do not create derived masks (e.g. skin from body mask).")
    v1_order: bool = Field(False, description="In multilabel file order classes as in v1. New v2 classes will be removed.")
    fastest: bool = Field(False, description="Run even faster lower resolution model (6mm)")
    roi_subset_robust: str = Field(None, description="Like roi_subset but uses a slower but more robust model to find the rois.")

app = FastAPI()

@app.post("/segment")
async def segment(body: RequestBody = Body(...)):
    """
    Run segment from api.
    """
    try:
        totalsegmentator(**body.model_dump())
    except Exception as e:
        return {"code": 0, "message": "totalsegmentator failed.\n" + str(e)}
    else:
        return {"code": 200, "message": "totalsegmentator succeed."}

