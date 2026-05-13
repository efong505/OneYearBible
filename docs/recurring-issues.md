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

## Issue #2: Day-of-Week Misalignment on Year Change

### Problem Description
The `reading-plan.json` file contains hardcoded `dayOfWeek` values that were set for 2025. When the year changes, the day of the week for each date shifts (e.g., January 1 is Wednesday in 2025 but Thursday in 2026). The reading page headings display the day of the week (e.g., "March 7--Friday"), which would be incorrect if not updated.

### Why the Year Change Broke the Dates
Calendar dates shift by 1 day each year (or 2 after a leap year). The `dayOfWeek` values in `reading-plan.json` were originally written for 2025. When 2026 started:
- January 1, 2025 = Wednesday
- January 1, 2026 = Thursday
- Every date's day-of-week was off by one

The reading pages themselves were NOT broken visually because `calendar.js` dynamically recalculates the day of week using `new Date(displayYear, month, day)` in the `updateDynamicDates()` function. The page heading and card header date are computed at runtime from the current year, so they always display correctly regardless of what's in the JSON.

### What `reading-plan.json` dayOfWeek Is Actually Used For
Currently, the `dayOfWeek` field in the JSON is **metadata only** — it is not rendered on reading pages. The pages calculate the day dynamically. However, keeping it accurate is good practice in case:
- Future features reference it (e.g., filtering by day)
- Debugging or generating static content
- External tools consume the JSON

### How the Year Display Works (No Action Needed)
The year shown on reading pages (e.g., "May 12, 2026") is handled by `updateDynamicDates()` in `calendar.js`:
```javascript
const displayYear = urlParams.get('year') ? parseInt(urlParams.get('year')) : new Date().getFullYear();
```
- If accessed directly (no URL parameter): shows current year ✓
- If accessed via calendar navigation with `?year=2025`: shows 2025 ✓

This requires **no manual update** — it works automatically every year.

### Solution: Annual Update Script
Created `update-reading-plan-year.py` to update the `dayOfWeek` values in `reading-plan.json` for any given year.

**Usage:**
```bash
python update-reading-plan-year.py          # Updates to current year
python update-reading-plan-year.py 2027     # Updates to a specific year
```

**What the script does:**
1. Reads `assets/data/reading-plan.json`
2. For each date entry, calculates the correct day of the week for the given year
3. Updates the `dayOfWeek` field
4. Writes the updated JSON back to the file

### Files Involved
- `assets/data/reading-plan.json` — contains the `dayOfWeek` metadata
- `assets/js/calendar.js` — `updateDynamicDates()` dynamically sets year and day on pages
- `update-reading-plan-year.py` — script to update JSON for a new year

### Annual Maintenance Checklist
Run these steps at the start of each new year (e.g., January 1):

1. **Backup the reading plan:**
   ```bash
   copy assets\data\reading-plan.json assets\data\reading-plan-backup.json
   ```

2. **Run the update script:**
   ```bash
   python update-reading-plan-year.py
   ```

3. **Verify a few dates are correct:**
   - Check that Jan 1 shows the right day for the new year
   - Spot-check a few other dates

4. **Upload to S3:**
   ```bash
   aws s3 cp assets/data/reading-plan.json s3://one-year-bible-ekewaka/assets/data/reading-plan.json --profile ekewaka
   ```

5. **Push to git:**
   ```bash
   git add assets/data/reading-plan.json
   git commit -m "Update reading plan dayOfWeek for [YEAR]"
   git push
   ```

6. **Test the live site:**
   - [ ] Open a reading page and confirm the correct year displays
   - [ ] Confirm the day-of-week heading is accurate
   - [ ] Navigate between dates using the calendar widget
   - [ ] Test "Go to Today's Reading" button

### Reverting If Something Breaks
If the update causes issues, restore from backup:
```bash
copy assets\data\reading-plan-backup.json assets\data\reading-plan.json
```
Then re-upload to S3.

### Summary
| Component | Needs Annual Update? | How |
|-----------|---------------------|-----|
| Year on reading pages | No | Automatic via `new Date().getFullYear()` |
| Day-of-week on reading pages | No | Automatic via `updateDynamicDates()` |
| `dayOfWeek` in reading-plan.json | Yes (optional) | Run `update-reading-plan-year.py` |
| Audio files / readings content | No | Same plan every year |

---

*Document created: January 6, 2026*
*Last updated: June 14, 2026*