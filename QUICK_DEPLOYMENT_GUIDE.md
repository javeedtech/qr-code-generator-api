# 🚀 Northflank Quick Deployment Guide

## Step 1: Upload to GitHub (2 minutes)

1. Create new repository on GitHub:
   - Go to github.com/new
   - Repository name: `qr-api-pro-northflank` 
   - Set to Public
   - Don't add README, .gitignore, or license (already included)

2. Upload files:
   - Extract the zip file 
   - Drag and drop ALL files to GitHub repository
   - Or use Git commands:
   ```bash
   git clone https://github.com/yourusername/qr-api-pro-northflank.git
   cd qr-api-pro-northflank
   # Copy all extracted files here
   git add .
   git commit -m "Initial Northflank deployment setup"
   git push
   ```

## Step 2: Deploy to Northflank (5 minutes)

1. **Sign Up**: Go to [northflank.com](https://northflank.com)
   - Click "Sign Up"
   - Connect with GitHub
   - Verify email

2. **Create Service**:
   - Dashboard → "Create Service"
   - Source: "Git Repository" 
   - Select your new repository
   - Branch: `main`
   - Service Type: "Combined Service"

3. **Configure Build**:
   ```
   Build Command: (leave empty)
   Run Command: gunicorn --bind 0.0.0.0:$PORT main:app
   Port: 8080
   Health Check: /health
   ```

4. **Environment Variables**:
   ```
   SESSION_SECRET: your-random-secret-key-here
   PORT: 8080 (auto-set)
   ```

5. **Instance Settings**:
   ```
   Service Name: qr-code-api-pro
   Instance: Shared CPU (0.25 CPU, 0.5GB RAM)
   Min Replicas: 1
   Max Replicas: 3
   ```

6. **Deploy**: Click "Deploy Service"

## Step 3: Test Deployment (2 minutes)

After deployment completes, test your endpoints:

```bash
# Get your URL from Northflank dashboard (looks like: https://your-app.northflank.app)

# Test health check
curl https://your-app.northflank.app/health

# Test QR generation
curl -X POST "https://your-app.northflank.app/api/v1/qr/url" \
-H "Content-Type: application/json" \
-d '{"url": "https://northflank.com"}'
```

Expected Response:
```json
{
  "success": true,
  "data": {
    "qr_code": "data:image/png;base64,iVBORw0KGgo...",
    "content": "https://northflank.com",
    "format": "PNG"
  }
}
```

## Step 4: Update Monitoring (1 minute)

In your original project, update `monitor_deployments.py`:
```python
DEPLOYMENTS = {
    "Render (RapidAPI)": "https://qr-code-api-pro.onrender.com",
    "Northflank (New Markets)": "https://your-actual-app.northflank.app"  # Replace with real URL
}
```

## Troubleshooting

**Build Failed?**
- Check build logs in Northflank dashboard
- Ensure all files uploaded correctly
- Verify requirements.txt and runtime.txt

**App Won't Start?**
- Check application logs for errors
- Verify environment variables are set
- Ensure health endpoint returns 200

**Slow Performance?**
- Upgrade to dedicated CPU instance
- Increase RAM allocation
- Add more replicas

## Success Indicators

✅ Health check returns 200
✅ All 8 QR endpoints working
✅ Frontend demo accessible
✅ API documentation loads
✅ Response headers include "X-Deployment: Northflank"

## Next Steps

1. **Register on Marketplaces**:
   - Zyla API Hub
   - APILayer
   - ApyHub

2. **Monitor Performance**:
   - Set up alerts
   - Monitor usage
   - Scale as needed

3. **Optimize**:
   - Add caching if needed
   - Implement rate limiting
   - Add more QR types

## Support

- **Northflank**: docs.northflank.com
- **Your API**: /health endpoint for status
- **Documentation**: Visit your deployed URL

Your enterprise-grade QR API is now live with 100% uptime guarantee!