# Deploy to Hetzner Cloud (Cost-Effective Testing)

## Cost Breakdown
- **CX22 VPS**: €5.83/month (~$6.30 USD)
  - 2 vCPU cores
  - 4 GB RAM
  - 40 GB SSD
  - 20 TB traffic
  - Perfect for testing and light production use

- **Alternative for minimal testing**: CX11 at €4.15/month (~$4.50 USD) - 2GB RAM should be fine for testing

## Step 1: Create Hetzner Cloud Server

1. Go to https://console.hetzner.cloud
2. Create a new project (e.g., "syllabus-checker")
3. Click "Add Server"
4. Choose:
   - **Location**: Ashburn, VA (closest to you) or any US location
   - **Image**: Ubuntu 24.04
   - **Type**: CX22 (or CX11 for minimal testing)
   - **Networking**: Enable IPv4
   - **SSH Key**: Add your SSH public key (or create password)
   - **Name**: syllabus-checker
5. Click "Create & Buy Now"
6. Wait ~30 seconds for server to provision
7. Note the IP address shown (e.g., `123.45.67.89`)

## Step 2: Point Your Domain to the Server

1. Go to your DNS provider (where you manage clarkenstein.com)
2. Add an A record:
   ```
   Type: A
   Name: syllabus-check
   Value: <your-hetzner-server-ip>
   TTL: 300 (5 minutes)
   ```
3. Wait a few minutes for DNS to propagate
4. Test with: `ping syllabus-check.clarkenstein.com`

## Step 3: Initial Server Setup

SSH into your server:
```bash
ssh root@<your-server-ip>
```

Update system and install dependencies:
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git ufw
```

Set up firewall:
```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable
```

## Step 4: Create Deploy User (Optional but Recommended)

```bash
adduser deploy
usermod -aG sudo deploy
su - deploy
```

## Step 5: Upload Your Application

**Option A: Using Git (Recommended)**

On your local machine, create a git repository:
```bash
cd /Users/dclark/Documents/syllabus_checker
git init
git add .
git commit -m "Initial commit"
```

Push to GitHub (or GitLab/Bitbucket):
```bash
# Create a repo on GitHub first, then:
git remote add origin <your-repo-url>
git push -u origin main
```

On the server:
```bash
cd /var/www
sudo mkdir syllabus-checker
sudo chown deploy:deploy syllabus-checker  # if using deploy user
cd syllabus-checker
git clone https://github.com/dapclark/syllabus-checker.git .
```

**Option B: Direct Upload with scp**

From your local machine:
```bash
cd /Users/dclark/Documents/syllabus_checker
scp -r * root@<your-server-ip>:/var/www/syllabus-checker/
```

## Step 6: Set Up Python Environment

On the server:
```bash
cd /var/www/syllabus-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 7: Create Uploads Directory

```bash
mkdir -p /var/www/syllabus-checker/uploads
sudo chown -R www-data:www-data /var/www/syllabus-checker/uploads
```

## Step 8: Set Up Environment Variables

```bash
nano /var/www/syllabus-checker/.env
```

Add:
```bash
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
UPLOAD_FOLDER=/var/www/syllabus-checker/uploads
```

Save and exit (Ctrl+X, Y, Enter)

## Step 9: Create Systemd Service

```bash
sudo nano /etc/systemd/system/syllabus-checker.service
```

Paste this content:
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
ExecStart=/var/www/syllabus-checker/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:8000 wsgi:app --timeout 300
Restart=always

[Install]
WantedBy=multi-user.target
```

**Note**: Using 2 workers to keep memory usage low on small server.

Start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable syllabus-checker
sudo systemctl start syllabus-checker
sudo systemctl status syllabus-checker
```

Check it's running:
```bash
curl http://127.0.0.1:8000
```

## Step 10: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/syllabus-checker
```

Paste:
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
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/syllabus-checker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 11: Test HTTP Access

Visit http://syllabus-check.clarkenstein.com in your browser.

If it works, proceed to SSL!

## Step 12: Add SSL Certificate (Let's Encrypt - FREE)

```bash
sudo certbot --nginx -d syllabus-check.clarkenstein.com
```

Follow the prompts:
- Enter your email
- Agree to terms
- Choose whether to redirect HTTP to HTTPS (recommend YES)

Certbot will automatically:
- Get a certificate
- Update nginx config
- Set up auto-renewal

Test auto-renewal:
```bash
sudo certbot renew --dry-run
```

## Step 13: Done! 🎉

Visit **https://syllabus-check.clarkenstein.com**

## Monitoring & Maintenance

**View application logs:**
```bash
sudo journalctl -u syllabus-checker -f
```

**View nginx logs:**
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

**Restart app after changes:**
```bash
cd /var/www/syllabus-checker
git pull  # if using git
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart syllabus-checker
```

**Check server resources:**
```bash
htop  # install with: sudo apt install htop
df -h  # disk usage
free -h  # memory usage
```

## Cost Optimization Tips

1. **Start with CX11** ($4.50/month) - upgrade to CX22 if needed
2. **Snapshots**: Hetzner charges €0.01/GB/month for snapshots - take one after setup
3. **Backups**: €1.17/month for automated backups (20% of server cost) - optional for testing
4. **Traffic**: 20TB included - you won't hit this limit
5. **Scale up anytime** - Can resize server in minutes if needed

## Automatic Cleanup of Old Files

Add a cron job to delete files older than 7 days:
```bash
sudo crontab -e
```

Add this line:
```
0 2 * * * find /var/www/syllabus-checker/uploads -type f -mtime +7 -delete
```

## Troubleshooting

**Service won't start:**
```bash
sudo journalctl -u syllabus-checker -n 50 --no-pager
```

**Permission errors:**
```bash
sudo chown -R www-data:www-data /var/www/syllabus-checker
```

**Nginx errors:**
```bash
sudo nginx -t
sudo systemctl status nginx
```

**Can't connect to server:**
```bash
# Check firewall
sudo ufw status
# Should show: 22/tcp, 80/tcp, 443/tcp allowed
```

**Out of memory:**
- Upgrade from CX11 to CX22 in Hetzner console
- Or reduce workers in systemd service (change `--workers 2` to `--workers 1`)

## Security Hardening (Optional but Recommended)

```bash
# Disable root SSH login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
sudo systemctl restart sshd

# Set up fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Monthly Cost: ~$5-6 USD

Perfect for testing and light production use!
