#!/usr/bin/env python3
"""
General Purpose Email Sender Tool

A flexible email sending tool that can send personalized emails to multiple recipients
from a CSV file with configurable templates and multiple sender accounts.

Author: Your Name
License: MIT
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import csv
import time
import random
import os
import argparse
import json
from dotenv import load_dotenv
from typing import List, Dict, Optional

class EmailSender:
    """A flexible email sending class with support for multiple sender accounts and templates."""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize the email sender with configuration."""
        load_dotenv()
        self.config = self._load_config(config_file)
        self.sender_emails = self.config.get('sender_emails', [os.getenv('SENDER_EMAIL')])
        self.sender_password = self.config.get('sender_password', os.getenv('SENDER_PASSWORD'))
        self.smtp_server = self.config.get('smtp_server', os.getenv('SMTP_SERVER'))
        self.smtp_port = self.config.get('smtp_port', int(os.getenv('SMTP_PORT', 587)))
        self.template = self.config.get('email_template', {})
        self.delay_between_emails = self.config.get('delay_between_emails', 1)
        self.max_retries = self.config.get('max_retries', 3)
        
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file or environment variables."""
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def send_email(self, sender_email: str, recipient_email: str, subject: str, 
                   body: str, is_html: bool = True) -> bool:
        """Send a single email."""
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Attach body as HTML or plain text
            msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
            
            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(sender_email, self.sender_password)
            
            # Send email
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email to {recipient_email}: {e}")
            return False
    
    def generate_unique_code(self) -> str:
        """Generate a unique code for the email."""
        return str(random.randint(10000, 99999))
    
    def format_email_body(self, template: str, **kwargs) -> str:
        """Format email body with provided variables."""
        # Add common variables
        kwargs['unique_code'] = self.generate_unique_code()
        
        try:
            return template.format(**kwargs)
        except KeyError as e:
            print(f"Missing template variable: {e}")
            return template
    
    def send_emails_from_csv(self, csv_filename: str, email_index: int = 0) -> Dict[str, int]:
        """Send emails to all recipients in CSV file."""
        results = {'sent': 0, 'failed': 0, 'total': 0}
        
        if not os.path.exists(csv_filename):
            print(f"CSV file not found: {csv_filename}")
            return results
        
        with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                results['total'] += 1
                recipient_email = row.get('email', '').strip()
                
                if not recipient_email:
                    print("Skipping row with empty email")
                    continue
                
                # Get sender email (rotate through available senders)
                sender_email = self.sender_emails[email_index % len(self.sender_emails)]
                
                # Format email content
                subject = self.template.get('subject', 'Email from Email Sender Tool')
                body_template = self.template.get('body', 'Hello {name}, this is a test email.')
                
                # Format the email body with row data
                formatted_body = self.format_email_body(body_template, **row)
                
                # Send email with retries
                success = False
                for attempt in range(self.max_retries):
                    if self.send_email(sender_email, recipient_email, subject, formatted_body):
                        results['sent'] += 1
                        print(f"✓ Email sent successfully to {recipient_email} from {sender_email} (attempt {attempt + 1})")
                        success = True
                        break
                    else:
                        if attempt < self.max_retries - 1:
                            print(f"✗ Attempt {attempt + 1} failed for {recipient_email}, retrying...")
                            time.sleep(5)  # Wait before retry
                
                if not success:
                    results['failed'] += 1
                    print(f"✗ Failed to send email to {recipient_email} after {self.max_retries} attempts")
                
                # Rotate to next sender email
                email_index = (email_index + 1) % len(self.sender_emails)
                
                # Delay between emails to avoid rate limiting
                if self.delay_between_emails > 0:
                    time.sleep(self.delay_between_emails)
        
        return results

def main():
    """Main function to run the email sender."""
    parser = argparse.ArgumentParser(description='Send personalized emails from CSV file')
    parser.add_argument('--csv', required=True, help='CSV file with recipient data')
    parser.add_argument('--config', default='config.json', help='Configuration file (default: config.json)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be sent without actually sending')
    
    args = parser.parse_args()
    
    # Initialize email sender
    sender = EmailSender(args.config)
    
    if args.dry_run:
        print("DRY RUN MODE - No emails will be sent")
        print(f"Would process CSV file: {args.csv}")
        print(f"Using configuration: {args.config}")
        return
    
    # Send emails
    print(f"Starting email sending process...")
    print(f"CSV file: {args.csv}")
    print(f"Configuration: {args.config}")
    print(f"Sender emails: {len(sender.sender_emails)}")
    print("-" * 50)
    
    results = sender.send_emails_from_csv(args.csv)
    
    print("-" * 50)
    print(f"Email sending completed!")
    print(f"Total recipients: {results['total']}")
    print(f"Successfully sent: {results['sent']}")
    print(f"Failed: {results['failed']}")
    
    if results['failed'] > 0:
        print(f"Success rate: {(results['sent'] / results['total'] * 100):.1f}%")

if __name__ == "__main__":
    main()
