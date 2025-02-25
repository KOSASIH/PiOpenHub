# PiOpenHub User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [System Requirements](#system-requirements)
   - [Installation](#installation)
3. [Configuration](#configuration)
4. [Using PiOpenHub](#using-piopenhub)
   - [User Registration](#user-registration)
   - [Logging In](#logging-in)
   - [Managing Transactions](#managing-transactions)
   - [Viewing Transaction History](#viewing-transaction-history)
5. [Troubleshooting](#troubleshooting)
6. [FAQs](#faqs)
7. [Support](#support)
8. [Conclusion](#conclusion)

## Introduction
Welcome to the PiOpenHub user guide! This document provides detailed instructions on how to set up and use the PiOpenHub application for cryptocurrency transactions and blockchain interactions.

## Getting Started

### System Requirements
Before you begin, ensure that your system meets the following requirements:
- Operating System: Windows, macOS, or Linux
- Python 3.x (if using the Python version)
- Node.js (if using the Node.js version)
- Internet connection for blockchain interactions

### Installation
Follow these steps to install PiOpenHub:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KOSASIH/PiOpenHub.git
   cd PiOpenHub
   ```

2. **Install Dependencies**:
   - For Python:
     ```bash
     pip install -r requirements.txt
     ```
   - For Node.js:
     ```bash
     npm install
     ```

3. **Set Up the Database**:
   - Run the database migrations:
     ```bash
     # For Python
     python src/database/migrations/migrate.py
     
     # For Node.js
     npm run migrate
     ```

4. **Start the Application**:
   - For Python:
     ```bash
     python src/main/app.py
     ```
   - For Node.js:
     ```bash
     node src/main/index.js
     ```

## Configuration
Before using the application, you may need to configure certain settings:

- **Configuration Files**:
  - Edit `src/main/config/config.py` (Python) or `src/main/config/config.js` (Node.js) to set your database connection details, API keys, and other settings.

## Using PiOpenHub

### User Registration
1. Navigate to the registration page.
2. Fill in the required fields (username, email, password).
3. Click on the "Register" button.
4. Check your email for a confirmation link and verify your account.

### Logging In
1. Go to the login page.
2. Enter your registered email and password.
3. Click on the "Login" button to access your account.

### Managing Transactions
1. After logging in, navigate to the "Transactions" section.
2. To create a new transaction:
   - Click on "New Transaction."
   - Enter the recipient's address and the amount.
   - Click "Send" to initiate the transaction.
3. Follow the prompts to confirm the transaction.

### Viewing Transaction History
1. Go to the "Transaction History" section.
2. Here, you can view all your past transactions, including details such as date, amount, and status.

## Troubleshooting
- **Common Issues**:
  - **Cannot connect to the database**: Ensure that your database server is running and that the connection details in the configuration file are correct.
  - **Transaction failed**: Check your internet connection and ensure that the recipient's address is valid.

- **Error Messages**: If you encounter any error messages, refer to the logs located in `src/main/utils/logger.py` for more details.

## FAQs
1. **What cryptocurrencies does PiOpenHub support?**
   - Currently, PiOpenHub supports Bitcoin, Ethereum, and Stellar transactions.

2. **Is my data secure?**
   - Yes, PiOpenHub implements industry-standard security practices, including data encryption and secure authentication.

3. **Can I use PiOpenHub on mobile devices?**
   - The current version is optimized for desktop use, but a mobile-friendly version is planned for future releases.

## Support
If you need further assistance, please reach out to our support team:
- Email: support@piopenhub.com
- GitHub Issues: [PiOpenHub Issues](https://github.com/KOSASIH/PiOpenHub/issues)

## Conclusion
Thank you for using PiOpenHub! We hope this user guide has helped you get started with the application. For any further questions or feedback , please feel free to contact our support team. We are continuously working to improve the application and your input is valuable to us. Enjoy your experience with PiOpenHub and happy transacting!
