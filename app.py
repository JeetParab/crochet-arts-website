#!/usr/bin/env python3
"""
Crochet Business Site - Flask Backend (Lightweight for Termux)
Beautiful mobile-first site with real persistence + image uploads.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = "crochet-super-secret-2026"  # Change this in production
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB max upload

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==================== DATA HELPERS ====================
def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    # Seed data on first run
    seed = [
        {
            "id": 1,
            "name": "Mini Elephant Amigurumi",
            "price": 450,
            "category": "Amigurumi",
            "description": "Adorable little elephant toy made with soft cotton yarn. Perfect as a baby gift or nursery decor.",
            "imageUrl": "/static/uploads/placeholder.jpg",
            "status": "available",
            "created_at": "2026-05-20T10:00:00"
        },
        {
            "id": 2,
            "name": "Boho Plant Hanger",
            "price": 380,
            "category": "Home Decor",
            "description": "Hand-crocheted plant hanger. Fits 6-8 inch pots beautifully.",
            "imageUrl": "/static/uploads/placeholder.jpg",
            "status": "available",
            "created_at": "2026-05-18T14:30:00"
        },
        {
            "id": 3,
            "name": "Mandala Coaster Set (4 pcs)",
            "price": 290,
            "category": "Coasters",
            "description": "Set of 4 intricate mandala coasters. Great as gifts.",
            "imageUrl": "/static/uploads/placeholder.jpg",
            "status": "available",
            "created_at": "2026-05-15T09:15:00"
        }
    ]
    save_products(seed)
    return seed

def save_products(products):
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

def get_product_by_id(product_id):
    products = load_products()
    return next((p for p in products if p["id"] == product_id), None)

# ==================== ROUTES ====================
@app.route('/')
def index():
    products = load_products()
    return render_template('index.html', products=products, config={
        "makerName": "Crochet Arts",
        "whatsappNumber": "919876543210",  # ← Change this
        "instagram": "@aarohiscrochet"
    })

@app.route('/api/products')
def api_get_products():
    return jsonify(load_products())

@app.route('/api/product/add', methods=['POST'])
def api_add_product():
    data = request.form
    file = request.files.get('image')

    products = load_products()

    new_id = max([p['id'] for p in products], default=0) + 1

    image_url = "/static/uploads/placeholder.jpg"
    if file and file.filename:
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"
        filepath = os.path.join(UPLOAD_DIR, unique_name)
        file.save(filepath)
        image_url = f"/static/uploads/{unique_name}"

    new_product = {
        "id": new_id,
        "name": data.get('name', 'Untitled'),
        "price": int(data.get('price', 0)),
        "category": data.get('category', 'Other'),
        "description": data.get('description', ''),
        "imageUrl": image_url,
        "status": data.get('status', 'available'),
        "created_at": datetime.now().isoformat()
    }

    products.insert(0, new_product)
    save_products(products)
    return jsonify({"success": True, "product": new_product})

@app.route('/api/product/edit/<int:product_id>', methods=['POST'])
def api_edit_product(product_id):
    data = request.form
    file = request.files.get('image')

    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"success": False, "error": "Not found"}), 404

    product['name'] = data.get('name', product['name'])
    product['price'] = int(data.get('price', product['price']))
    product['category'] = data.get('category', product['category'])
    product['description'] = data.get('description', product['description'])
    product['status'] = data.get('status', product.get('status', 'available'))

    if file and file.filename:
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"
        filepath = os.path.join(UPLOAD_DIR, unique_name)
        file.save(filepath)
        product['imageUrl'] = f"/static/uploads/{unique_name}"

    save_products(products)
    return jsonify({"success": True, "product": product})

@app.route('/api/product/delete/<int:product_id>', methods=['POST'])
def api_delete_product(product_id):
    products = load_products()
    products = [p for p in products if p["id"] != product_id]
    save_products(products)
    return jsonify({"success": True})

@app.route('/api/stats')
def api_stats():
    products = load_products()
    total_items = len(products)
    total_value = sum(p['price'] for p in products)
    categories = {}
    for p in products:
        cat = p.get('category', 'Other')
        categories[cat] = categories.get(cat, 0) + 1

    return jsonify({
        "total_items": total_items,
        "total_value": total_value,
        "categories": categories
    })

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# Simple admin protection (optional)
@app.route('/admin')
def admin_page():
    # For now just redirect to main (we use JS prompt in frontend)
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🧶 Crochet Site running!")
    print("Open: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)