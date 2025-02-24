import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image
import io

# Mock medication database
medications_db = {
    "lisinopril": {
        "common_dosages": ["5mg", "10mg", "20mg"],
        "max_daily": "40mg",
        "interactions": ["potassium supplements", "spironolactone"],
        "patient_instructions": "Take once daily. May cause dizziness."
    },
    "metformin": {
        "common_dosages": ["500mg", "850mg", "1000mg"],
        "max_daily": "2000mg",
        "interactions": ["alcohol", "contrast dyes"],
        "patient_instructions": "Take with meals to reduce stomach upset."
    }
    # Add more medications as needed
}

def preprocess_image(image):
    # Convert to OpenCV format
    img_array = np.array(image)
    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    # Apply thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

def extract_text(image):
    processed_img = preprocess_image(image)
    text = pytesseract.image_to_string(processed_img)
    return text

def verify_prescription(medication, dosage, frequency, patient_data):
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

# Streamlit UI
st.title("AI Prescription Verification System")

# Patient information section
st.header("Patient Information")
col1, col2 = st.columns(2)

with col1:
    patient_name = st.text_input("Patient Name", "John Doe")
    patient_age = st.number_input("Patient Age", 18, 100, 45)

with col2:
    current_meds = st.text_input("Current Medications (comma separated)", "atorvastatin, aspirin")
    allergies = st.text_input("Allergies (comma separated)", "penicillin, sulfa")

# Create patient data dictionary
patient_data = {
    "name": patient_name,
    "age": patient_age,
    "current_medications": [med.strip().lower() for med in current_meds.split(",") if med.strip()],
    "allergies": [allergy.strip().lower() for allergy in allergies.split(",") if allergy.strip()]
}

# Prescription upload
st.header("Prescription Upload")
uploaded_file = st.file_uploader("Upload prescription image", type=["jpg", "jpeg", "png"])

# Manual override section (for demo purposes)
st.header("Manual Entry (or OCR Results)")
medication = st.text_input("Medication", "")
dosage = st.text_input("Dosage", "")
frequency = st.text_input("Frequency", "")

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Prescription", use_column_width=True)
    
    # Extract text using OCR
    if st.button("Extract Text from Image"):
        with st.spinner("Processing image..."):
            text = extract_text(image)
            st.text_area("Extracted Text", text, height=150)
            
            # In a real app, you would implement NLP here to extract medication, dosage, etc.
            # For demo, we'll just use the first few words as a placeholder
            if not medication:
                words = text.split()
                if len(words) > 0:
                    medication = words[0]
                if len(words) > 1:
                    dosage = words[1]
                if len(words) > 2:
                    frequency = words[2]

# Verify prescription
if st.button("Verify Prescription"):
    if medication:
        issues, instructions = verify_prescription(
            medication, 
            dosage, 
            frequency, 
            patient_data
        )
        
        # Display results
        st.header("Verification Results")
        st.subheader("Medication Details")
        st.write(f"**Medication:** {medication}")
        st.write(f"**Dosage:** {dosage}")
        st.write(f"**Frequency:** {frequency}")
        
        # Display issues
        st.subheader("Issues Found")
        if not issues:
            st.success("No issues found with this prescription.")
        else:
            for issue in issues:
                st.error(issue)
        
        # Display patient instructions
        if instructions:
            st.subheader("Patient Instructions")
            st.info(instructions)
            
            # Generate printable instructions button
            if st.button("Generate Printable Instructions"):
                st.download_button(
                    label="Download Instructions PDF",
                    data=f"Patient: {patient_name}\nMedication: {medication}\nDosage: {dosage}\nFrequency: {frequency}\n\nInstructions: {instructions}",
                    file_name=f"{patient_name}_instructions.txt",
                    mime="text/plain"
                )
    else:
        st.error("Please enter a medication name.")

# Add explanatory text at the bottom
st.markdown("---")
st.caption("This is a prototype system for the AI Hackathon. It demonstrates how AI can assist in verifying prescriptions and generating patient instructions.")
