# Import necessary packages  
import streamlit as st  
import os  
import base64  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.primitives.asymmetric import rsa, padding  
from cryptography.hazmat.primitives import hashes  
from cryptography.hazmat.backends import default_backend  
from datetime import datetime  

# Function to generate RSA public and private keys  
def generate_keys():  
    try:  
        private_key = rsa.generate_private_key(  
            public_exponent=65537,  
            key_size=3072,  
            backend=default_backend()  
        )  
        public_key = private_key.public_key()  

        # Save keys to files as PEM format using serialization  
        save_key('./keys/privateKey.pem', private_key.private_bytes(  
            encoding=serialization.Encoding.PEM,  
            format=serialization.PrivateFormat.PKCS8,  
            encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')  
        ))  

        save_key('./keys/publicKey.pem', public_key.public_bytes(  
            encoding=serialization.Encoding.PEM,  
            format=serialization.PublicFormat.SubjectPublicKeyInfo  
        ))  

        show_success_message("Keys generated and saved successfully!")  
        log_intrusion("Keys generated and saved successfully!", is_success=True)  
    except Exception as e:  
        st.error(f"Error generating keys: {e}")  
        log_intrusion(f"Error generating keys: {e}", is_success=False)  

# Function to save RSA key data to a specified file  
def save_key(filepath, key_data):  
    with open(filepath, 'wb') as file:  
        file.write(key_data)  

# Load RSA keys from files  
def load_keys():  
    try:  
        st.session_state.private_key = load_key('./keys/privateKey.pem', is_private=True)  
        st.session_state.public_key = load_key('./keys/publicKey.pem', is_private=False)  
        show_success_message("Keys loaded successfully!")  
        log_intrusion("Keys loaded successfully!", is_success=True)  
    except Exception as e:  
        st.error(f"Error loading keys: {e}")  
        log_intrusion(f"Error loading keys: {e}", is_success=False)  

def load_key(filepath, is_private=True):  
    with open(filepath, 'rb') as file:  
        if is_private:  
            return serialization.load_pem_private_key(  
                file.read(),  
                password=(b'mypassword'),  
                backend=default_backend()  
            )  
        else:  
            return serialization.load_pem_public_key(  
                file.read(),  
                backend=default_backend()  
            )  

# Display success message  
def show_success_message(message):   
    custom_message = f"""  
    <div style="  
        background-color: rgba(34, 140, 34, 0.85);  
        color: #ffffff;   
        font-size: 1.2em;  
        padding: 5px;  
        border-radius: 8px;   
        text-align: center;   
        margin: 10px;  
    ">  
        {message}  
    </div>  
    """  
    st.markdown(custom_message, unsafe_allow_html=True)  

# Encryption with file saving  
def encrypt_message(message):  
    if st.session_state.public_key is None:  
        st.warning("Generate or load keys first!")  
        return None  
    try:  
        # Encrypt the message  
        encrypted_message = st.session_state.public_key.encrypt(  
            message.encode(),  
            padding.OAEP(  
                mgf=padding.MGF1(hashes.SHA256()),  
                algorithm=hashes.SHA256(),  
                label=None  
            )  
        )  

        # Save the encrypted message to a file  
        file_path = "encrypted_message.bin"  
        with open(file_path, "wb") as encrypted_file:  
            encrypted_file.write(encrypted_message)  
        show_success_message(f"Encrypted message saved as {file_path}")  
        log_intrusion("Encrypted message saved successfully", is_success=True)  

        return encrypted_message  
    except Exception as e:  
        st.error(f"Encryption failed: {e}")  
        log_intrusion(f"Encryption failed: {e}", is_success=False)  
        return None  

# Decryption from a file  
def decrypt_message_from_file(encrypted_data):  
    if st.session_state.private_key is None:  
        st.warning("Generate or load keys first!")  
        log_intrusion("Decryption attempt without keys", is_success=False)  
        return None  

    try:  
        # Decrypt the message using the loaded private key  
        decrypted_message = st.session_state.private_key.decrypt(  
            encrypted_data,  
            padding.OAEP(  
                mgf=padding.MGF1(hashes.SHA256()),  
                algorithm=hashes.SHA256(),  
                label=None  
            )  
        )  
        log_intrusion("Decryption successful", is_success=True)  
        return decrypted_message.decode('utf-8')  
    except Exception as e:  
        st.error(f"Decryption failed: {e}")  
        log_intrusion(f"Decryption failed: {e}", is_success=False)  
        return None

# Signing the content and saving the signed file  
def sign_and_save_file(content, username):  
    if st.session_state.private_key is None:  
        st.warning("Generate or load keys first!")  
        return None  

    # Sign the content  
    signature = st.session_state.private_key.sign(  
        content.encode(),  
        padding.PSS(  
            mgf=padding.MGF1(hashes.SHA256()),  
            salt_length=padding.PSS.MAX_LENGTH  
        ),  
        hashes.SHA256()  
    )  
    st.session_state.signature = signature  

    # Append "Signed by: username" to the content  
    signed_content = content + f"\n\nSigned by: {username}"  

    # Save the signed file  
    file_path = 'signed_file.txt'  
    with open(file_path, 'w') as signed_file:  
        signed_file.write(signed_content)  

    show_success_message(f"Signed file saved as {file_path}")  
    log_intrusion(f"File signed and saved successfully by {username}", is_success=True)  
    return signature  

# Verification  
def verify_signature(content, signature):  
    if st.session_state.public_key is None:  
        st.warning("Generate or load keys first!")  
        return None  
    try:  
        # Verify the signature  
        st.session_state.public_key.verify(  
            signature,  
            content.encode(),  
            padding.PSS(  
                mgf=padding.MGF1(hashes.SHA256()),  
                salt_length=padding.PSS.MAX_LENGTH  
            ),  
            hashes.SHA256()  
        )  
        show_success_message("Signature verified successfully!")  
        log_intrusion("Signature verified successfully!", is_success=True)  
        return True  
    except Exception as e:  
        st.error(f"Signature verification failed: {e}")  
        log_intrusion(f"Signature verification failed: {e}", is_success=False)  
        return False  

# Intrusion Detection logging  
def log_intrusion(event, is_success=False):  
    """Log an event (success or failure) to a file."""  
    with open('./logs/intrusion_logs.txt', 'a') as log_file:  
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        status = "SUCCESS" if is_success else "FAILURE"  
        log_file.write(f"[{timestamp}] {status}: {event}\n")  

# Streamlit Interface  
st.title("RSA Application Tool")  
username = st.text_input("Enter your username: ", value="")  

# Key management  
if st.button("Generate Keys"):  
    generate_keys()  

if st.button("Load Keys"):  
    load_keys()  

# Open file to upload any txt file to perform functions  
uploaded_file = st.file_uploader("Upload a .txt file", type="txt")  
if uploaded_file is not None:  
    file_content = uploaded_file.read().decode("utf-8")  
    st.text_area("File Content", file_content, height=200)  

    # Encryption  
    if st.button("Encrypt Message"):  
        encrypted_message = encrypt_message(file_content)  
 
# File uploader for encrypted file to decrypt  
st.subheader("Upload Encrypted File for Decryption")  
encrypted_file = st.file_uploader("Upload Encrypted File", type="bin")  
if encrypted_file is not None:  
    encrypted_message = encrypted_file.read()  # Read the uploaded file as bytes  

    if st.button("Decrypt Uploaded File"):  
        decrypted_message = decrypt_message_from_file(encrypted_message)  
        if decrypted_message:  
            st.text_area("Decrypted Message:", decrypted_message, height=200)  

# Signing  
    if st.button("Sign and Save"):  
        if username.strip():  
            signature = sign_and_save_file(file_content, username)   
        else:  
            st.warning("Please provide a username before signing!")

# Verification  
    if st.button("Verify Signature"):  
        if st.session_state.signature:  
            is_verified = verify_signature(file_content, st.session_state.signature)  
            if is_verified:  
                show_success_message("Signature is valid and matches the content!")  
        else:  
            st.warning("No signature available to verify!")  


# Viewing Intrusion Logs  
st.subheader("View Intrusion Logs")  

if os.path.exists('./logs/intrusion_logs.txt'):  
    with open('./logs/intrusion_logs.txt', 'r') as log_file:  
        logs = log_file.readlines()  
        
    if logs:  
        styled_logs = ""  
        for log in logs:  
            if "FAILURE" in log:  
                styled_logs += f"<div style='color: red;'>{log.strip()}</div>"  
            else:  
                styled_logs += f"<div style='color: green;'>{log.strip()}</div>"  
        
        st.markdown(  
            f"""  
            <div style='background-color:rgb(240, 240, 240); border: 1px solid #eee;  
            padding: 10px; border-radius: 5px; overflow-y: auto; height: 300px;'>  
                {styled_logs}  
            </div>  
            """,  
            unsafe_allow_html=True  
        )  
    else:  
        st.write("No intrusion logs available.")   


# Set background image
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    custom_css = f"""
    <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.25)),
                url("data:image/png;base64,{encoded_image}");
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
            font-family: 'Consolas', sans-serif;
            color: white;
        }}

        h1 {{
            text-align: center;
            font-family: 'Baskerville Old Face', sans-serif;
            font-size: 2.8em;
            margin-top: 20px;
            color: rgb(240, 240, 240);
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


# Set the background
set_background("bg.png")
  

# Add Footer  
st.markdown("""  
    <footer>  
        Created by Umu Habiba, 32146640<br>  
        B.Sc. Cybersecurity | University of West London<br>  
        RSA Encryption Project<br>  
        © 2024  
    </footer>  
""", unsafe_allow_html=True)