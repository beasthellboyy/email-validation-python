Email Validation Script

Overview

This script validates email addresses by performing the following checks:

Pattern Validation – Uses a regular expression to check if the email format is valid.

DNS Check – Retrieves MX (Mail Exchange) records of the domain to ensure it can receive emails.

SMTP Server Verification – Attempts to connect to the domain's SMTP server to verify its existence.

WHOIS Lookup (Optional) – Retrieves domain registration information (not used in filtering, but useful for investigation).

Prerequisites

Ensure you have Python installed along with the necessary libraries:

pip install pyisemail dnspython smtplib-python python-whois

How to Use:-

Create a text file named email_valid.txt and add one email per line.

Run the script:-

python email_validation.py

The script will output a list of valid emails that passed all checks.

Explanation of Functions

validate_email_pattern(email): Ensures the email follows a valid format.

get_mx_records(domain): Retrieves the domain's MX records.

verify_smtp(email): Connects to the domain’s SMTP server to check if it is reachable.

get_domain_info(domain): Fetches WHOIS data for a domain.

Notes

Some mail servers may block direct SMTP verification, leading to false negatives.

WHOIS lookup may not always be available due to privacy restrictions.

Author

This script is designed for email validation and filtering tasks to ensure deliverability.

