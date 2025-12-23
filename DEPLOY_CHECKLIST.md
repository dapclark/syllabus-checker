# Hetzner Deployment Checklist

Quick reference for deploying to syllabus-check.clarkenstein.com

## Before You Start
- [ ] Hetzner account created
- [ ] SSH key ready or will use password
- [ ] Access to DNS settings for clarkenstein.com

## Hetzner Setup (5 minutes)
- [ ] Create CX22 server ($6/month) - Ubuntu 24.04 in Ashburn
- [ ] Note IP address: `___________________`
- [ ] Can SSH in: `ssh root@<ip>`

## DNS Setup (5 minutes)
- [ ] Add A record: `syllabus-check` → `<server-ip>`
- [ ] Wait 2-5 minutes
- [ ] Test: `ping syllabus-check.clarkenstein.com` works

## Server Setup (10 minutes)
```bash
# SSH in
ssh root@<server-ip>

# Install everything
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git ufw

# Firewall
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable
```

## Upload Code (5 minutes)
Choose one:

**Option A - Git:**
```bash
# On local machine: push to GitHub
# On server:
cd /var/www
mkdir syllabus-checker
cd syllabus-checker
git clone https://github.com/dapclark/syllabus-checker.git .
```

**Option B - Direct upload:**
```bash
# On local machine:
cd /Users/dclark/Documents/syllabus_checker
scp -r * root@<server-ip>:/var/www/syllabus-checker/
```

## Python Setup (3 minutes)
```bash
cd /var/www/syllabus-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p uploads
chown -R www-data:www-data uploads
```

## Environment (2 minutes)
```bash
nano /var/www/syllabus-checker/.env
```
Add:
```
SECRET_KEY=<random-string-here>
UPLOAD_FOLDER=/var/www/syllabus-checker/uploads
```

## Systemd Service (3 minutes)
```bash
sudo nano /etc/systemd/system/syllabus-checker.service
```
Paste content from HETZNER_DEPLOY.md → Save

```bash
sudo systemctl daemon-reload
sudo systemctl enable syllabus-checker
sudo systemctl start syllabus-checker
sudo systemctl status syllabus-checker  # Should be "active (running)"
```

## Nginx (3 minutes)
```bash
sudo nano /etc/nginx/sites-available/syllabus-checker
```
Paste content from HETZNER_DEPLOY.md → Save

```bash
sudo ln -s /etc/nginx/sites-available/syllabus-checker /etc/nginx/sites-enabled/
sudo nginx -t  # Should say "syntax is ok"
sudo systemctl restart nginx
```

## Test HTTP (1 minute)
- [ ] Visit: http://syllabus-check.clarkenstein.com
- [ ] Upload works

## SSL Certificate (2 minutes)
```bash
sudo certbot --nginx -d syllabus-check.clarkenstein.com
```
- [ ] Enter email
- [ ] Agree to terms
- [ ] Redirect HTTP to HTTPS? YES

## Final Test
- [ ] Visit: https://syllabus-check.clarkenstein.com
- [ ] Upload a test .docx file
- [ ] Results display correctly
- [ ] Download marked document works

## Done! ✅

Total time: ~30-40 minutes
Monthly cost: $6

## Quick Commands Reference

**Restart app:**
```bash
sudo systemctl restart syllabus-checker
```

**View logs:**
```bash
sudo journalctl -u syllabus-checker -f
```

**Update code:**
```bash
cd /var/www/syllabus-checker
git pull
sudo systemctl restart syllabus-checker
```

**Check resources:**
```bash
free -h  # Memory
df -h    # Disk
```
