#!/usr/bin/env python
"""
Script to test the QR code generation functionality
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aamcare.settings')
django.setup()

def test_qr_code_generation():
    """Test that the QR code generation works correctly"""
    print("=" * 50)
    print("TESTING QR CODE GENERATION")
    print("=" * 50)
    
    try:
        # Import the view function
        from core.views import generate_whatsapp_qr
        from django.http import HttpRequest
        
        # Create a mock request
        request = HttpRequest()
        
        # Generate the QR code
        response = generate_whatsapp_qr(request)
        
        # Check if we got a valid response
        if response and response.content:
            print("✅ QR code generation successful!")
            print(f"   Response content type: {response.get('Content-Type', 'Not set')}")
            print(f"   Response size: {len(response.content)} bytes")
            
            # Save the QR code to a file for visual inspection
            with open('test_whatsapp_qr.png', 'wb') as f:
                f.write(response.content)
            print("   QR code saved as 'test_whatsapp_qr.png'")
        else:
            print("❌ QR code generation failed - empty response")
            
    except Exception as e:
        print(f"❌ Error generating QR code: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("QR CODE TEST COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    test_qr_code_generation()