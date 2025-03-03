from pyisemail import is_email
import dns.resolver
import smtplib
import whois
import re

def validate_email_with_pyisemail(email):
    """Validate email with pyisemail"""
    bool_result = is_email(email, check_dns=True)
    detailed_result = is_email(email, check_dns=True, diagnose=True)
    return bool_result, detailed_result

def get_mx_records(domain):
    """Retrieve MX records for the domain"""
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return [(r.exchange.to_text(), r.preference) for r in answers]
    except Exception as e:
        return str(e)

def verify_smtp(email):
    """Verify if the SMTP server is reachable"""
    try:
        domain = email.split('@')[1]
        # Try connecting to the primary MX server
        mx_records = get_mx_records(domain)
        if isinstance(mx_records, str):
            return f"Error retrieving MX records: {mx_records}"
        primary_mx = mx_records[0][0]
        server = smtplib.SMTP(primary_mx, 25, timeout=10)
        server.ehlo()
        server.quit()
        return True  # SMTP server is responsive
    except Exception as e:
        return False  # SMTP verification failed

def get_domain_info(domain):
    """Retrieve domain registration information using Whois"""
    try:
        info = whois.whois(domain)
        return info
    except Exception as e:
        return str(e)

def validate_email_pattern(email):
    """Validate the general pattern of the email"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def main():
    # Read emails from file
    try:
        with open("email_valid.txt", "r") as file:
            emails = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("The file 'email_valid.txt' was not found.")
        return

    existing_emails = []

    for email in emails:
        if not validate_email_pattern(email):
            print(f"Skipping invalid email format: {email}")
            continue
        
        smtp_result = verify_smtp(email)
        if smtp_result:
            existing_emails.append(email)

    print("Existing Emails:")
    for email in existing_emails:
        print(email)

if __name__ == "__main__":
    main()
