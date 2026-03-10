# One Year Bible Website - Recurring Issues & Solutions

## Issue #1: Calendar Widget Year Discrepancy

### Problem Description
When navigating to reading pages from different years (e.g., October 8, 2025), the calendar widget on the reading page would always show the current year (2026) instead of the year corresponding to the selected reading.

### Symptoms
- Reading page content shows correct year (e.g., "October 8, 2025")
- Calendar widget header shows wrong year (e.g., "Oct 2026" instead of "Oct 2025")
- URL contains correct year parameter (`?year=2025`)
- Date calculations are correct (day of week matches)

### Root Cause
The calendar widget initialization code always defaulted to the current year (`new Date().getFullYear()`) without checking for URL parameters that indicate a different year was selected.

**Problematic Code:**
```javascript
let widgetYear = new Date().getFullYear(); // Always uses current year
```

### Solution
Modified the calendar initialization to check for year parameter in URL when on reading pages:

```javascript
let widgetYear = new Date().getFullYear(); // Use current year
let widgetMonth = currentPageDate ? currentPageDate.month : new Date().getMonth();

// If on a reading page, get year from URL parameter
if (window.location.pathname.includes('/readings/')) {
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('year')) {
    widgetYear = parseInt(urlParams.get('year'));
    console.log('Using year from URL:', widgetYear);
  }
}
```

### Files Modified
- `assets/js/calendar.js` - Lines 15-23

### Why This Was Difficult to Diagnose
1. **Multiple Components**: The issue involved coordination between URL parameters, calendar widget initialization, and date display functions
2. **Partial Functionality**: The reading content displayed correctly, making it seem like the year parameter was working
3. **Browser Caching**: Changes to JavaScript files were cached, requiring cache-busting techniques
4. **Local vs Live Testing**: CORS restrictions made local testing challenging

### Prevention for Future Years
- When transitioning to a new year (2027, 2028, etc.), ensure the calendar widget respects URL parameters
- Test navigation between different years thoroughly
- Use browser developer tools to verify URL parameters are being read correctly
- Consider adding more robust year validation and error handling

### Related Files to Update Annually
- `calendar.js` - Main calendar logic
- `index.html` - Version parameters for cache busting
- All reading pages - Calendar.js version references
- `reading-plan.json` - If creating new year's reading plan

### Testing Checklist for Year Transitions
- [ ] Navigate to previous year's dates via calendar
- [ ] Verify calendar widget shows correct year
- [ ] Check URL parameters are passed correctly
- [ ] Confirm reading content displays correct year
- [ ] Test "Go to Today's Reading" button
- [ ] Verify day-of-week calculations are accurate

---

*Document created: January 6, 2026*
*Last updated: January 6, 2026*