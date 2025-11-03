// Multi-Version Bible Fetcher for NASB, NKJV, KJV
class MultiVersionBibleFetcher {
  constructor() {
    this.versions = {
      'KJV': 'King James Version',
      'NASB': 'New American Standard Bible',
      'NKJV': 'New King James Version',
      'ESV': 'English Standard Version',
      'NIV': 'New International Version'
    };
  }

  // API Sources for different versions
  getAPISources() {
    return {
      // Free APIs (no auth required)
      'bible-api.com': {
        url: 'https://bible-api.com',
        versions: ['KJV'],
        format: 'json',
        notes: 'Free, KJV only'
      },
      
      // Requires free API key
      'api.esv.org': {
        url: 'https://api.esv.org/v3',
        versions: ['ESV'],
        format: 'json',
        notes: 'Free tier: 5000 requests/day'
      },
      
      // Requires API key
      'api.scripture.api.bible': {
        url: 'https://api.scripture.api.bible/v1',
        versions: ['KJV', 'NASB', 'ESV', 'NIV'],
        format: 'json',
        notes: 'Free tier: 1000 requests/day'
      },
      
      // GitHub repositories (direct download)
      'github-repos': {
        'KJV': 'https://raw.githubusercontent.com/aruljohn/Bible-kjv/master/Gideons.json',
        'NASB': 'https://raw.githubusercontent.com/seven1m/bible_api/master/bibles/nasb.json',
        'NKJV': 'Limited availability due to copyright',
        'ESV': 'https://raw.githubusercontent.com/seven1m/bible_api/master/bibles/esv.json'
      }
    };
  }

  // Download commands for each version
  getDownloadCommands() {
    return `
# Download Bible versions to your project:

# KJV (Public Domain - Free)
curl -o assets/data/bible-kjv.json https://raw.githubusercontent.com/aruljohn/Bible-kjv/master/Gideons.json

# NASB (Copyright protected - Limited availability)
curl -o assets/data/bible-nasb.json https://raw.githubusercontent.com/seven1m/bible_api/master/bibles/nasb.json

# ESV (Requires API key for full access)
curl -o assets/data/bible-esv.json https://raw.githubusercontent.com/seven1m/bible_api/master/bibles/esv.json

# NKJV (Copyright protected - Not freely available)
# Contact Thomas Nelson Publishers for licensing

# Alternative: Use Bible Gateway API (requires key)
# https://www.biblegateway.com/api/
`;
  }

  // Copyright status for each version
  getCopyrightInfo() {
    return {
      'KJV': {
        status: 'Public Domain',
        availability: 'Freely available',
        download: 'Yes - multiple sources'
      },
      'NASB': {
        status: 'Copyright © The Lockman Foundation',
        availability: 'Limited free use',
        download: 'Some sources available'
      },
      'NKJV': {
        status: 'Copyright © Thomas Nelson',
        availability: 'Restricted',
        download: 'Requires licensing'
      },
      'ESV': {
        status: 'Copyright © Crossway',
        availability: 'API available with key',
        download: 'Limited free tier'
      },
      'NIV': {
        status: 'Copyright © Biblica',
        availability: 'API available with key',
        download: 'Requires licensing'
      }
    };
  }

  // Recommended approach for your project
  getRecommendation() {
    return `
RECOMMENDED APPROACH:

1. PRIMARY: Use KJV (Public Domain)
   - Freely available, no copyright issues
   - Matches your current content
   - curl -o assets/data/bible-kjv.json https://raw.githubusercontent.com/aruljohn/Bible-kjv/master/Gideons.json

2. SECONDARY: Add version selector
   - Let users choose their preferred translation
   - Load different JSON files based on selection
   - Start with KJV, add others as available

3. FUTURE: Bible Gateway API
   - Sign up for free API key
   - Access multiple versions legally
   - 500 requests/day free tier
   - https://www.biblegateway.com/api/

4. STRUCTURE:
   assets/data/
   ├── bible-kjv.json (free)
   ├── bible-esv.json (API key)
   └── bible-nasb.json (limited)
`;
  }
}

// Usage
const fetcher = new MultiVersionBibleFetcher();
console.log('API Sources:', fetcher.getAPISources());
console.log('Download Commands:', fetcher.getDownloadCommands());
console.log('Copyright Info:', fetcher.getCopyrightInfo());
console.log('Recommendation:', fetcher.getRecommendation());