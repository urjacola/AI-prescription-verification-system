import streamlit as st
from PIL import Image
import io
import numpy as np
from utils import preprocess_image, extract_text, verify_prescription

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
    },
    "atorvastatin": {
        "common_dosages": ["10mg", "20mg", "40mg", "80mg"],
        "max_daily": "80mg",
        "interactions": ["grapefruit juice", "certain antibiotics"],
        "patient_instructions": "Take in the evening. Report unexplained muscle pain."
    },
    "aspirin": {
        "common_dosages": ["81mg", "325mg"],
        "max_daily": "4000mg",
        "interactions": ["blood thinners", "ibuprofen"],
        "patient_instructions": "Take with food to minimize stomach irritation."
    }
    # Add more medications as needed
}

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
            patient_data,
            medications_db  # Pass the database to the function
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
st.caption("This is a prototype system for AI Prescription Verification. It demonstrates how AI can assist in verifying prescriptions and generating patient instructions.")
