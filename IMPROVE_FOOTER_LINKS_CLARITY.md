# Improve Footer Links Clarity

## Issue Identified

The footer support links had overlapping and unclear purposes:
- "Danger Signs" and "Emergency Contacts" were too similar
- "Emergency Contacts" link pointed to the same page as "Danger Signs" with just an anchor
- This created confusion for users trying to find specific information

## Root Cause

The footer links were not clearly differentiated in purpose:
- Both "Danger Signs" and "Emergency Contacts" pointed to the same general area
- Users couldn't easily distinguish between the two options
- The navigation structure was redundant

## Fix Applied

### 1. Clarified Link Purposes
Replaced confusing "Emergency Contacts" with "Find Health Workers" which:
- Points to the Community Workers page (`/community-workers/`)
- Contains actual contact information for health workers
- Provides a clearer distinction from "Danger Signs"

### 2. Improved Navigation Structure
Now the footer links have distinct, clear purposes:
- **Danger Signs** → Information about recognizing dangerous symptoms
- **Vaccination Guide** → Information about vaccination schedules
- **Find Health Workers** → Contact information for community health workers
- **FAQs** → Answers to common questions

## Files Modified

1. **`core/templates/core/base.html`** - Updated footer support links for clarity

## Verification

✅ **Link Distinction**: Each footer link now has a clearly different purpose
✅ **Logical Navigation**: Links point to appropriate, relevant content
✅ **User Experience**: Reduced confusion with clearer labeling
✅ **Content Accuracy**: "Find Health Workers" correctly points to the community workers page

## Result

The footer support links are now clearer and more intuitive:
- Users can easily distinguish between different support options
- Each link leads to distinctly different content
- Navigation is more logical and user-friendly
- Eliminates redundancy between "Danger Signs" and "Emergency Contacts"

Users will now have a better experience finding the specific support information they need.