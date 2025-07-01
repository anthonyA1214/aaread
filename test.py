from email_validator import validate_email, EmailNotValidError

email = "anthonyamiludd"

try:
    # Validate the email address
    valid = validate_email(email, check_deliverability=True)
    print(f"Valid email: {valid.email}")

except EmailNotValidError as e:
    # Email is not valid, handle the error
    print(f"Invalid email: {e}")
# This is a simple test to validate an email address using the email_validator library.