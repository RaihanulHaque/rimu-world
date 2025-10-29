# Rimu's World - Product Management System

A modern, fully responsive e-commerce platform built with FastAPI for managing fashion products (clothing and jewelry) with a beautiful admin interface.

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Development Setup](#-development-setup)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [API Reference](#-api-reference)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Support](#-support)

## ✨ Features

### 🛍️ Product Management
- **Product Catalog**: Display clothing and jewelry with images, sizes, colors
- **Product Types**: Support for clothing (1-piece, 2-piece, 3-piece) and jewelry (bangles, bracelets, necklaces, etc.)
- **Automatic ID Generation**: Unique product IDs (RW0001, RW0002, etc.)
- **Image Upload**: Multiple product images (up to 5 per product)

### 🔐 Admin Panel
- **Secure Authentication**: Basic HTTP authentication
- **Product CRUD**: Create, read, update, delete products
- **Color Picker**: Interactive color selection
- **Size Management**: Dynamic size selection (hidden for 3-piece sets)
- **Image Management**: Upload and manage product images

### 🎨 Frontend
- **Fully Responsive**: Works on desktop, tablet, and mobile
- **Modern UI**: Elegant design inspired by high-end fashion sites
- **Smooth Animations**: CSS transitions and JavaScript enhancements
- **Product Gallery**: Modal view with image carousel
- **Social Integration**: WhatsApp and Facebook contact buttons

### ⚙️ Backend
- **FastAPI Framework**: High-performance async web framework
- **SQLite Database**: Lightweight, file-based database
- **RESTful API**: Clean API endpoints
- **File Upload**: Secure image handling
- **CORS Support**: Cross-origin resource sharing enabled

### 🐳 DevOps
- **Docker Support**: Containerized deployment
- **Volume Persistence**: Database and uploads in Docker volumes
- **Environment Variables**: Configurable credentials

## 🚀 Quick Start

### With Docker (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd rimu-world
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - **Main Site**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin

4. **Default Admin Credentials:**
   - Username: `rimu_admin`
   - Password: `rimu2024secure`

## 💻 Development Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Local Installation

1. **Create project directory:**
   ```bash
   mkdir rimu-world
   cd rimu-world
   ```

2. **Create `requirements.txt`:**
   ```txt
   fastapi==0.104.1
   uvicorn[standard]==0.24.0
   python-multipart==0.0.6
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create directory structure:**
   ```bash
   mkdir -p templates static/uploads static/css static/js
   ```

5. **Place application files:**
   - `main.py` (FastAPI backend)
   - `templates/index.html` (main website)
   - `templates/admin.html` (admin panel)

6. **Run the application:**
   ```bash
   python main.py
   ```
   Or with auto-reload:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📁 Project Structure

```
rimu-world/
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker container config
├── docker-compose.yml         # Docker Compose setup
├── .dockerignore             # Docker build exclusions
├── README.md                 # This file
├── data/                     # Database directory (Docker)
│   └── rimu_world.db        # SQLite database
├── templates/
│   ├── index.html           # Main customer website
│   └── admin.html           # Admin management panel
└── static/
    ├── uploads/             # Product images
    ├── css/                # Stylesheets
    └── js/                 # JavaScript files
```

## 📖 Usage Guide

### For Customers

1. **Browse Products**: Visit http://localhost:8000
2. **Filter by Category**: Choose between Clothing and Jewelry sections
3. **View Product Details**: Click on any product to see full details, images, and options
4. **Contact to Order**: Use WhatsApp or Facebook buttons to place orders

### For Admins

#### Accessing Admin Panel
1. Go to http://localhost:8000/admin
2. Login with admin credentials

#### Adding Products
1. Click "Upload Product" tab
2. Fill in product information:
   - **Name**: Product name
   - **Type**: Clothing or Jewelry
   - **Category**: Specific category (1-piece, 2-piece, etc.)
   - **Price**: Price in BDT (৳)
   - **Details**: Product description
   - **Colors**: Select available colors
   - **Sizes**: Choose available sizes (not shown for 3-piece sets)
   - **Images**: Upload 1-5 high-quality product images
3. Click "Upload Product"

#### Managing Products
1. Click "Manage Products" tab
2. View all products in a table
3. Delete products using the delete button

## 🔌 API Reference

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main website page |
| `GET` | `/admin` | Admin login page |
| `GET` | `/api/products` | Get all products (with optional `type` filter) |
| `GET` | `/api/products/{product_id}` | Get specific product details |

### Admin Endpoints (Require Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/admin/products` | Create new product |
| `DELETE` | `/api/admin/products/{product_id}` | Delete product |

### Authentication
Admin endpoints use HTTP Basic Authentication with credentials defined in environment variables or `main.py`.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_secure_password
```

### Contact Information

Update `templates/index.html` for contact details:

**WhatsApp Integration** (around line 660):
```javascript
const WHATSAPP_NUMBER = '8801XXXXXXXXX'; // Your WhatsApp number
const FACEBOOK_PAGE = 'https://facebook.com/yourpage'; // Your Facebook page
```

**Footer Contact Info** (around line 610):
```html
<p>📞 WhatsApp: +880-XXXX-XXXXXX</p>
<p>📘 Facebook: @yourhandle</p>
<p>✉️ Email: hello@yourdomain.com</p>
```

### Security Notes
- **Change default admin credentials** before production deployment
- Use strong, unique passwords
- Consider implementing additional security measures for production

## 🚀 Deployment

### Docker Deployment (Recommended)

1. **Build and run:**
   ```bash
   docker-compose up --build -d
   ```

2. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop application:**
   ```bash
   docker-compose down
   ```

### Production Deployment

1. **Use environment variables** for credentials
2. **Set up reverse proxy** (nginx recommended)
3. **Enable HTTPS** with SSL certificate
4. **Configure domain** and DNS
5. **Set up monitoring** and logging
6. **Regular database backups**

### Production Server Example

```bash
# Using gunicorn for production
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔧 Troubleshooting

### Common Issues

**Images not loading:**
- Verify `static/uploads/` directory exists and has proper permissions
- Check image file paths in database

**Admin login fails:**
- Confirm credentials in `main.py` or environment variables
- Check browser developer console for errors

**Database errors:**
- Delete `rimu_world.db` (or `data/rimu_world.db` in Docker)
- Restart application (database recreates automatically)

**Port 8000 already in use:**
- Change port in `main.py` or use different port:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8080
  ```

**Docker build fails:**
- Ensure Docker and Docker Compose are installed
- Check for syntax errors in Dockerfile

### Performance Tips

- Upload high-quality images (800x800px recommended)
- Monitor `static/uploads/` folder size
- Regular database backups
- Use production WSGI server for high traffic

## 📞 Support

### Getting Help

If you encounter issues:

1. **Check logs**: `docker-compose logs` or application console output
2. **Verify file locations**: Ensure all files are in correct directories
3. **Check Python version**: Requires Python 3.8+
4. **Port availability**: Ensure port 8000 is not in use

### Product ID System

- **Format**: RW0001, RW0002, etc.
- **RW**: Rimu's World identifier
- **4-digit number**: Sequential product numbering
- **Auto-generated**: Created automatically on product upload

### Customer Order Flow

1. Customer browses and selects products
2. Notes Product ID (e.g., RW0001)
3. Contacts via WhatsApp/Facebook with Product ID, size, and color
4. Shop owner manually confirms and processes order

---

**Built with ❤️ for Rimu's World - Modern Fashion E-commerce**