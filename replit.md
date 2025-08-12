# QR Code Generator API

## Overview

This is a Flask-based QR code generation API that provides web endpoints for creating customizable QR codes. The application offers both a demo interface and comprehensive API documentation, designed to serve as a professional QR code generation service with advanced styling and formatting options.

The system supports multiple QR code types with extensive customization capabilities including colors, module shapes, error correction levels, and various output formats. It's built with a focus on ease of use while providing powerful features for developers and businesses.

## User Preferences

Preferred communication style: Simple, everyday language.
Monetization focus: Competitive pricing strategy for RapidAPI with 5-tier structure starting at 500 free requests.
Deployment preference: GitHub + Render for backend API deployment.

## System Architecture

### Web Framework Architecture
- **Flask-based REST API**: Uses Flask as the lightweight web framework with CORS enabled for cross-origin requests
- **Template-driven frontend**: Implements server-side rendering using Jinja2 templates for the demo interface and documentation
- **Modular design**: Separates core QR generation logic into a dedicated `QRCodeGenerator` class for better maintainability

### QR Code Generation Engine
- **PIL/Pillow integration**: Uses Python Imaging Library for advanced image processing and styling
- **qrcode library foundation**: Built on the `qrcode` Python library with custom styling extensions
- **Multiple module drawer support**: Implements square, rounded, and circle module drawing styles
- **Color customization**: Supports solid fills and gradient color masks (square and radial gradients)
- **Error correction flexibility**: Configurable error correction levels (L, M, Q, H) for different reliability needs

### Frontend Architecture
- **Bootstrap-based responsive design**: Uses Bootstrap 5 for consistent, mobile-first UI components
- **Progressive enhancement**: JavaScript-driven interactive features with graceful degradation
- **Real-time preview system**: Implements live QR code generation and preview updates
- **Tabbed interface**: Organizes different QR code types (URL, text, etc.) in a clean tabbed layout
- **Complete customization UI**: Full frontend controls for size, format (PNG/JPEG/PDF), shapes (square/rounded/circle), error correction levels, and both foreground/background colors
- **Advanced download system**: Format-aware file downloads with proper MIME types and extensions

### API Design Patterns
- **RESTful endpoints**: Follows REST conventions with versioned API structure (`/api/v1/`)
- **JSON request/response**: Standard JSON communication format for all API interactions
- **Options-based configuration**: Flexible parameter system allowing default options with custom overrides
- **Rate limiting headers**: Includes rate limiting information for API consumers (designed for RapidAPI integration)

### File Organization
- **Static asset separation**: CSS and JavaScript files organized in dedicated static directories
- **Template inheritance**: HTML templates structured for reusability and maintenance
- **Entry point separation**: Main application logic separated from the Flask app initialization

## External Dependencies

### Core Libraries
- **Flask**: Web framework for API endpoints and template rendering
- **Flask-CORS**: Cross-Origin Resource Sharing support for API access
- **qrcode**: Primary QR code generation library with PIL integration
- **Pillow (PIL)**: Image processing and manipulation capabilities
- **ReportLab**: PDF generation functionality for QR code output

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded via CDN for responsive design
- **Font Awesome 6**: Icon library for UI elements
- **Prism.js**: Syntax highlighting for API documentation code examples

### Development Tools
- **Python logging**: Built-in logging system for debugging and monitoring
- **Environment variable support**: Configuration through environment variables for deployment flexibility

### Potential Integrations
- **RapidAPI compatibility**: Headers and structure prepared for RapidAPI marketplace integration
- **Logo embedding**: Framework in place for adding custom logos to QR codes
- **Multiple format export**: Support for PNG, PDF, and other output formats

## Competitive Pricing Strategy

The API uses a 5-tier pricing structure designed to attract paying customers while remaining competitive:

### Tier Structure
- **Free**: $0/mo - 500 requests/month, 1 req/sec rate limit
- **Starter**: $5/mo - 2,000 requests + $0.05 overage, 2 req/sec rate limit
- **Basic**: $7/mo - 5,000 requests + $0.03 overage, 3 req/sec rate limit  
- **Pro**: $12.99/mo - 15,000 requests + $0.02 overage, 5 req/sec rate limit
- **Ultra**: $49/mo - 100,000 requests + $0.01 overage, 10 req/sec rate limit

### Competitive Advantages
- 500 free requests (vs competitors' typical 100-200)
- Lower overage rates than market leaders
- All QR code types included in every tier
- Progressive rate limits encouraging upgrades
- Clear value proposition with batch processing and priority support

## Deployment Configuration

### Multi-Platform Deployment Support
- **GitHub + Render Setup**: Primary deployment configuration with render.yaml and Procfile
- **Northflank Deployment**: Successfully deployed at https://site--qr-code-generator-api--lrw6bbnkrwj5.code.run/
- **Runtime specification**: Python 3.11 for compatibility across platforms
- **Static assets**: Organized for CDN deployment
- **Environment variables**: SESSION_SECRET for Flask security
- **Keep-alive service**: Automatic pinging every 5 minutes to prevent Render free tier sleeping

### Northflank Configuration (August 2025)
- **Python version file**: Uses `.python-version` with `3.11` format (not `runtime.txt`)
- **Build requirements**: Replaced old `runtime.txt` (python-3.11.8) with `.python-version` file
- **Deployment package**: Updated zip file available via `/download-northflank` route
- **Live deployment**: Successfully running at https://site--qr-code-generator-api--lrw6bbnkrwj5.code.run/
- **Download page path**: `/download-northflank` - for providing updated deployment packages

### User Preferences
- **Frontend branding**: User prefers Northflank-specific branding over RapidAPI references
- **Download access**: Wants easy access to updated zip files via preview window
- **Frontend completeness**: Fully restored all customization options to match API capabilities
- **Format support**: Confirmed working JPEG and enhanced SVG generation with optimized rendering

### Keep-Alive Implementation
- **keep_alive.py**: Background service that pings `/health` endpoint every 5 minutes
- **Production-only activation**: Only runs when `RENDER` environment variable is set
- **Health endpoint**: `/health` route for monitoring and keep-alive pings
- **Graceful error handling**: Continues running even if individual pings fail
- **Logging**: Comprehensive logging of keep-alive activities

### File Structure for Deployment
- All templates and static files properly organized
- API endpoints follow REST conventions with versioning
- Rate limiting headers prepared for RapidAPI integration
- Error handling and logging configured for production
- DEPLOYMENT.md guide for GitHub + Render deployment process