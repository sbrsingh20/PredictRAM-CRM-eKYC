import streamlit as st
import random
from fpdf import FPDF

# Function to generate PDF from form data
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add eKYC Details
    pdf.cell(200, 10, txt="eKYC and Agreement Details", ln=True, align='C')
    pdf.cell(200, 10, txt="eKYC Details", ln=True, align='L')
    
    for key, value in data['ekyc'].items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    # Add Agreement Details
    pdf.cell(200, 10, txt="Investment Advisor Agreement Details", ln=True, align='L')
    for key, value in data['agreement'].items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    # Save PDF to local file system
    pdf_output = "eKYC_Agreement_Details.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Step 1: EKYC Form
def ekyc_form():
    st.title("eKYC Form")
    
    # Collecting user information
    full_name = st.text_input("Full Name as per official records")
    dob = st.date_input("Date of Birth")
    address = st.text_area("Address")
    photo = st.file_uploader("Upload a recent passport-size photo", type=["jpg", "jpeg", "png"])
    email = st.text_input("Email ID")
    mobile = st.text_input("Mobile Number")
    pan = st.text_input("PAN (Permanent Account Number)")
    bank_account = st.text_input("Bank Account Details (optional)")
    aadhar_number = st.text_input("Aadhar Number")
    
    # Simulate OTP (generated once for verification)
    if aadhar_number:
        aadhar_otp = random.randint(1000, 9999)  # Simulate Aadhar OTP generation
        otp_input = st.text_input(f"Enter OTP sent to Aadhar Number {aadhar_number}:", key="otp_input")
        
        if otp_input:
            if otp_input == str(aadhar_otp):
                st.success("eKYC Verified and Agreement Signed Successfully!")
                
                # Collecting the data for PDF generation
                ekyc_data = {
                    "Full Name": full_name,
                    "Date of Birth": dob,
                    "Address": address,
                    "Email ID": email,
                    "Mobile Number": mobile,
                    "PAN": pan,
                    "Bank Account": bank_account,
                    "Aadhar Number": aadhar_number
                }

                # Agreement Details
                agreement_data = {
                    "Investment Advisor": "[Advisor Name], [Firm Name], [Address]",
                    "Effective Date": "[Effective Date of Agreement]",
                    "Scope of Services": "The Advisor will provide portfolio management, investment advice, and monitoring.",
                    "Client's Responsibilities": "The client agrees to provide accurate financial data and make investment decisions.",
                    "Fees and Compensation": "The Client agrees to pay [Fee Structure] on a [monthly/quarterly/annually] basis."
                }
                
                # Combine both sets of data (eKYC and Agreement)
                data = {
                    'ekyc': ekyc_data,
                    'agreement': agreement_data
                }
                
                # Generate and provide the PDF download link
                pdf_file = generate_pdf(data)
                with open(pdf_file, "rb") as pdf:
                    st.download_button("Download eKYC and Agreement PDF", pdf, file_name="eKYC_Agreement_Details.pdf", mime="application/pdf")
            else:
                st.warning("Invalid OTP. Please try again.")
    
    return full_name, address, aadhar_number

# Main logic to handle the flow
def main():
    client_name, client_address, client_aadhar = ekyc_form()  # Run EKYC Form

if __name__ == "__main__":
    main()
