from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import secrets
import base64
import os
from datetime import datetime
import json

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBasic()

# Admin credentials (change these!)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "rimu_admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "rimu2024secure")

# Database file path
DATABASE_PATH = 'data/rimu_world.db'

# Database initialization
def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT,
            details TEXT,
            price REAL NOT NULL,
            sizes TEXT,
            colors TEXT,
            images TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# Create directories for uploads
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Models
class Product(BaseModel):
    name: str
    type: str
    category: Optional[str] = None
    details: str
    price: float
    sizes: Optional[List[str]] = None
    colors: Optional[List[str]] = None

# Helper functions
def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials.username

def generate_product_id():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM products')
    count = c.fetchone()[0]
    conn.close()
    return f"RW{count + 1:04d}"

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/admin", response_class=HTMLResponse)
async def admin_login():
    with open("templates/admin.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/products")
async def get_products(type: Optional[str] = None):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if type:
        c.execute('SELECT * FROM products WHERE type = ? ORDER BY created_at DESC', (type,))
    else:
        c.execute('SELECT * FROM products ORDER BY created_at DESC')
    
    products = []
    for row in c.fetchall():
        product = dict(row)
        product['sizes'] = json.loads(product['sizes']) if product['sizes'] else []
        product['colors'] = json.loads(product['colors']) if product['colors'] else []
        product['images'] = json.loads(product['images']) if product['images'] else []
        products.append(product)
    
    conn.close()
    return products

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = dict(row)
    product['sizes'] = json.loads(product['sizes']) if product['sizes'] else []
    product['colors'] = json.loads(product['colors']) if product['colors'] else []
    product['images'] = json.loads(product['images']) if product['images'] else []
    
    return product

@app.post("/api/admin/products")
async def create_product(
    name: str = Form(...),
    type: str = Form(...),
    category: str = Form(...),
    details: str = Form(...),
    price: float = Form(...),
    sizes: str = Form("[]"),
    colors: str = Form("[]"),
    images: List[UploadFile] = File(...),
    admin: str = Depends(verify_admin)
):
    product_id = generate_product_id()
    
    # Save images
    image_paths = []
    for idx, image in enumerate(images):
        if image.filename:
            ext = image.filename.split('.')[-1]
            filename = f"{product_id}_{idx}.{ext}"
            filepath = f"static/uploads/{filename}"
            
            with open(filepath, "wb") as f:
                content = await image.read()
                f.write(content)
            
            image_paths.append(f"/static/uploads/{filename}")
    
    # Insert into database
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO products (product_id, name, type, category, details, price, sizes, colors, images)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        product_id,
        name,
        type,
        category,
        details,
        price,
        sizes,
        colors,
        json.dumps(image_paths)
    ))
    
    conn.commit()
    conn.close()
    
    return {"message": "Product created successfully", "product_id": product_id}

@app.put("/api/admin/products/{product_id}")
async def update_product(
    product_id: str,
    name: str = Form(...),
    type: str = Form(...),
    category: str = Form(...),
    details: str = Form(...),
    price: float = Form(...),
    sizes: str = Form("[]"),
    colors: str = Form("[]"),
    images: Optional[List[UploadFile]] = File(None),
    existing_images: str = Form("[]"),
    admin: str = Depends(verify_admin)
):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Get existing product
    c.execute('SELECT images FROM products WHERE product_id = ?', (product_id,))
    row = c.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Handle images
    existing_image_list = json.loads(existing_images)
    image_paths = existing_image_list.copy()
    
    # Add new images if uploaded
    if images and images[0].filename:
        for idx, image in enumerate(images):
            if image.filename:
                ext = image.filename.split('.')[-1]
                filename = f"{product_id}_{len(image_paths) + idx}.{ext}"
                filepath = f"static/uploads/{filename}"
                
                with open(filepath, "wb") as f:
                    content = await image.read()
                    f.write(content)
                
                image_paths.append(f"/static/uploads/{filename}")
    
    # Update product in database
    c.execute('''
        UPDATE products 
        SET name = ?, type = ?, category = ?, details = ?, price = ?, sizes = ?, colors = ?, images = ?
        WHERE product_id = ?
    ''', (
        name,
        type,
        category,
        details,
        price,
        sizes,
        colors,
        json.dumps(image_paths),
        product_id
    ))
    
    conn.commit()
    conn.close()
    
    return {"message": "Product updated successfully", "product_id": product_id}

@app.delete("/api/admin/products/{product_id}")
async def delete_product(product_id: str, admin: str = Depends(verify_admin)):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Get images to delete
    c.execute('SELECT images FROM products WHERE product_id = ?', (product_id,))
    row = c.fetchone()
    
    if row:
        images = json.loads(row[0])
        for image_path in images:
            try:
                os.remove(image_path.lstrip('/'))
            except:
                pass
    
    c.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Product deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)