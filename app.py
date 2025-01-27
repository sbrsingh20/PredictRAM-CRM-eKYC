import streamlit as st
from fpdf import FPDF
import random
import time

# Step 1: Client Information Form
def client_form():
    st.title("Client EKYC Form")

    full_name = st.text_input("Full Name (as per official records)")
    dob = st.date_input("Date of Birth")
    address = st.text_area("Address (as per government records)")
    photo = st.file_uploader("Upload Passport-Size Photograph", type=['jpg', 'png', 'jpeg'])
    email = st.text_input("Email ID")
    mobile = st.text_input("Mobile Number")
    pan = st.text_input("PAN Number")
    bank_account = st.text_input("Bank Account Details (optional)")
    aadhar_number = st.text_input("Aadhar Number")

    if st.button('Submit'):
        # Proceed to the next step after form submission
        if not full_name or not dob or not address or not email or not mobile or not pan or not aadhar_number:
            st.error("Please fill all the required fields.")
        else:
            st.session_state.client_info = {
                'full_name': full_name,
                'dob': dob,
                'address': address,
                'photo': photo,
                'email': email,
                'mobile': mobile,
                'pan': pan,
                'bank_account': bank_account,
                'aadhar_number': aadhar_number
            }
            st.success("Form submitted successfully! Proceeding to the next step.")
            time.sleep(2)
            return True
    return False

# Step 2: Display the Investment Advisor Agreement
def agreement_page():
    st.title("Investment Advisor Agreement")

    agreement_text = """
    Investment Advisor Agreement

    This Investment Advisor Agreement ("Agreement") is made and entered into by and between:

    Client: [Client Name], [Address], [City, State, ZIP Code]
    and
    Investment Advisor: [Advisor Name], [Firm Name], [Address], [City, State, ZIP Code]

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
    """
    
    st.markdown(agreement_text)

    agreement_accepted = st.checkbox("I accept the terms and conditions of the agreement.")

    if st.button('Proceed to Aadhar OTP') and agreement_accepted:
        return True
    else:
        st.warning("You must accept the agreement before proceeding.")
    return False

# Step 3: Aadhar OTP Verification (Simulated)
def aadhar_otp_verification():
    st.title("Aadhar OTP Verification")

    aadhar_otp = st.text_input("Enter Aadhar OTP", max_chars=4)

    if st.button('Verify OTP'):
        # Simulate OTP verification
        if aadhar_otp == "1100":
            st.success("eKYC Verified successfully!")
            time.sleep(1)
            return True
        else:
            st.error("Invalid OTP. Please try again.")
    return False

# Step 4: Generate and Download PDF
def generate_pdf():
    if 'client_info' in st.session_state:
        client_info = st.session_state.client_info

        # Create a PDF document
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="EKYC Verification - Client Details", ln=True, align='C')

        # Add client information to the PDF
        pdf.ln(10)
        for key, value in client_info.items():
            if key == 'photo':  # Skip the photo in the PDF
                continue
            pdf.cell(200, 10, f"{key.capitalize()}: {value}", ln=True)

        # Save the PDF
        pdf_output_path = "ekyc_client_details.pdf"
        pdf.output(pdf_output_path)

        st.success("PDF generated successfully!")
        with open(pdf_output_path, "rb") as file:
            st.download_button("Download PDF", file, file_name="ekyc_client_details.pdf")

# Main Flow
def main():
    if 'client_info' not in st.session_state:
        if client_form():
            if agreement_page():
                if aadhar_otp_verification():
                    generate_pdf()
    else:
        st.warning("eKYC process is already completed. Please proceed with downloading the PDF.")

if __name__ == "__main__":
    main()
