# Regularly sending emails as a reminder

This is a personal snippet for reminding people around doing periodic things like housework by sending emails on schedule.

# Configuration

First create a `.env` file to save the credentials of sending email address/password and receivers' email address. (Requires `python-dotenv`)

An example of `.env` file is
```
GMAIL_USER=your@email.com
GMAIL_PASSWORD=yourpassword
RECEIVERS={"Alice":"alice@email.com","Bob":"bob@email.com"}
```
*Note: Only gmail account has been tested with "less secure apps" being turn on.*
