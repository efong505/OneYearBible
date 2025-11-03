## Adding Other Months
To add other months, you only need to:

- Create the month folder (e.g., readings/january/, readings/february/)

- Add date codes to the availableReadings arrays in both:

main-script.js (line 14)

widget-script.js (line 77 and line 171)

That's it! The scripts automatically handle all month names and navigation.

# File Structure
OneYearBible/
├── index.html (main intro page)
├── calendar.html (current calendar)
├── coming-soon.html (temporary page)
├── css/
│   ├── style.css
│   └── widget-style.css
├── js/
│   ├── script.js
│   └── widget-script.js
├── readings/
│   ├── january/
│   │   ├── 0101.html
│   │   ├── 0102.html
│   │   └── ...
│   ├── february/
│   │   ├── 0201.html
│   │   └── ...
│   ├── september/
│   │   ├── 0922.html
│   │   └── ...
│   └── december/
│       └── 1231.html
└── assets/
    ├── images/
    └── audio/
