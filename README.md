# RSA Encryption Tool 🔐

A Python-based RSA cryptography application built with Streamlit. This project demonstrates secure file encryption and decryption, RSA key management, digital signatures, and signature verification through a web-based interface.

## 📌 Project Overview

This project was developed for the **Applied Cryptography** module as part of my BSc (Hons) Cybersecurity degree at the University of West London.

The application provides a graphical interface for exploring RSA public-key cryptography and demonstrating how encryption, decryption, and digital signatures can be used to protect information and verify authenticity.

## ✨ Features

- **RSA Key Generation:** Generate RSA public and private key pairs.
- **Key Management:** Save and load keys in PEM format, with password-based encryption for private-key storage.
- **File Encryption:** Encrypt text files using RSA encryption.
- **File Decryption:** Decrypt encrypted files using the corresponding private key.
- **Digital Signatures:** Sign files using RSA-PSS and SHA-256.
- **Signature Verification:** Verify digital signatures using the corresponding public key.
- **Activity Logging:** Record application activity and operation outcomes.
- **Interactive Web Interface:** Use a Streamlit interface to interact with the cryptographic functions.

## 🛠️ Technologies Used

- **Python** — application logic
- **Streamlit** — web-based user interface
- **Cryptography** — cryptographic operations and key handling
- **Base64** — encoding support
- **PEM** — key storage format

## 🔑 Cryptographic Concepts

### RSA Public-Key Cryptography

RSA uses a public and private key pair. The public key can be shared, while the private key must remain confidential.

### Encryption and Decryption

The application demonstrates encrypting file content and decrypting it with the corresponding private key.

### Digital Signatures

RSA-PSS with SHA-256 is used to demonstrate signing and verifying file content. Digital signatures help verify data integrity and authenticity.

### Private-Key Protection

Private-key files are password-protected when saved by the application. Keep private keys and their passwords secure.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3
- pip
- Git

### 1. Clone the repository

```bash
git clone https://github.com/habiba-cy/RSA-Encryption-Tool.git
cd RSA-Encryption-Tool
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install streamlit cryptography
```

### 4. Run the application

```bash
python -m streamlit run rsa_app.py
```

Streamlit will provide a local URL in the terminal. Open that URL in your browser to use the application.

## 📁 Project Structure

```text
RSA-Encryption-Tool/
├── rsa_app.py       # Main Streamlit application
├── bg.png           # Application background image
├── README.md        # Project documentation
└── .gitignore       # Excludes local and sensitive files
```

Keys, activity logs, generated files, and the Python virtual environment are kept out of the public repository.

## 🛡️ Security Considerations

- Never publish private keys, key passwords, or sensitive logs.
- Use test files and test keys when experimenting.
- Protect private keys with strong passwords and store them securely.
- Do not use this academic demonstration as a production encryption service without further security review.
- RSA encryption has message-size limitations. For encrypting larger files, hybrid encryption using RSA to protect a symmetric key is generally more appropriate.

## 🎓 Project Purpose

This project demonstrates practical applications of public-key cryptography, secure key management, file protection, and digital signatures. It helped me explore how cryptographic principles can be implemented in a Python application.

## 👩‍💻 Author

**Umu Habiba**

BSc (Hons) Cybersecurity — First-Class Honours  
University of West London

GitHub: [@habiba-cy](https://github.com/habiba-cy)

---

*Academic project developed for the Applied Cryptography module.*