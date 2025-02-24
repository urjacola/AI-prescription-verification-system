# AI-prescription-verification-system
# AI-Powered Prescription Verification System

A prototype system that verifies prescription information and generates patient-friendly instructions.

Prerequisites

This application requires Tesseract OCR to be installed on your system.

 Installing Tesseract OCR:

- **Windows**: Download and install from [here](https://github.com/UB-Mannheim/tesseract/wiki)


Features
- Prescription image processing and text extraction
- Medication verification against a database
- Patient-specific interaction checking
- Automated patient instruction generation

 Running Locally
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run streamlit_app.py`

 Deployment
This application is deployed on Streamlit Cloud at [your-app-url].

## Project Structure
- `streamlit_app.py`: Main application file
- `sample_images/`: Sample prescription images for testing
- `requirements.txt`: Dependencies

## Demo Instructions
1. Upload a prescription image or use manual entry
2. Enter patient information
3. Click "Verify Prescription" to see results


