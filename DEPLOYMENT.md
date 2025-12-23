# Deployment Guide for Syllabus Accessibility Checker

This guide will help you deploy the Syllabus Accessibility Checker to **syllabus-check.clarkenstein.com**.

## Prerequisites

- A server with Python 3.8+ installed
- Domain DNS configured to point to your server
- SSH access to your server
- nginx or Apache web server
- SSL certificate (recommended: Let's Encrypt)

## Step 1: Prepare Your Server

SSH into your server:
```bash
ssh user@your-server-ip
```

Install required system packages:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

## Step 2: Upload Application Files

Create application directory:
```bash
sudo mkdir -p /var/www/syllabus-checker
sudo chown $USER:$USER /var/www/syllabus-checker
```

Upload your files to the server (from your local machine):
```bash
scp -r /Users/dclark/Documents/syllabus_checker/* user@your-server-ip:/var/www/syllabus-checker/
```

Or use git:
```bash
cd /var/www/syllabus-checker
git clone <your-repo-url> .
```

## Step 3: Set Up Python Virtual Environment

On the server:
```bash
cd /var/www/syllabus-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 4: Create Upload Directory

```bash
sudo mkdir -p /var/www/syllabus-checker/uploads
sudo chown www-data:www-data /var/www/syllabus-checker/uploads
```

## Step 5: Set Environment Variables

Create a `.env` file:
```bash
cat > /var/www/syllabus-checker/.env << EOF
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
UPLOAD_FOLDER=/var/www/syllabus-checker/uploads
EOF
```

## Step 6: Create Systemd Service

Create service file:
```bash
sudo nano /etc/systemd/system/syllabus-checker.service
```

Add this content:
```ini
[Unit]
Description=Syllabus Accessibility Checker
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/syllabus-checker
Environment="PATH=/var/www/syllabus-checker/venv/bin"
EnvironmentFile=/var/www/syllabus-checker/.env
ExecStart=/var/www/syllabus-checker/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 wsgi:app

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable syllabus-checker
sudo systemctl start syllabus-checker
sudo systemctl status syllabus-checker
```

## Step 7: Configure Nginx

Create nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/syllabus-checker
```

Add this content:
```nginx
server {
    listen 80;
    server_name syllabus-check.clarkenstein.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/syllabus-checker/static;
        expires 30d;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/syllabus-checker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 8: Set Up SSL with Let's Encrypt

Install certbot:
```bash
sudo apt install certbot python3-certbot-nginx
```

Get SSL certificate:
```bash
sudo certbot --nginx -d syllabus-check.clarkenstein.com
```

Follow the prompts. Certbot will automatically update your nginx configuration.

## Step 9: Verify Deployment

Visit https://syllabus-check.clarkenstein.com in your browser!

## Updating the Application

To update the application:
```bash
cd /var/www/syllabus-checker
git pull  # or upload new files
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart syllabus-checker
```

## Monitoring and Logs

View application logs:
```bash
sudo journalctl -u syllabus-checker -f
```

View nginx logs:
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Troubleshooting

**Service won't start:**
```bash
sudo journalctl -u syllabus-checker -n 50
```

**Permission errors:**
```bash
sudo chown -R www-data:www-data /var/www/syllabus-checker/uploads
```

**Nginx errors:**
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

## Security Notes

1. The `.env` file contains secrets - never commit it to git
2. Keep your system and packages updated
3. Consider setting up a firewall (ufw)
4. Enable automatic security updates
5. Regularly backup your uploaded files

## Optional: Set Up Automatic Cleanup

Create a cron job to clean old uploads:
```bash
sudo crontab -e
```

Add:
```
0 2 * * * find /var/www/syllabus-checker/uploads -type f -mtime +7 -delete
```

This deletes files older than 7 days every night at 2 AM.
