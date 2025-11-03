// Convert GitHub Bible-kjv format to our structure
class BibleConverter {
  constructor() {
    this.convertedBible = {};
  }

  // Convert from GitHub format to our format
  convertGitHubFormat(githubBible) {
    const converted = {};
    
    githubBible.forEach(book => {
      const bookName = book.name;
      converted[bookName] = {};
      
      book.chapters.forEach((chapter, chapterIndex) => {
        const chapterNum = chapterIndex + 1;
        converted[bookName][chapterNum] = {};
        
        chapter.forEach((verse, verseIndex) => {
          const verseNum = verseIndex + 1;
          converted[bookName][chapterNum][verseNum] = verse;
        });
      });
    });
    
    return converted;
  }

  // Download and convert the GitHub Bible
  async downloadAndConvert() {
    try {
      console.log('Downloading KJV Bible from GitHub...');
      const response = await fetch('https://raw.githubusercontent.com/aruljohn/Bible-kjv/master/bible_kjv.json');
      const githubBible = await response.json();
      
      console.log('Converting format...');
      const converted = this.convertGitHubFormat(githubBible);
      
      console.log('Conversion complete!');
      return converted;
      
    } catch (error) {
      console.error('Download failed:', error);
      return null;
    }
  }

  // Generate the final JSON file content
  generateBibleJSON(convertedBible) {
    return JSON.stringify(convertedBible, null, 2);
  }
}

// Usage instructions
console.log(`
IMPLEMENTATION STEPS:

1. Download the Bible JSON:
   - Go to: https://github.com/aruljohn/Bible-kjv
   - Download: bible_kjv.json
   - Save to: assets/data/bible_kjv_raw.json

2. Run conversion:
   const converter = new BibleConverter();
   fetch('assets/data/bible_kjv_raw.json')
     .then(r => r.json())
     .then(data => {
       const converted = converter.convertGitHubFormat(data);
       console.log(JSON.stringify(converted, null, 2));
     });

3. Save output as: assets/data/bible-kjv.json

4. Update bible-generator.js to use the full Bible
`);

// Export for use
if (typeof module !== 'undefined') {
  module.exports = BibleConverter;
}