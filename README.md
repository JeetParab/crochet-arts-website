# Crochet Arts - Handmade Crochet Website

A beautiful mobile-friendly website for a solo crochet artist to showcase products, manage inventory, and accept inquiries via WhatsApp.

Built with **Flask** + Tailwind CSS. Designed to run easily on phones (Termux) and deploy to free platforms.

## Features
- Mobile-first beautiful design
- Add / Edit / Delete products with image upload
- Wishlist + Bulk WhatsApp inquiry
- Direct "DM to Buy" buttons
- Admin panel (protected by simple code)
- Persistent storage using JSON file

## Local Development (Termux / Any Linux)

```bash
# Clone the repo
git clone <your-repo-url>
cd crochet-site-v2

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open: **http://127.0.0.1:5000**

**Admin Code:** `crochet2026`

## Deployment

### Recommended: Render.com (Easiest)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com)
3. Create new **Web Service**
4. Connect GitHub repo
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `python app.py`
7. Add a **Persistent Disk** mounted at `/opt/render/project/src/data`

### Alternative: PythonAnywhere

Very beginner friendly.

### Alternative: AWS (Lightsail / Elastic Beanstalk)

You can deploy on AWS Free Tier using Lightsail or Elastic Beanstalk.

## Important Notes

- Change the WhatsApp number in `app.py`
- For production, consider moving image uploads to S3
- Never commit real customer data

## Tech Stack
- Python + Flask
- Tailwind CSS (via CDN)
- Local JSON storage + file uploads

Made for small handmade businesses.
