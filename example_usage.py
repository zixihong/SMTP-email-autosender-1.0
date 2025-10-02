#!/usr/bin/env python3
"""
Example usage of the Email Sender Tool

This script demonstrates how to use the EmailSender class programmatically
instead of using the command line interface.
"""

from email_sender import EmailSender
import json

def create_example_config():
    """Create an example configuration file."""
    config = {
        "sender_emails": [
            "your-email1@gmail.com",
            "your-email2@gmail.com"
        ],
        "sender_password": "your-app-password",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "delay_between_emails": 2,
        "max_retries": 3,
        "email_template": {
            "subject": "Welcome to Our Service - {name}",
            "body": """
            <html>
            <body>
                <h2>Welcome {name}!</h2>
                <p>Thank you for joining our service. We're excited to have you on board.</p>
                <p>Your unique registration code is: <strong>{unique_code}</strong></p>
                <p>Please keep this code safe as you'll need it for account verification.</p>
                <br>
                <p>Best regards,<br>Our Team</p>
            </body>
            </html>
            """
        }
    }
    
    with open('example_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Created example_config.json")

def send_single_email_example():
    """Example of sending a single email."""
    sender = EmailSender('example_config.json')
    
    # Send a single email
    success = sender.send_email(
        sender_email="your-email@gmail.com",
        recipient_email="recipient@example.com",
        subject="Test Email",
        body="<html><body><p>This is a test email.</p></body></html>",
        is_html=True
    )
    
    if success:
        print("✓ Single email sent successfully!")
    else:
        print("✗ Failed to send single email")

def send_bulk_emails_example():
    """Example of sending bulk emails from CSV."""
    sender = EmailSender('example_config.json')
    
    # Send emails from CSV
    results = sender.send_emails_from_csv('sample_recipients.csv')
    
    print(f"Bulk email results:")
    print(f"  Total: {results['total']}")
    print(f"  Sent: {results['sent']}")
    print(f"  Failed: {results['failed']}")

if __name__ == "__main__":
    print("Email Sender Tool - Example Usage")
    print("=" * 40)
    
    # Create example configuration
    create_example_config()
    
    print("\nTo use this tool:")
    print("1. Update example_config.json with your email settings")
    print("2. Create your recipients CSV file")
    print("3. Run: python email_sender.py --csv your_file.csv --config example_config.json")
    print("4. Or use the EmailSender class programmatically as shown above")
