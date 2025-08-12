# QR Code Generator API - Northflank Deployment (JPEG Free)

## 🚀 Ready for Northflank Deployment

This package contains the complete QR Code Generator API with JPEG option removed from the frontend demo interface.

## ✅ What's Fixed

- **JPEG Removed**: No more JPEG option in URL and Text QR code forms
- **Clean Interface**: Only PNG, SVG, PDF options shown
- **Updated Documentation**: API docs updated to reflect available formats
- **All 8 Endpoints Working**: URL, Text, Email, Phone, SMS, vCard, WiFi, Location

## 📁 Files Included

### Core Application
- `app.py` - Main Flask application
- `qr_generator.py` - QR code generation engine
- `main.py` - Application entry point
- `Procfile` - Gunicorn configuration
- `requirements.txt` - Python dependencies
- `.python-version` - Python 3.11

### Frontend (Updated)
- `templates/northflank_index.html` - Demo interface (JPEG removed)
- `templates/northflank_api_docs.html` - API documentation (JPEG removed)  
- `static/css/styles.css` - Stylesheets
- `static/js/main.js` - JavaScript (JPEG handling removed)

## 🔄 Deployment Steps

1. **Upload Files**: Upload all files to your Northflank project
2. **Environment**: Python 3.11 (detected from `.python-version`)
3. **Build**: `pip install -r requirements.txt`
4. **Start**: `gunicorn --bind 0.0.0.0:$PORT --reuse-port --reload main:app`

## 🌐 Live URL
Your current deployment: https://site--qr-code-generator-api--lrw6bbnkrwj5.code.run/

## 📋 API Endpoints (All Working)
- POST `/api/v1/qr/url` - URL QR codes
- POST `/api/v1/qr/text` - Text QR codes  
- POST `/api/v1/qr/email` - Email QR codes
- POST `/api/v1/qr/phone` - Phone QR codes
- POST `/api/v1/qr/sms` - SMS QR codes
- POST `/api/v1/qr/vcard` - vCard QR codes
- POST `/api/v1/qr/wifi` - WiFi QR codes
- POST `/api/v1/qr/location` - Location QR codes

## 🎨 Demo Interface
- Clean, consistent format options across all QR types
- Only PNG, SVG, PDF formats available
- Professional Northflank branding
- Responsive Bootstrap design

Deploy this package to update your live site with the JPEG-free interface!