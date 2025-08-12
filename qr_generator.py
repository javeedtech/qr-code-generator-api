import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import os

# Try to import advanced styling features, fallback to basic if not available
try:
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, SquareModuleDrawer
    ADVANCED_STYLING = True
except ImportError:
    ADVANCED_STYLING = False

class QRCodeGenerator:
    def __init__(self):
        self.default_options = {
            'size': 10,
            'border': 4,
            'error_correction': 'M',
            'format': 'PNG',
            'foreground_color': '#000000',
            'background_color': '#FFFFFF',
            'module_drawer': 'square',
            'logo_path': None,
            'logo_size_ratio': 0.3
        }
    
    def _get_error_correction_level(self, level):
        """Convert string error correction level to qrcode constant"""
        levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,  # ~7%
            'M': qrcode.constants.ERROR_CORRECT_M,  # ~15%
            'Q': qrcode.constants.ERROR_CORRECT_Q,  # ~25%
            'H': qrcode.constants.ERROR_CORRECT_H   # ~30%
        }
        return levels.get(level.upper(), qrcode.constants.ERROR_CORRECT_M)
    
    def _get_module_drawer(self, drawer_type):
        """Get module drawer based on type"""
        if not ADVANCED_STYLING:
            return None
        
        drawers = {
            'square': SquareModuleDrawer(),
            'rounded': RoundedModuleDrawer(), 
            'circle': CircleModuleDrawer()
        }
        return drawers.get(drawer_type.lower(), SquareModuleDrawer())
    
    def _create_qr_code(self, data, options):
        """Create base QR code with given data and options"""
        merged_options = {**self.default_options, **options}
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=self._get_error_correction_level(merged_options['error_correction']),
            box_size=merged_options['size'],
            border=merged_options['border'],
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        # Try advanced styling first, fallback to basic if colors don't work
        if ADVANCED_STYLING and merged_options['module_drawer'] != 'square':
            try:
                module_drawer = self._get_module_drawer(merged_options['module_drawer'])
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=module_drawer,
                    fill_color=merged_options['foreground_color'],
                    back_color=merged_options['background_color']
                )
            except Exception as e:
                logging.warning(f"Advanced styling failed, falling back to basic: {e}")
                img = qr.make_image(
                    fill_color=merged_options['foreground_color'],
                    back_color=merged_options['background_color']
                )
        else:
            # Basic image generation
            img = qr.make_image(
                fill_color=merged_options['foreground_color'],
                back_color=merged_options['background_color']
            )
        
        # Add logo if specified
        if merged_options.get('logo_path') and os.path.exists(merged_options['logo_path']):
            img = self._add_logo(img, merged_options['logo_path'], merged_options['logo_size_ratio'])
        
        return img, merged_options
    
    def _add_logo(self, qr_img, logo_path, size_ratio):
        """Add logo to center of QR code"""
        try:
            logo = Image.open(logo_path)
            
            # Calculate logo size
            qr_width, qr_height = qr_img.size
            logo_size = int(min(qr_width, qr_height) * size_ratio)
            
            # Resize logo
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Create a white background for logo
            logo_bg = Image.new('RGB', (logo_size + 20, logo_size + 20), 'white')
            logo_bg.paste(logo, (10, 10))
            
            # Calculate position to center logo
            pos = ((qr_width - logo_size - 20) // 2, (qr_height - logo_size - 20) // 2)
            qr_img.paste(logo_bg, pos)
            
        except Exception as e:
            logging.warning(f"Failed to add logo: {e}")
        
        return qr_img
    
    def _image_to_base64(self, img, format_type='PNG'):
        """Convert PIL image to base64 string"""
        buffer = io.BytesIO()
        
        if format_type.upper() == 'PNG':
            img.save(buffer, format='PNG', optimize=True)
            mime_type = 'image/png'
        elif format_type.upper() == 'JPEG':
            # Convert to RGB for JPEG (no transparency)
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, 'white')
                background.paste(img, mask=img.split()[-1])
                img = background
            img.save(buffer, format='JPEG', optimize=True, quality=85)
            mime_type = 'image/jpeg'
        elif format_type.upper() == 'SVG':
            # Generate SVG format
            return self._create_svg_qr(img)
        else:
            img.save(buffer, format='PNG', optimize=True)
            mime_type = 'image/png'
        
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode()
        return f"data:{mime_type};base64,{img_str}"
    
    def _create_svg_qr(self, img):
        """Create SVG version of QR code"""
        try:
            width, height = img.size
            
            # Convert image to black/white pixels
            img_bw = img.convert('1')  # Convert to 1-bit (black/white)
            pixels = list(img_bw.getdata())
            
            # Create optimized SVG with larger modules for better performance
            module_size = max(1, width // 50)  # Adjust based on QR size
            svg_width = width
            svg_height = height
            
            # Create SVG with proper scaling
            svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
<rect width="{width}" height="{height}" fill="white"/>'''
            
            # Group adjacent black pixels into larger rectangles for efficiency
            for y in range(0, height, module_size):
                for x in range(0, width, module_size):
                    # Check if this module should be black
                    pixel_idx = min(y * width + x, len(pixels) - 1)
                    if pixels[pixel_idx] == 0:  # Black pixel
                        rect_width = min(module_size, width - x)
                        rect_height = min(module_size, height - y)
                        svg_content += f'<rect x="{x}" y="{y}" width="{rect_width}" height="{rect_height}" fill="black"/>'
            
            svg_content += '</svg>'
            
            # Encode SVG as base64
            import base64
            svg_b64 = base64.b64encode(svg_content.encode('utf-8')).decode()
            return f"data:image/svg+xml;base64,{svg_b64}"
            
        except Exception as e:
            logging.warning(f"SVG generation failed, falling back to PNG: {e}")
            # Fallback to PNG
            return self._image_to_base64(img, 'PNG')
    
    def _create_pdf(self, img, content):
        """Create PDF with QR code"""
        try:
            # Save image to temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img:
                img.save(temp_img.name, 'PNG')
                temp_img_path = temp_img.name
            
            # Create PDF
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
                c = canvas.Canvas(temp_pdf.name, pagesize=letter)
                
                # Add title
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, 750, "QR Code")
                
                # Add QR code image
                c.drawImage(temp_img_path, 50, 500, width=200, height=200)
                
                # Add content description
                c.setFont("Helvetica", 12)
                c.drawString(50, 480, f"Content: {content[:50]}...")
                
                c.save()
                temp_pdf_path = temp_pdf.name
            
            # Read PDF and convert to base64
            with open(temp_pdf_path, 'rb') as pdf_file:
                pdf_data = base64.b64encode(pdf_file.read()).decode()
            
            # Cleanup
            os.unlink(temp_img_path)
            os.unlink(temp_pdf_path)
            
            return f"data:application/pdf;base64,{pdf_data}"
            
        except Exception as e:
            logging.error(f"PDF generation failed: {e}")
            # Fallback to PNG
            return self._image_to_base64(img, 'PNG')
    
    def generate_url_qr(self, url, options=None):
        """Generate QR code for URL"""
        if options is None:
            options = {}
        
        try:
            img, final_options = self._create_qr_code(url, options)
            
            if final_options['format'].upper() == 'PDF':
                qr_data = self._create_pdf(img, url)
            else:
                qr_data = self._image_to_base64(img, final_options['format'])
            
            return {
                'success': True,
                'data': {
                    'qr_code': qr_data,
                    'content': url,
                    'format': final_options['format'].upper(),
                    'options': final_options
                }
            }
        except Exception as e:
            logging.error(f"Error generating URL QR code: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_text_qr(self, text, options=None):
        """Generate QR code for plain text"""
        if options is None:
            options = {}
        
        try:
            img, final_options = self._create_qr_code(text, options)
            
            if final_options['format'].upper() == 'PDF':
                qr_data = self._create_pdf(img, text)
            else:
                qr_data = self._image_to_base64(img, final_options['format'])
            
            return {
                'success': True,
                'data': {
                    'qr_code': qr_data,
                    'content': text,
                    'format': final_options['format'].upper(),
                    'options': final_options
                }
            }
        except Exception as e:
            logging.error(f"Error generating text QR code: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_email_qr(self, email, subject='', message='', options=None):
        """Generate QR code for email"""
        if options is None:
            options = {}
        
        # Create mailto link
        mailto_data = f"mailto:{email}"
        params = []
        if subject:
            params.append(f"subject={subject}")
        if message:
            params.append(f"body={message}")
        
        if params:
            mailto_data += "?" + "&".join(params)
        
        try:
            img, final_options = self._create_qr_code(mailto_data, options)
            
            if final_options['format'].upper() == 'PDF':
                qr_data = self._create_pdf(img, mailto_data)
            else:
                qr_data = self._image_to_base64(img, final_options['format'])
            
            return {
                'success': True,
                'data': {
                    'qr_code': qr_data,
                    'content': mailto_data,
                    'format': final_options['format'].upper(),
                    'options': final_options
                }
            }
        except Exception as e:
            logging.error(f"Error generating email QR code: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_phone_qr(self, phone, options=None):
        """Generate QR code for phone number"""
        if options is None:
            options = {}
        
        phone_data = f"tel:{phone}"
        
        try:
            img, final_options = self._create_qr_code(phone_data, options)
            
            if final_options['format'].upper() == 'PDF':
                qr_data = self._create_pdf(img, phone_data)
            else:
                qr_data = self._image_to_base64(img, final_options['format'])
            
            return {
                'success': True,
                'data': {
                    'qr_code': qr_data,
                    'content': phone_data,
                    'format': final_options['format'].upper(),
                    'options': final_options
                }
            }
        except Exception as e:
            logging.error(f"Error generating phone QR code: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_sms_qr(self, phone, message='', options=None):
        """Generate QR code for SMS"""
        if options is None:
            options = {}
        
        sms_data = f"sms:{phone}"
        if message:
            sms_data += f"?body={message}"
        
        try:
            img, final_options = self._create_qr_code(sms_data, options)
            
            if final_options['format'].upper() == 'PDF':
                qr_data = self._create_pdf(img, sms_data)
            else:
                qr_data = self._image_to_base64(img, final_options['format'])
            
            return {
                'success': True,
                'data': {
                    'qr_code': qr_data,
                    'content': sms_data,
                    'format': final_options['format'].upper(),
                    'options': final_options
                }
            }
        except Exception as e:
            logging.error(f"Error generating SMS QR code: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_vcard_qr(self, vcard_data, options=None):
        """Generate QR code for vCard contact"""
        if options is None:
            options = {}
        
        # Create vCard format
        vcard = "BEGIN:VCARD\nVERSION:3.0\n"
        
        if vcard_data.get('first_name') or vcard_data.get('last_name'):
            vcard += f"FN:{vcard_data.get('first_name', '')} {vcard_data.get('last_name', '')}\n"
            vcard += f"N:{vcard_data.get('last_name', '')};{vcard_data.get('first_name', '')}\n"
        
        if vcard_data.get('organization'):
            vcard += f"ORG:{vcard_data['organization']}\n"
        
        if vcard_data.get('phone_work'):
            vcard += f"TEL;TYPE=WORK:{vcard_data['phone_work']}\n"
        
        if vcard_data.get('phone_mobile'):
            vcard += f"TEL;TYPE=CELL:{vcard_data['phone_mobile']}\n"
        
        if vcard_data.get('email'):
            vcard += f"EMAIL:{vcard_data['email']}\n"
        
        if vcard_data.get('website'):
            vcard += f"URL:{vcard_data['website']}\n"
        
        # Address
        address_parts = [
            vcard_data.get('street', ''),
            vcard_data.get('city', ''),
            vcard_data.get('state', ''),
            vcard_data.get('zipcode', ''),
            vcard_data.get('country', '')
        ]
        
        if any(address_parts):
            address = ';'.join(address_parts)
            vcard += f"ADR:;;{address}\n"
        
        vcard += "END:VCARD"
        
        try:
            img, final_options = self._create_qr_code(vcard, options)
            
            if final_options['format'].upper() == 'PDF':
                qr_data = self._create_pdf(img, "vCard Contact")
            else:
                qr_data = self._image_to_base64(img, final_options['format'])
            
            return {
                'success': True,
                'data': {
                    'qr_code': qr_data,
                    'content': vcard,
                    'format': final_options['format'].upper(),
                    'options': final_options
                }
            }
        except Exception as e:
            logging.error(f"Error generating vCard QR code: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_wifi_qr(self, ssid, password='', encryption='WPA', options=None):
        """Generate QR code for WiFi connection"""
        if options is None:
            options = {}
        
        # Create WiFi format
        if encryption.upper() == 'NOPASS':
            wifi_data = f"WIFI:T:nopass;S:{ssid};;"
        else:
            wifi_data = f"WIFI:T:{encryption.upper()};S:{ssid};P:{password};;"
        
        try:
            img, final_options = self._create_qr_code(wifi_data, options)
            
            if final_options['format'].upper() == 'PDF':
                qr_data = self._create_pdf(img, f"WiFi: {ssid}")
            else:
                qr_data = self._image_to_base64(img, final_options['format'])
            
            return {
                'success': True,
                'data': {
                    'qr_code': qr_data,
                    'content': wifi_data,
                    'format': final_options['format'].upper(),
                    'options': final_options
                }
            }
        except Exception as e:
            logging.error(f"Error generating WiFi QR code: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_location_qr(self, latitude, longitude, options=None):
        """Generate QR code for location coordinates"""
        if options is None:
            options = {}
        
        # Create geo location format
        geo_data = f"geo:{latitude},{longitude}"
        
        try:
            img, final_options = self._create_qr_code(geo_data, options)
            
            if final_options['format'].upper() == 'PDF':
                qr_data = self._create_pdf(img, geo_data)
            else:
                qr_data = self._image_to_base64(img, final_options['format'])
            
            return {
                'success': True,
                'data': {
                    'qr_code': qr_data,
                    'content': geo_data,
                    'format': final_options['format'].upper(),
                    'options': final_options
                }
            }
        except Exception as e:
            logging.error(f"Error generating location QR code: {e}")
            return {'success': False, 'error': str(e)}