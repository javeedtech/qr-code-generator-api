# QR Code Generator API - Northflank Deployment

## Overview

Professional QR code generation API with advanced customization options, deployed on Northflank for 100% uptime and high availability. This deployment serves multiple API marketplaces including Zyla API Hub, APILayer, and ApyHub.

## Features

- **8 QR Code Types**: URL, Text, Email, Phone, SMS, vCard, WiFi, Location
- **Advanced Styling**: Custom colors, shapes, error correction levels
- **Multiple Formats**: PNG, SVG, PDF output
- **High Performance**: Base64 encoded responses for fast integration
- **100% Uptime**: Deployed on Northflank for guaranteed availability
- **Global Reach**: Optimized for worldwide API marketplace distribution

## Quick Start

### Base URL
```
https://your-app.northflank.app
```

### Example Request
```bash
curl -X POST "https://your-app.northflank.app/api/v1/qr/url" \
-H "Content-Type: application/json" \
-d '{"url": "https://example.com", "options": {"size": 10, "format": "PNG"}}'
```

### Example Response
```json
{
  "success": true,
  "data": {
    "qr_code": "data:image/png;base64,iVBORw0KGgo...",
    "content": "https://example.com",
    "format": "PNG",
    "options": {...}
  }
}
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/v1/qr/url` - Generate URL QR codes
- `POST /api/v1/qr/text` - Generate text QR codes
- `POST /api/v1/qr/email` - Generate email QR codes
- `POST /api/v1/qr/phone` - Generate phone QR codes
- `POST /api/v1/qr/sms` - Generate SMS QR codes
- `POST /api/v1/qr/vcard` - Generate contact QR codes
- `POST /api/v1/qr/wifi` - Generate WiFi QR codes
- `POST /api/v1/qr/location` - Generate location QR codes

## Deployment

This API is deployed on Northflank for:
- Zero downtime
- High availability
- Fast global response times
- Automatic scaling

## Documentation

Visit the deployed API for interactive documentation:
- Demo: `https://your-app.northflank.app/`
- API Docs: `https://your-app.northflank.app/docs`

## Marketplace Integration

This deployment serves:
- Zyla API Hub
- APILayer  
- ApyHub
- AWS Marketplace
- Other premium API marketplaces

## Support

For technical support or enterprise inquiries, please contact our API team.