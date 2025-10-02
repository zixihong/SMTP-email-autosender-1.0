#!/usr/bin/env python3
"""
Setup script for Email Sender Tool

This script helps users set up the email sender tool by creating
necessary configuration files and checking dependencies.
"""

import os
import json
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    else:
        print(f"✓ Python version: {sys.version.split()[0]}")
        return True

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_config_file():
    """Create a default configuration file if it doesn't exist."""
    if os.path.exists("config.json"):
        print("✓ Configuration file already exists")
        return True
    
    config = {
        "sender_emails": [
            "your-email@gmail.com"
        ],
        "sender_password": "your-app-password",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "delay_between_emails": 1,
        "max_retries": 3,
        "email_template": {
            "subject": "Your Email Subject",
            "body": "<html><body><p>Hello {name},<br><br>This is your personalized email.<br><br>Your unique code: <strong>{unique_code}</strong><br><br>Best regards,<br>Your Team</p></body></html>"
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✓ Created config.json - please update with your settings")
    return True

def create_env_file():
    """Create a .env file template if it doesn't exist."""
    if os.path.exists(".env"):
        print("✓ .env file already exists")
        return True
    
    env_content = """# Email Sender Tool Configuration
# Copy this file and update with your actual values

# Sender email (for single sender mode)
SENDER_EMAIL=your-email@gmail.com

# App password (not your regular password)
SENDER_PASSWORD=your-app-password

# SMTP settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# CSV file with recipients
CSV_FILENAME=recipients.csv
"""
    
    with open(".env.template", "w") as f:
        f.write(env_content)
    
    print("✓ Created .env.template - copy to .env and update with your settings")
    return True

def check_csv_file():
    """Check if sample CSV file exists."""
    if os.path.exists("sample_recipients.csv"):
        print("✓ Sample CSV file exists")
        return True
    else:
        print("❌ Sample CSV file not found")
        return False

def main():
    """Main setup function."""
    print("Email Sender Tool - Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create configuration files
    create_config_file()
    create_env_file()
    
    # Check sample files
    check_csv_file()
    
    print("\n" + "=" * 30)
    print("Setup completed!")
    print("\nNext steps:")
    print("1. Update config.json with your email settings")
    print("2. Create your recipients CSV file")
    print("3. Test with: python email_sender.py --csv sample_recipients.csv --dry-run")
    print("4. Send emails: python email_sender.py --csv your_file.csv")
    
    return True

if __name__ == "__main__":
    main()
