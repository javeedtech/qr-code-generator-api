// QR Code Generator Pro - Northflank Deployment JavaScript

// Global variables
let currentQRData = null;
let currentQRBlob = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDemo();
    generateHeroQR();
    setupFormValidation();
});

// Initialize demo functionality
function initializeDemo() {
    // Add smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add animation to feature cards on scroll
    observeElements();
}

// Generate demo QR for hero section
function generateHeroQR() {
    const canvas = document.getElementById('heroQR');
    if (canvas) {
        createSimpleQR(canvas, 'https://northflank.com', 300);
    }
}

// Create a simple QR code visualization
function createSimpleQR(canvas, text, size) {
    const ctx = canvas.getContext('2d');
    const moduleSize = 10;
    const modules = Math.floor(size / moduleSize);
    
    // Clear and set background
    ctx.clearRect(0, 0, size, size);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, size, size);
    
    // Create a simple QR-like pattern
    ctx.fillStyle = '#000000';
    
    // Create finder patterns (corners)
    drawFinderPattern(ctx, 0, 0, moduleSize);
    drawFinderPattern(ctx, size - 7 * moduleSize, 0, moduleSize);
    drawFinderPattern(ctx, 0, size - 7 * moduleSize, moduleSize);
    
    // Fill with random-like pattern based on text
    const seed = hashCode(text);
    for (let x = 8; x < modules - 8; x++) {
        for (let y = 8; y < modules - 8; y++) {
            if (seededRandom(seed + x * 31 + y) > 0.5) {
                ctx.fillRect(x * moduleSize, y * moduleSize, moduleSize, moduleSize);
            }
        }
    }
}

// Draw QR finder pattern (corner squares)
function drawFinderPattern(ctx, startX, startY, moduleSize) {
    // Outer square
    ctx.fillRect(startX, startY, 7 * moduleSize, 7 * moduleSize);
    // Inner white square
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(startX + moduleSize, startY + moduleSize, 5 * moduleSize, 5 * moduleSize);
    // Center black square
    ctx.fillStyle = '#000000';
    ctx.fillRect(startX + 2 * moduleSize, startY + 2 * moduleSize, 3 * moduleSize, 3 * moduleSize);
}

// Simple hash function for seeding
function hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash);
}

// Seeded random function
function seededRandom(seed) {
    const x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
}

// QR Code Generation Functions
async function generateQR(type) {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const qrResult = document.getElementById('qrResult');
    
    // Show loading
    loadingSpinner.classList.remove('d-none');
    qrResult.classList.add('d-none');
    
    try {
        const requestData = buildRequestData(type);
        const response = await fetch(`/api/v1/qr/${type}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayQRResult(data);
        } else {
            showError(data.error || 'Failed to generate QR code');
        }
    } catch (error) {
        console.error('Error generating QR code:', error);
        showError('Network error: ' + error.message);
    } finally {
        loadingSpinner.classList.add('d-none');
    }
}

// Build request data based on QR type
function buildRequestData(type) {
    const baseOptions = {
        size: 10,
        format: 'PNG',
        foreground_color: '#000000',
        background_color: '#FFFFFF',
        error_correction: 'M',
        module_drawer: 'square'
    };
    
    let requestData = { options: baseOptions };
    
    // Get common options for each type
    function getTypeOptions(prefix) {
        const sizeEl = document.getElementById(prefix + 'Size');
        const formatEl = document.getElementById(prefix + 'Format');
        const shapeEl = document.getElementById(prefix + 'Shape');
        const errorCorrectionEl = document.getElementById(prefix + 'ErrorCorrection');
        const foregroundEl = document.getElementById(prefix + 'ForegroundColor');
        const backgroundEl = document.getElementById(prefix + 'BackgroundColor');
        
        const options = {};
        if (sizeEl) options.size = parseInt(sizeEl.value) || 10;
        if (formatEl) options.format = formatEl.value || 'PNG';
        if (shapeEl) options.module_drawer = shapeEl.value || 'square';
        if (errorCorrectionEl) options.error_correction = errorCorrectionEl.value || 'M';
        if (foregroundEl) options.foreground_color = foregroundEl.value || '#000000';
        if (backgroundEl) options.background_color = backgroundEl.value || '#FFFFFF';
        
        return options;
    }
    
    switch (type) {
        case 'url':
            requestData.url = document.getElementById('urlInput').value || 'https://northflank.com';
            Object.assign(requestData.options, getTypeOptions('url'));
            break;
        case 'text':
            requestData.text = document.getElementById('textInput').value || 'Northflank QR API';
            Object.assign(requestData.options, getTypeOptions('text'));
            break;
        case 'email':
            requestData.email = document.getElementById('emailInput').value || 'api@northflank.com';
            requestData.subject = document.getElementById('emailSubject').value || 'API Inquiry';
            requestData.message = document.getElementById('emailMessage').value || 'Hello from Northflank!';
            // Email uses default options for now, can be enhanced
            break;
        case 'phone':
            requestData.phone = document.getElementById('phoneInput').value || '+1234567890';
            // Phone uses default options for now, can be enhanced
            break;
        case 'wifi':
            requestData.ssid = document.getElementById('wifiSSID').value || 'NorthflankWiFi';
            requestData.password = document.getElementById('wifiPassword').value || 'secure123';
            requestData.encryption = document.getElementById('wifiSecurity').value || 'WPA';
            // WiFi uses default options for now, can be enhanced
            break;
    }
    
    return requestData;
}

// Display QR code result
function displayQRResult(data) {
    const qrResult = document.getElementById('qrResult');
    const qrImageContainer = document.getElementById('qrImageContainer');
    const apiResponse = document.getElementById('apiResponse');
    
    // Store current QR data for download
    currentQRData = data;
    
    // Display QR code image
    const img = document.createElement('img');
    img.src = data.data.qr_code;
    img.className = 'img-fluid';
    img.style.maxWidth = '300px';
    img.style.maxHeight = '300px';
    
    qrImageContainer.innerHTML = '';
    qrImageContainer.appendChild(img);
    
    // Display API response (formatted)
    const formattedResponse = {
        success: data.success,
        qr_code: data.data.qr_code.substring(0, 50) + '...',
        content: data.data.content,
        format: data.data.format,
        options: data.data.options
    };
    
    apiResponse.textContent = JSON.stringify(formattedResponse, null, 2);
    
    // Show result
    qrResult.classList.remove('d-none');
    
    // Smooth scroll to result
    qrResult.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Show error message
function showError(message) {
    const qrResult = document.getElementById('qrResult');
    const qrImageContainer = document.getElementById('qrImageContainer');
    const apiResponse = document.getElementById('apiResponse');
    
    qrImageContainer.innerHTML = `
        <div class="text-center text-danger p-4">
            <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
            <h5>Error Generating QR Code</h5>
            <p>${message}</p>
        </div>
    `;
    
    const errorResponse = {
        success: false,
        error: message
    };
    
    apiResponse.textContent = JSON.stringify(errorResponse, null, 2);
    qrResult.classList.remove('d-none');
}

// Download QR code
function downloadQR() {
    if (currentQRData && currentQRData.data) {
        const format = currentQRData.data.format || 'PNG';
        const base64Data = currentQRData.data.qr_code;
        
        // Extract the actual base64 data (remove data:image/format;base64, prefix)
        const base64Content = base64Data.split(',')[1];
        
        // Convert base64 to blob
        const byteCharacters = atob(base64Content);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        
        // Determine MIME type and file extension
        let mimeType, fileExtension;
        switch (format.toLowerCase()) {
            case 'jpeg':
                mimeType = 'image/jpeg';
                fileExtension = 'jpg';
                break;
            case 'svg':
                mimeType = 'image/svg+xml';
                fileExtension = 'svg';
                break;
            case 'pdf':
                mimeType = 'application/pdf';
                fileExtension = 'pdf';
                break;
            default:
                mimeType = 'image/png';
                fileExtension = 'png';
        }
        
        const blob = new Blob([byteArray], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `qr-code-${Date.now()}.${fileExtension}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } else {
        alert('No QR code to download. Please generate a QR code first.');
    }
}

// Copy QR data to clipboard
async function copyQRData() {
    if (currentQRData) {
        try {
            await navigator.clipboard.writeText(currentQRData.data.qr_code);
            showToast('QR code data copied to clipboard!', 'success');
        } catch (error) {
            console.error('Failed to copy:', error);
            showToast('Failed to copy data', 'error');
        }
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0 position-fixed`;
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${type === 'success' ? 'check' : 'times'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove from DOM after hiding
    toast.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toast);
    });
}

// Setup form validation
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Observe elements for animations
function observeElements() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-slide-in');
            }
        });
    }, observerOptions);
    
    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });
    
    // Observe marketplace cards
    document.querySelectorAll('.marketplace-card').forEach(card => {
        observer.observe(card);
    });
    
    // Observe performance stats
    document.querySelectorAll('.performance-stat').forEach(stat => {
        observer.observe(stat);
    });
}

// Update base URL in documentation
function updateBaseUrl() {
    const baseUrlElements = document.querySelectorAll('#baseUrl, .base-url');
    const currentUrl = window.location.origin;
    
    baseUrlElements.forEach(element => {
        element.textContent = currentUrl;
    });
}

// Copy to clipboard function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Copied to clipboard!', 'success');
    }, function(error) {
        console.error('Could not copy text: ', error);
        showToast('Failed to copy', 'error');
    });
}

// Add loading states to buttons
function addButtonLoading(button, text = 'Processing...') {
    const originalText = button.innerHTML;
    button.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>${text}`;
    button.disabled = true;
    
    return function removeLoading() {
        button.innerHTML = originalText;
        button.disabled = false;
    };
}

// Performance monitoring
function trackPerformance() {
    // Track API response times
    const performanceObserver = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
            if (entry.name.includes('/api/')) {
                console.log(`API ${entry.name}: ${entry.duration.toFixed(2)}ms`);
            }
        });
    });
    
    performanceObserver.observe({ entryTypes: ['measure', 'navigation'] });
}

// Initialize performance tracking
if ('PerformanceObserver' in window) {
    trackPerformance();
}

// Update documentation URLs when page loads
document.addEventListener('DOMContentLoaded', updateBaseUrl);