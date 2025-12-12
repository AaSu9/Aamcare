# Fix for Duplicate Baby Age Display in Mother Portal

## Issue Identified

The mother dashboard had duplicate display of the baby's age information:
1. In the welcome section (lines 355-369)
2. In a separate "Hero Section" (lines 389-415)

Both sections were showing the same information: "Your baby is X days old", causing visual redundancy and potential confusion for users.

## Root Cause

1. **Template Redundancy**: The `mother_dashboard.html` template contained two separate sections displaying the same baby age information.
2. **Variable Inconsistency**: One section used `{{ postpartum_info.days_since_birth }}` while another used `{{ postpartum_dates.days_since_birth }}`, though the view only passed `postpartum_dates`.

## Fix Applied

### 1. Removed Duplicate Section
Removed the redundant "Hero Section" that duplicated the baby age information already present in the welcome section.

### 2. Standardized Variable Usage
Ensured consistent use of `{{ postpartum_dates.days_since_birth }}` throughout the template.

### 3. Maintained Essential Information
Kept all essential information in the main welcome section:
- Baby's age in days
- Postpartum stage badge
- Birth date
- Large display of days old

## Files Modified

- `core/templates/core/mother_dashboard.html`: Removed duplicate "Hero Section" and standardized variable usage

## Verification

✅ **Visual Consistency**: Baby age information now appears only once in the dashboard
✅ **Functional Integrity**: All baby age information still displays correctly
✅ **Variable Consistency**: Using the correct `postpartum_dates` variable passed from the view
✅ **User Experience**: Cleaner, less cluttered dashboard without redundant information

## Result

The mother portal now displays the baby's age information cleanly and without duplication, improving the user experience while maintaining all essential information. Users will see:
- One clear display of "Your baby is X days old"
- Consistent information throughout the dashboard
- Clean, uncluttered interface