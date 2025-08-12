# QR Code Generator API - Clean Deployment Package

## Format Support: PNG, SVG, PDF Only

This package provides consistent format support across all interfaces:

### Supported Formats
- **PNG** - High quality raster images, best for web display
- **SVG** - Scalable vector graphics, perfect for responsive design  
- **PDF** - Document format, ideal for printing and archival

### What's Cleaned Up
- Removed JPEG format references for consistency
- All demo interfaces show only PNG, SVG, PDF options
- API documentation updated to match supported formats
- Backend properly handles the three supported formats

### Essential Files Only
- `app.py` - Main Flask application with all API endpoints
- `qr_generator.py` - QR code generation engine (PNG/SVG/PDF)
- `main.py` - Application entry point
- `templates/index.html` - Demo interface with consistent formats
- `templates/api_docs.html` - API documentation
- `static/css/styles.css` - Complete styling
- `static/js/main.js` - JavaScript functionality
- Deployment files: Procfile, .python-version, requirements.txt, .gitignore

### Deployment Instructions
1. Download and extract this package
2. Replace ALL files in your GitHub repository 
3. Commit and push to GitHub
4. Redeploy on Northflank

All format options are now consistent across demo interface, API documentation, and backend implementation.