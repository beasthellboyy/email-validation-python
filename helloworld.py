from pyisemail import is_email  # Library to validate email format and DNS
import dns.resolver  # Used to get MX records of a domain
import smtplib  # Used to verify SMTP server availability
import whois  # Used to get domain registration details
import re  # Regular expressions for pattern matching

def validate_email_with_pyisemail(email):
    """Validate email format and DNS using pyisemail"""
    bool_result = is_email(email, check_dns=True)  # Returns True if valid
    detailed_result = is_email(email, check_dns=True, diagnose=True)  # Returns detailed validation info
    return bool_result, detailed_result

def get_mx_records(domain):
    """Retrieve MX (Mail Exchange) records for the given domain"""
    try:
        answers = dns.resolver.resolve(domain, 'MX')  # Query MX records
        return [(r.exchange.to_text(), r.preference) for r in answers]  # Return list of MX servers with preferences
    except Exception as e:
        return str(e)  # Return error message if failed

def verify_smtp(email):
    """Verify if the SMTP server for an email is reachable"""
    try:
        domain = email.split('@')[1]  # Extract domain from email
        mx_records = get_mx_records(domain)  # Get MX records for domain
        
        if isinstance(mx_records, str):  # If error occurred, return message
            return f"Error retrieving MX records: {mx_records}"
        
        primary_mx = mx_records[0][0]  # Get primary mail server
        server = smtplib.SMTP(primary_mx, 25, timeout=10)  # Connect to SMTP server
        server.ehlo()  # Send EHLO command
        server.quit()  # Close connection
        return True  # SMTP server is responsive
    except Exception as e:
        return False  # SMTP verification failed

def get_domain_info(domain):
    """Retrieve domain registration information using Whois lookup"""
    try:
        info = whois.whois(domain)  # Fetch Whois info
        return info
    except Exception as e:
        return str(e)  # Return error message if failed

def validate_email_pattern(email):
    """Validate the general pattern of an email using regex"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"  # Basic email regex pattern
    return re.match(pattern, email) is not None  # Returns True if pattern matches

def main():
    """Main function to read emails, validate, and check if they exist"""
    # Try to read emails from a file
    try:
        with open("email_valid.txt", "r") as file:
            emails = [line.strip() for line in file if line.strip()]  # Read and clean up emails
    except FileNotFoundError:
        print("The file 'email_valid.txt' was not found.")
        return

    existing_emails = []  # List to store valid emails

    for email in emails:
        if not validate_email_pattern(email):  # Check if email format is valid
            print(f"Skipping invalid email format: {email}")
            continue
        
        smtp_result = verify_smtp(email)  # Check if email's SMTP server is reachable
        if smtp_result:
            existing_emails.append(email)  # Add to valid list if SMTP server responds

    # Print out valid emails
    print("Existing Emails:")
    for email in existing_emails:
        print(email)

# Run main function when script is executed
if __name__ == "__main__":
    main()

# Run this file through your cmd to fetch the list of emails
