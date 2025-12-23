# Push to GitHub: Quick Guide

Your repo: https://github.com/dapclark/syllabus-checker.git

## Step 1: Initialize Git (if not already done)

```bash
cd /Users/dclark/Documents/syllabus_checker
git init
```

## Step 2: Add Files

**Important**: Make sure these files are present:
- `Uniform-Syllabus-Template-1.docx` (required for checking)
- `app.py`
- `syllabus_checker.py`
- `wsgi.py`
- `requirements.txt`
- `templates/` folder
- `.gitignore`

Add all files:
```bash
git add .
```

Check what will be committed:
```bash
git status
```

**Make sure NOT to commit:**
- `venv/` folder (excluded by .gitignore)
- `*.docx` test files (excluded by .gitignore)
- `.env` files (excluded by .gitignore)
- `__pycache__/` (excluded by .gitignore)

## Step 3: Make Initial Commit

```bash
git commit -m "Initial commit - Syllabus Accessibility Checker web app"
```

## Step 4: Add GitHub Remote

```bash
git remote add origin https://github.com/dapclark/syllabus-checker.git
```

## Step 5: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

If you get authentication errors, you'll need to use a Personal Access Token (PAT):

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "syllabus-checker-deploy"
4. Select scopes: `repo` (all checkboxes under it)
5. Click "Generate token"
6. Copy the token (you won't see it again!)
7. When pushing, use:
   ```bash
   git push -u origin main
   ```
   - Username: `dapclark`
   - Password: `<paste-your-token-here>`

## Step 6: Verify

Visit: https://github.com/dapclark/syllabus-checker

You should see all your files!

## Future Updates

After making changes:
```bash
git add .
git commit -m "Description of changes"
git push
```

## Important Files Checklist

Before pushing, verify these exist:
- [ ] app.py
- [ ] syllabus_checker.py
- [ ] wsgi.py
- [ ] requirements.txt
- [ ] .gitignore
- [ ] templates/index.html
- [ ] templates/results.html
- [ ] templates/about.html
- [ ] Uniform-Syllabus-Template-1.docx
- [ ] HETZNER_DEPLOY.md
- [ ] DEPLOY_CHECKLIST.md
- [ ] README.md

## Files That Should NOT Be Pushed

(Already excluded by .gitignore):
- venv/
- __pycache__/
- .env
- uploads/
- Test .docx files (except the template)
