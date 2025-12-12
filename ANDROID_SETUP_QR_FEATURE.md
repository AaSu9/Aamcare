# Android Setup QR Code Feature

## Feature Overview

This feature provides a QR code that links to instructions for running the Aamcare Django application on Android devices.

## Implementation Details

### 1. New Views Added

1. **`android_setup_guide(request)`** - Renders the Android setup guide page
2. **`generate_android_setup_qr(request)`** - Generates a QR code linking to Android setup instructions

### 2. New URL Patterns

1. `/android-setup-guide/` - Displays the Android setup guide page
2. `/generate-android-setup-qr/` - Generates and serves the QR code image

### 3. New Template

**`core/templates/core/android_setup_guide.html`** - Provides detailed instructions for running the app on Android with:
- Step-by-step Termux installation guide
- Package installation commands
- Server setup and running instructions
- Cloud deployment alternatives
- QR code generation button

## How It Works

1. Users can navigate to `/android-setup-guide/` to view instructions
2. The page includes a "Show Setup QR Code" button
3. When clicked, it displays a QR code that links to detailed setup instructions
4. Scanning the QR code on an Android device will open the setup guide in the browser

## Technical Implementation

### QR Code Generation
- Uses the existing `qrcode` library
- Generates a PNG image response
- Links to a GitHub wiki page with detailed instructions (placeholder URL)
- Dynamically generated on request

### Template Features
- Responsive Bootstrap design
- Clear step-by-step instructions
- Syntax-highlighted code examples
- Toggleable QR code section
- Back navigation to dashboard

## Files Created/Modified

1. **`core/views.py`** - Added two new view functions
2. **`core/urls.py`** - Added two new URL patterns
3. **`core/templates/core/android_setup_guide.html`** - New template file
4. **`TEST_ANDROID_QR.py`** - Test script (temporary)

## Verification

✅ **QR Code Generation**: Tested and working correctly
- Generates valid PNG images
- Correctly encodes the destination URL
- Proper HTTP response with correct content type

✅ **Template Integration**: 
- Page renders correctly
- QR code toggle functionality works
- Responsive design maintained

## Usage Instructions

1. Navigate to `/android-setup-guide/` in the application
2. Click "Show Setup QR Code" button
3. Scan the QR code with an Android device
4. Follow the instructions to set up Termux and run the application

## Note

The QR code currently links to a placeholder URL (`https://github.com/Aamcare/aamcare-app/wiki/Android-Setup-Guide`). This should be updated to point to the actual documentation when available.