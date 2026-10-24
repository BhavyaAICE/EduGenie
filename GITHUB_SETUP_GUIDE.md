# Frankenstein Web & Deploy: GitHub Repository Setup & Publication Guide

This document provides organizers with the exact commands and workflow to publish the three participant repositories to GitHub for the **Frankenstein Web & Deploy** challenge.

> **Note**: Each repository directory on your local filesystem is already initialized as a distinct Git repository with an initial commit containing all required files and component documentation.

---

## 1. Prerequisites for Organizers

1. **GitHub Account or Organization**: Create three public (or private with team access) repositories on GitHub:
   - `frankenstein-edugenie-frontend`
   - `frankenstein-edugenie-backend`
   - `frankenstein-edugenie-features`
2. **Git Credentials**: Ensure your local terminal is authenticated to GitHub (via SSH key or GitHub CLI `gh auth login`).

---

## 2. Step-by-Step Commands to Push Each Repository

### Repository 1: Frontend (`frankenstein-edugenie-frontend`)

Run these commands from the `frankenstein-edugenie-frontend` folder:

```bash
cd c:\Users\Bhavy\Desktop\EduGenie\frankenstein-edugenie-frontend

# Rename default branch to main if not already
git branch -M main

# Add remote origin (replace <your-org> with your GitHub user or organization name)
git remote add origin https://github.com/<your-org>/frankenstein-edugenie-frontend.git

# Push to GitHub
git push -u origin main
```

*(If using GitHub CLI, you can create and push in one command)*:
```bash
gh repo create <your-org>/frankenstein-edugenie-frontend --public --source=. --remote=origin --push
```

---

### Repository 2: Backend (`frankenstein-edugenie-backend`)

Run these commands from the `frankenstein-edugenie-backend` folder:

```bash
cd c:\Users\Bhavy\Desktop\EduGenie\frankenstein-edugenie-backend

# Rename default branch to main
git branch -M main

# Add remote origin
git remote add origin https://github.com/<your-org>/frankenstein-edugenie-backend.git

# Push to GitHub
git push -u origin main
```

*(Using GitHub CLI)*:
```bash
gh repo create <your-org>/frankenstein-edugenie-backend --public --source=. --remote=origin --push
```

---

### Repository 3: Features (`frankenstein-edugenie-features`)

Run these commands from the `frankenstein-edugenie-features` folder:

```bash
cd c:\Users\Bhavy\Desktop\EduGenie\frankenstein-edugenie-features

# Rename default branch to main
git branch -M main

# Add remote origin
git remote add origin https://github.com/<your-org>/frankenstein-edugenie-features.git

# Push to GitHub
git push -u origin main
```

*(Using GitHub CLI)*:
```bash
gh repo create <your-org>/frankenstein-edugenie-features --public --source=. --remote=origin --push
```

---

## 3. Published Participant Clone URLs

The three challenge repositories are published and accessible to participants at:

```bash
git clone https://github.com/BhavyaAICE/frankenstein-edugenie-frontend.git
git clone https://github.com/BhavyaAICE/frankenstein-edugenie-backend.git
git clone https://github.com/BhavyaAICE/frankenstein-edugenie-features.git
```

---

## 4. Pre-Event Organizer Checklist

- [ ] Verify all three repositories are marked **Public** (or that participating teams have read permissions).
- [ ] Confirm that `ORGANIZER_SOLUTION.md`, `VERIFICATION_REPORT.md`, `INTEGRATION_REFERENCE.md`, and `EduGenie_reference_repaired/` are **NOT** pushed to the participant repositories.
- [ ] Confirm no actual `.env` files or API secrets were committed.
- [ ] Test cloning all three repositories into a fresh directory using a non-admin GitHub account to verify accessibility.
