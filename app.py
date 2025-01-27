import streamlit as st
import pandas as pd
from fpdf import FPDF
import random

# Function to generate PDF from form data
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="eKYC Details", ln=True, align='C')
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    # Save PDF to local file system
    pdf_output = "eKYC_Details.pdf"
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
    
    # Simulating OTP
    if aadhar_number:
        aadhar_otp = random.randint(1000, 9999)  # Simulate Aadhar OTP generation
        otp_input = st.text_input(f"Enter OTP sent to Aadhar Number {aadhar_number}:", key="otp_input")
        if otp_input and otp_input == str(aadhar_otp):
            st.success("eKYC Verified!")
            
            # Collecting the data for PDF generation
            data = {
                "Full Name": full_name,
                "Date of Birth": dob,
                "Address": address,
                "Email ID": email,
                "Mobile Number": mobile,
                "PAN": pan,
                "Bank Account": bank_account,
                "Aadhar Number": aadhar_number
            }
            
            # Generate and provide the PDF download link
            pdf_file = generate_pdf(data)
            with open(pdf_file, "rb") as pdf:
                st.download_button("Download eKYC PDF", pdf, file_name="eKYC_Details.pdf", mime="application/pdf")
        else:
            st.warning("Invalid OTP. Please try again.")
    
    return full_name, address, aadhar_number

# Step 2: Investment Advisor Agreement
def investment_advisor_agreement(client_name, client_address, client_aadhar):
    st.title("Investment Advisor Agreement")
    
    # Show Agreement Text
    agreement_text = f"""
    Investment Advisor Agreement

    This Investment Advisor Agreement ("Agreement") is made and entered into by and between:

    Client: {client_name}, {client_address}

    and

    Investment Advisor: [Advisor Name], [Firm Name], [Address]

    Effective Date: [Effective Date of Agreement]

    1. Scope of Services
    The Advisor agrees to provide investment advisory services to the Client, which may include the following:
        - Asset allocation and portfolio management advice
        - Recommendations regarding the purchase, sale, or retention of securities
        - Ongoing monitoring and review of the Client's investment portfolio

    2. Client’s Responsibilities
    The Client agrees to:
        - Provide the Advisor with accurate and timely financial information
        - Actively communicate with the Advisor regarding any changes in the Client's financial situation
        - Be responsible for the final decision on all investments

    3. Fees and Compensation
    The Client agrees to pay the Advisor a fee of [Fee Structure] for the services provided under this Agreement. Payment will be made [Payment Terms: e.g., monthly, quarterly, annually].

    Please enter your Aadhar OTP to sign this agreement:
    """
    st.markdown(agreement_text)
    
    # Aadhar OTP for Agreement signing with a unique key
    otp_input = st.text_input(f"Enter OTP sent to Aadhar Number {client_aadhar}:", key="agreement_otp_input")
    if otp_input and otp_input == "1100":
        st.success("Agreement Signed Successfully!")
        st.write("You have successfully signed the Investment Advisor Agreement.")
    else:
        st.warning("Invalid OTP. Please try again.")
    
# Main logic to handle the flow
def main():
    client_name, client_address, client_aadhar = ekyc_form()  # Run EKYC Form
    if client_name and client_address and client_aadhar:
        # After successful EKYC, proceed with the agreement
        investment_advisor_agreement(client_name, client_address, client_aadhar)

if __name__ == "__main__":
    main()
