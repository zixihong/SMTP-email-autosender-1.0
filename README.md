# Email Sender Tool

A flexible, general-purpose email sending tool that can send personalized emails to multiple recipients from a CSV file. Features configurable templates, multiple sender accounts, retry logic, and rate limiting.

## Features

- 📧 **Bulk Email Sending**: Send personalized emails to multiple recipients from CSV files
- 🔄 **Multiple Sender Accounts**: Rotate between multiple sender email accounts to avoid rate limits
- 📝 **Configurable Templates**: Customize email subjects and HTML/plain text bodies
- 🔁 **Retry Logic**: Automatic retry on failed sends with configurable attempts
- ⏱️ **Rate Limiting**: Configurable delays between emails to avoid spam filters
- 🛡️ **Error Handling**: Comprehensive error handling and logging
- 🧪 **Dry Run Mode**: Test your configuration without actually sending emails
- 🔧 **Environment Variables**: Support for `.env` files for sensitive configuration

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd email-sender-tool
   ```

2. **Install dependencies**
   ```bash
   pip install python-dotenv
   ```

3. **Set up your environment**
   ```bash
   # Copy the template files
   cp config.json.template config.json
   cp sample_recipients.csv your_recipients.csv
   ```

## Configuration

### Method 1: JSON Configuration File (Recommended)

Create a `config.json` file based on the template:

```json
{
  "sender_emails": [
    "your-email1@gmail.com",
    "your-email2@gmail.com"
  ],
  "sender_password": "your-app-password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "delay_between_emails": 1,
  "max_retries": 3,
  "email_template": {
    "subject": "Your Email Subject Here",
    "body": "<html><body><p>Hello {name},<br><br>This is a personalized email for you.<br><br>Your unique code is: <strong>{unique_code}</strong><br><br>Best regards,<br>Your Team</p></body></html>"
  }
}
```

### Method 2: Environment Variables

Create a `.env` file:

```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
CSV_FILENAME=recipients.csv
```

## Email Template Variables

The email template supports the following variables:

- `{name}` - Recipient's name from CSV
- `{email}` - Recipient's email from CSV
- `{unique_code}` - Auto-generated unique code
- Any other column from your CSV file (e.g., `{title}`, `{company}`, etc.)

## CSV File Format

Your CSV file should have at least an `email` column. Additional columns can be used in your email template:

```csv
name,email,title,company
John Doe,john.doe@example.com,Software Engineer,Acme Corp
Jane Smith,jane.smith@example.com,Data Scientist,Tech Inc
```

## Usage

### Basic Usage

```bash
python email_sender.py --csv recipients.csv
```

### With Custom Configuration

```bash
python email_sender.py --csv recipients.csv --config my_config.json
```

### Dry Run (Test Mode)

```bash
python email_sender.py --csv recipients.csv --dry-run
```

### Command Line Options

- `--csv`: Path to CSV file with recipient data (required)
- `--config`: Path to configuration file (default: config.json)
- `--dry-run`: Show what would be sent without actually sending emails

## Email Provider Setup

### Gmail Setup

1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
3. Use the app password (not your regular password) in the configuration

### Other Email Providers

| Provider | SMTP Server | Port | Security |
|----------|-------------|------|----------|
| Gmail | smtp.gmail.com | 587 | TLS |
| Outlook | smtp-mail.outlook.com | 587 | TLS |
| Yahoo | smtp.mail.yahoo.com | 587 | TLS |
| Custom | your-smtp-server.com | 587/465 | TLS/SSL |

## Best Practices

### Rate Limiting
- Start with 1-2 second delays between emails
- Use multiple sender accounts to distribute load
- Monitor your email provider's sending limits

### Email Content
- Use clear, professional subject lines
- Include unsubscribe information if required
- Test with small batches first
- Avoid spam trigger words

### Security
- Never commit passwords to version control
- Use app passwords instead of main passwords
- Consider using environment variables for sensitive data

## Troubleshooting

### Common Issues

**"Authentication failed"**
- Check your email and password
- For Gmail, ensure you're using an App Password
- Verify 2-factor authentication is enabled

**"Connection refused"**
- Check SMTP server and port settings
- Verify your network connection
- Some networks block SMTP ports

**"Rate limit exceeded"**
- Increase delay between emails
- Use multiple sender accounts
- Check your email provider's limits

**"Template variable not found"**
- Ensure CSV column names match template variables
- Check for typos in variable names
- Use `{unique_code}` for auto-generated codes

### Debug Mode

Run with dry-run to test your configuration:

```bash
python email_sender.py --csv recipients.csv --dry-run
```

## Examples

### Example 1: Conference Invitation

**CSV (conference_attendees.csv):**
```csv
name,email,paper_title,registration_link
Dr. Smith,smith@university.edu,"Machine Learning in Healthcare",https://conference.com/register
Prof. Jones,jones@college.edu,"AI Ethics",https://conference.com/register
```

**Template:**
```json
{
  "subject": "Invitation to AI Conference 2024",
  "body": "<html><body><p>Dear {name},<br><br>We're excited about your research: <strong>{paper_title}</strong>.<br><br>You're invited to present at our conference. Register here: <a href='{registration_link}'>Conference Registration</a><br><br>Your unique code: <strong>{unique_code}</strong><br><br>Best regards,<br>Conference Team</p></body></html>"
}
```

### Example 2: Newsletter

**CSV (newsletter_subscribers.csv):**
```csv
name,email,company,industry
Alice Johnson,alice@techcorp.com,TechCorp,Technology
Bob Wilson,bob@finance.com,FinanceCorp,Finance
```

**Template:**
```json
{
  "subject": "Monthly Newsletter - {company}",
  "body": "<html><body><p>Hello {name},<br><br>Here's your monthly newsletter for {company} in the {industry} industry.<br><br>Your subscriber code: {unique_code}<br><br>Newsletter Team</p></body></html>"
}
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section above
- Create an issue on GitHub
- Review the examples and documentation

## Archive

The `archive/` directory contains the original email sender scripts that were used for the CSAC conference project. These files are preserved for historical reference:

- `archive_original_sender.py` - Original single-sender version
- `archive_improved_sender.py` - Improved multi-sender version
- `archive/README.md` - Detailed explanation of the archived files

## Changelog

### Version 1.0.0
- Initial release
- Basic email sending functionality
- CSV support
- Template system
- Multiple sender accounts
- Retry logic
- Rate limiting
