import streamlit as st
from fpdf import FPDF
import time

# Step 1: Client Information Form
def client_form():
    st.title("Client EKYC Form")

    # Get the client information inputs
    full_name = st.text_input("Full Name (as per official records)")
    dob = st.date_input("Date of Birth")
    address = st.text_area("Address (as per government records)")
    photo = st.file_uploader("Upload Passport-Size Photograph", type=['jpg', 'png', 'jpeg'])
    email = st.text_input("Email ID")
    mobile = st.text_input("Mobile Number")
    pan = st.text_input("PAN Number")
    bank_account = st.text_input("Bank Account Details (optional)")
    aadhar_number = st.text_input("Aadhar Number")

    # Submit button
    if st.button('Submit'):
        # Check if all required fields are filled
        if not full_name or not dob or not address or not email or not mobile or not pan or not aadhar_number:
            st.error("Please fill all the required fields.")
        else:
            # Store the data in session state for later use
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
            time.sleep(2)  # Simulate a small delay before moving to the next step
            return True
    return False

# Step 2: Display the Investment Advisor Agreement
def agreement_page():
    st.title("Investment Advisor Agreement")

    # Display the text of the agreement
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

    # Checkbox for agreement acceptance
    agreement_accepted = st.checkbox("I accept the terms and conditions of the agreement.")

    # Button to proceed to Aadhar OTP verification if the agreement is accepted
    if st.button('Proceed to Aadhar OTP') and agreement_accepted:
        return True
    elif not agreement_accepted:
        st.warning("You must accept the agreement to proceed.")
    return False

# Step 3: Aadhar OTP Verification (Simulated)
def aadhar_otp_verification():
    st.title("Aadhar OTP Verification")

    # Input for OTP
    aadhar_otp = st.text_input("Enter Aadhar OTP (e.g., 1100)", max_chars=4)

    # Button to verify OTP
    if st.button('Verify OTP'):
        # Simulating OTP verification with a predefined OTP "1100"
        if aadhar_otp == "1100":
            st.success("eKYC Verified successfully!")
            time.sleep(1)  # Simulate delay after verification
            return True
        else:
            st.error("Invalid OTP. Please try again.")
    return False

# Step 4: Generate PDF and allow downloading
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
        # Step 1: Collect client details via the form
        if client_form():
            # Step 2: Show the agreement page and accept terms
            if agreement_page():
                # Step 3: Verify Aadhar OTP
                if aadhar_otp_verification():
                    # Step 4: Generate and allow PDF download
                    generate_pdf()
    else:
        # eKYC process already completed, allow user to input OTP to download PDF
        st.warning("eKYC process is already completed. Please input OTP to download the PDF.")

        # Ask for OTP verification if the process is completed
        aadhar_otp = st.text_input("Enter Aadhar OTP (e.g., 1100)", max_chars=4)

        if st.button('Verify OTP'):
            if aadhar_otp == "1100":
                st.success("eKYC Verified successfully!")
                generate_pdf()  # Generate the PDF for download
            else:
                st.error("Invalid OTP. Please try again.")

if __name__ == "__main__":
    main()
