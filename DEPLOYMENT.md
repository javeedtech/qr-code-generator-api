# QR Code API Pro - Northflank Deployment Guide

## Overview

This guide will help you deploy the QR Code Generator API Pro to Northflank for 100% uptime and enterprise-grade performance. This deployment is specifically configured for multiple API marketplaces including Zyla API Hub, APILayer, and ApyHub.

## Prerequisites

1. **GitHub Account** with your repository
2. **Northflank Account** (sign up at [northflank.com](https://northflank.com))
3. **Your QR API code** (this repository)

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your GitHub repository contains these files:

```
your-repo/
├── app.py                 # Main Flask application
├── main.py               # Entry point
├── qr_generator.py       # QR generation logic
├── requirements.txt      # Python dependencies
├── Procfile             # Gunicorn configuration
├── runtime.txt          # Python version
├── templates/           # HTML templates
├── static/             # CSS & JS files
└── README.md           # Documentation
```

### 2. Sign Up for Northflank

1. Go to [northflank.com](https://northflank.com)
2. Click "Sign Up" and connect with your GitHub account
3. Verify your email address
4. Complete account setup

### 3. Create a New Service

1. **Dashboard**: Click "Create Service" 
2. **Source**: Select "Git Repository"
3. **Repository**: Choose your QR API repository
4. **Branch**: Select `main` or your deployment branch
5. **Service Type**: Choose "Combined Service"

### 4. Configure Build Settings

**Build Configuration:**
- **Build Command**: Leave empty (automatic detection)
- **Run Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
- **Dockerfile**: Not needed (Python buildpack)

**Environment Variables:**
```
SESSION_SECRET=your-secret-key-here
PORT=8080
```

### 5. Configure Deployment Settings

**Service Configuration:**
- **Service Name**: `qr-code-api-pro`
- **Instance**: `Shared CPU - 0.25 CPU, 0.5GB RAM` (start small)
- **Min Replicas**: 1
- **Max Replicas**: 3 (auto-scaling)

**Network Configuration:**
- **Port**: 8080
- **Protocol**: HTTP
- **Health Check**: `/health`

### 6. Set Up Custom Domain (Optional)

1. Go to **Service Settings** → **Domains**
2. Add your custom domain or use the provided `.northflank.app` domain
3. Configure DNS records as shown

### 7. Deploy and Test

1. Click **"Deploy Service"**
2. Wait for build completion (3-5 minutes)
3. Test your endpoints:

```bash
# Health check
curl https://your-app.northflank.app/health

# Test QR generation
curl -X POST "https://your-app.northflank.app/api/v1/qr/url" \
-H "Content-Type: application/json" \
-d '{"url": "https://northflank.com"}'
```

## Configuration Details

### Procfile Configuration
```
web: gunicorn --bind 0.0.0.0:$PORT --reuse-port --reload main:app
```

### Requirements.txt
```
flask==3.0.0
flask-cors==4.0.0
qrcode==7.4.2
pillow==10.2.0
reportlab==4.0.8
gunicorn==21.2.0
```

### Runtime.txt
```
python-3.11.8
```

## Environment Variables

Set these in Northflank dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `SESSION_SECRET` | Random string | Flask session encryption |
| `PORT` | 8080 | Application port (auto-set) |

## Monitoring and Scaling

### Health Monitoring
- **Health Endpoint**: `/health`
- **Monitoring**: Built into Northflank dashboard
- **Alerts**: Configure in Settings → Alerts

### Auto-Scaling
- **CPU Threshold**: 70% (recommended)
- **Memory Threshold**: 80% (recommended)
- **Min Replicas**: 1
- **Max Replicas**: 5

### Logs
Access logs via:
1. Northflank Dashboard → Your Service → Logs
2. Real-time log streaming available
3. Log retention: 7 days (upgrade for more)

## API Marketplace Integration

### Update Base URLs

After deployment, update your marketplace documentation:

```javascript
// Old RapidAPI URL (keep unchanged)
"https://qr-code-api-pro.onrender.com"

// New Northflank URL (use for new marketplaces)
"https://your-app.northflank.app"
```

### Marketplace-Specific Headers

Your API automatically includes deployment headers:

```json
{
  "X-Deployment": "Northflank",
  "X-RateLimit-Limit": "10000",
  "X-RateLimit-Remaining": "9999"
}
```

## Cost Optimization

### Northflank Pricing
- **Shared CPU**: $7/month (0.25 CPU, 0.5GB RAM)
- **Dedicated CPU**: $19/month (1 CPU, 1GB RAM)
- **Auto-scaling**: Only pay for what you use

### Optimization Tips
1. **Start Small**: Begin with shared CPU
2. **Monitor Usage**: Use Northflank analytics
3. **Scale on Demand**: Enable auto-scaling
4. **Cache Static Assets**: Use CDN for images/CSS

## Troubleshooting

### Common Issues

**Build Failures:**
```bash
# Check build logs in Northflank dashboard
# Ensure requirements.txt is correct
# Verify Python version in runtime.txt
```

**Application Won't Start:**
```bash
# Check if PORT environment variable is set
# Verify Procfile syntax
# Check application logs for errors
```

**Health Check Failures:**
```bash
# Ensure /health endpoint returns 200
# Check application is binding to 0.0.0.0:$PORT
# Verify no startup errors in logs
```

### Performance Issues

**Slow Response Times:**
1. **Upgrade Instance**: Move to dedicated CPU
2. **Enable Caching**: Add Redis if needed
3. **Optimize Code**: Profile with logs
4. **Add Replicas**: Increase min replicas

**High Memory Usage:**
1. **Profile Memory**: Check for memory leaks
2. **Optimize Images**: Use efficient image processing
3. **Upgrade RAM**: Increase instance size

## Security

### Best Practices
1. **Environment Variables**: Never commit secrets to git
2. **HTTPS Only**: Northflank provides SSL certificates
3. **Rate Limiting**: Implement API rate limits
4. **CORS**: Configure allowed origins

### Security Headers
Your app automatically includes:
- `X-Deployment: Northflank`
- CORS headers via Flask-CORS
- Standard security headers

## Support

### Northflank Support
- **Documentation**: [docs.northflank.com](https://docs.northflank.com)
- **Community**: Discord and GitHub discussions
- **Email**: support@northflank.com

### API Support
- **Health Check**: Monitor `/health` endpoint
- **Status Codes**: Standard HTTP status codes
- **Error Handling**: Comprehensive error responses

## Next Steps

1. **Monitor Performance**: Set up alerts and monitoring
2. **Register on Marketplaces**: Submit to Zyla, APILayer, ApyHub
3. **Scale as Needed**: Increase resources based on usage
4. **Add Features**: Implement additional QR types if needed

## Success Checklist

- [ ] Repository prepared with all required files
- [ ] Northflank account created and verified
- [ ] Service deployed successfully
- [ ] Health check endpoint responding
- [ ] All QR generation endpoints tested
- [ ] Custom domain configured (optional)
- [ ] Monitoring and alerts set up
- [ ] Documentation updated with new base URL
- [ ] Ready for marketplace submission

Your QR Code API Pro is now deployed on enterprise-grade infrastructure with guaranteed uptime and global reach!