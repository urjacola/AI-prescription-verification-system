import cv2
import numpy as np
import pytesseract
from PIL import Image

def preprocess_image(image):
    """Preprocess the image for OCR"""
    img_array = np.array(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

def extract_text(image):
    """Extract text from prescription image"""
    processed_img = preprocess_image(image)
    text = pytesseract.image_to_string(processed_img)
    return text

def verify_prescription(medication, dosage, frequency, patient_data, medications_db):
    """Verify prescription against medication database and patient data"""
    issues = []
    
    # Check if medication exists
    if medication.lower() not in medications_db:
        issues.append(f"Unknown medication: {medication}")
        return issues, ""
    
    med_info = medications_db[medication.lower()]
    
    # Check dosage
    if dosage not in med_info["common_dosages"]:
        issues.append(f"Unusual dosage: {dosage}")
    
    # Check for interactions with patient's medications
    for current_med in patient_data["current_medications"]:
        if current_med in med_info["interactions"]:
            issues.append(f"Potential interaction with {current_med}")
    
    # Check for allergies
    if medication.lower() in patient_data["allergies"]:
        issues.append(f"Patient has known allergy to {medication}")
        
    return issues, med_info.get("patient_instructions", "")
