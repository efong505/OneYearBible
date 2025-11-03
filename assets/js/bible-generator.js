// Bible Reading Page Generator
class BibleGenerator {
  constructor(version = 'kjv') {
    this.version = version;
    this.readingPlan = null;
    this.bibleText = null;
  }

  async loadData(basePath = '../../assets/data/') {
    const bibleFile = this.version === 'nkjv' ? 'bible-nkjv.json' : 'bible-kjv.json';
    const [planResponse, bibleResponse] = await Promise.all([
      fetch(`${basePath}reading-plan.json`),
      fetch(`${basePath}${bibleFile}`)
    ]);
    this.readingPlan = await planResponse.json();
    this.bibleText = await bibleResponse.json();
  }

  generatePage(dateCode) {
    const reading = this.readingPlan[dateCode];
    if (!reading) return null;

    return `<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Kenneth Copeland One Year Bible Reading</title>
    <link rel="icon" href="../../assets/images/bible-w-cross.png" type="image/png">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
    <link rel="stylesheet" href="../../assets/css/calendar.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap">
    <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200">
    <link rel="stylesheet" href="../../assets/css/reading.css">
</head>

<body>
    <div class="container mt-5">

        <!-- Intro Section -->
        <img src="../../assets/images/KCMCenterlineWebUse4ColorBlackText.png" alt="image" class="img-fluid mx-auto d-block">
        <h1 class="text-center mt-3">One-Year Bible</h1>
        <p class="mt-3 mb-5 text-center">
            This site an unofficial site of Kenneth Copeland Ministries is for personal use only. Although the authors
            support and endorse
            the views of this ministry, <br>it is not affilaited nor directly endorsed by Kenneth Copeland Ministries in
            any way.
            This page follows the ONE-YEAR Bible guide found here at:<br>
            <a href="https://www.kcm.org/read/one-year-bible" target="_blank"
                rel="noopener noreferrer">https://www.kcm.org/read/one-year-bible</a>

        </p><!-- Intro section End -->

        <!-- Calendar Widget -->
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="calendar-widget-inline">
                    <div class="widget-header">
                        <span class="widget-current-date"></span>
                        <div class="widget-navigation">
                            <span id="widget-prev" class="material-symbols-rounded">chevron_left</span>
                            <span id="widget-next" class="material-symbols-rounded">chevron_right</span>
                        </div>
                    </div>
                    <div class="widget-body">
                        <ul class="widget-weekdays">
                            <li>S</li>
                            <li>M</li>
                            <li>T</li>
                            <li>W</li>
                            <li>T</li>
                            <li>F</li>
                            <li>S</li>
                        </ul>
                        <ul class="widget-dates"></ul>
                    </div>
                </div>
            </div>
            <div class="col-md-8">
                <!-- Content will flow here -->
            </div>
        </div>
        
        <!-- Navigation -->
        <div class="mb-3 ms-2">
            <a href="../../index.html"><- Back to Main Page</a>
        </div>

        <!-- Reading Beginning -->
        <h2>${reading.date}--${reading.dayOfWeek}</h2>
        <h4 class="mt-3">${reading.oldTestament} & ${reading.newTestament}</h4>
        <div class="card mt-4">
            <div class="card-header">${reading.date}, 2025</div>
            <div class="card-body">
                <audio controls class="w-100">
                    <source src="https://d24muyyuu3zj8g.cloudfront.net/2025/september/4/${reading.audio}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
        </div>

        <!-- Drop Down Collapse  -->
        <!-- button container -->
        <p class="mt-3 d-inline-flex gap-1">
            <button class="btn btn-primary" type="button" data-bs-toggle="collapse"
                data-bs-target="#showScripturesCollapse${dateCode}" aria-expanded="false"
                aria-controls="showScripturesCollapse${dateCode}">
                Show Scriptures
            </button>
        </p> <!-- button containter end -->

        <!-- Dropdown Container -->
        <div class="collapse" id="showScripturesCollapse${dateCode}">
            <div class="card card-body">

                <!-- tabs -->
                <div class="container my-2">
                    <ul class="nav nav-tabs" id="myTab${dateCode}" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active" id="old-tab${dateCode}" data-bs-toggle="tab"
                                data-bs-target="#old${dateCode}" type="button" role="tab" aria-controls="old${dateCode}"
                                aria-selected="true">Old Testament</button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="new-tab${dateCode}" data-bs-toggle="tab" data-bs-target="#new${dateCode}"
                                type="button" role="tab" aria-controls="new${dateCode}" aria-selected="false">New
                                Testament/Psalms</button>
                        </li>

                    </ul>

                    <div class="tab-content mt-3" id="myTabContent${dateCode}">
                        <div class="tab-pane fade show active" id="old${dateCode}" role="tabpanel"
                            aria-labelledby="old-tab${dateCode}">
                            <h2>${reading.oldTestament}</h2>
                            ${this.parseAndGenerateScripture(reading.oldTestament)}
                        </div>
                        <div class="tab-pane fade" id="new${dateCode}" role="tabpanel" aria-labelledby="new-tab${dateCode}">
                            <h2>${reading.newTestament}</h2>
                            ${this.parseAndGenerateScripture(reading.newTestament)}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Navigation -->
        <nav class="mt-5 mb-5" aria-label="...">
            <ul class="pagination justify-content-center">
                <li class="page-item">
                    <a class="page-link" href="#" id="prev-day">← Previous Day</a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="#" id="next-day">Next Day →</a>
                </li>
            </ul>
        </nav>
    </div>

    <script src="../../assets/js/calendar.js"></script>
    <script src="../../assets/js/navigation.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
        crossorigin="anonymous"></script>
</body>

</html>`;
  }

  parseAndGenerateScripture(reference) {
    if (!reference || reference.trim() === '') return '';
    
    // Parse "Isa. 1:1 - 2:22" or "1 Tim. 1" or "Isa. 26-28"
    const parts = reference.split(' - ');
    if (parts.length === 1) {
      return this.generateSingleReference(parts[0]);
    } else {
      return this.generateRangeReference(parts[0], parts[1]);
    }
  }

  expandBookName(abbrev) {
    const bookMap = {
      'Gen.': 'Genesis', 'Ex.': 'Exodus', 'Lev.': 'Leviticus', 'Num.': 'Numbers', 'Deut.': 'Deuteronomy',
      'Josh.': 'Joshua', 'Jdgs.': 'Judges', 'Ruth': 'Ruth', '1 Sam.': '1 Samuel', '2 Sam.': '2 Samuel',
      '1 Kgs.': '1 Kings', '2 Kgs.': '2 Kings', '1 Chr.': '1 Chronicles', '2 Chr.': '2 Chronicles',
      'Ezra': 'Ezra', 'Ez.': 'Ezra', 'Neh.': 'Nehemiah', 'Est.': 'Esther', 'Job': 'Job', 'Ps.': 'Psalms', 'Prov.': 'Proverbs',
      'Eccl.': 'Ecclesiastes', 'Songs': 'Song of Solomon', 'Isa.': 'Isaiah', 'Jer.': 'Jeremiah', 'Lam.': 'Lamentations',
      'Ezek.': 'Ezekiel', 'Dan.': 'Daniel', 'Hos.': 'Hosea', 'Joel': 'Joel', 'Amos': 'Amos', 'Obad.': 'Obadiah',
      'Jon.': 'Jonah', 'Mic.': 'Micah', 'Nah.': 'Nahum', 'Hab.': 'Habakkuk', 'Zeph.': 'Zephaniah', 'Hag.': 'Haggai',
      'Zech.': 'Zechariah', 'Mal.': 'Malachi', 'Matt.': 'Matthew', 'Mark': 'Mark', 'Luke': 'Luke', 'John': 'John',
      'Acts': 'Acts', 'Rom.': 'Romans', '1 Cor.': '1 Corinthians', '2 Cor.': '2 Corinthians', 'Gal.': 'Galatians',
      'Eph.': 'Ephesians', 'Phil.': 'Philippians', 'Col.': 'Colossians', '1 Thess.': '1 Thessalonians', '2 Thess.': '2 Thessalonians',
      '1 Tim.': '1 Timothy', '2 Tim.': '2 Timothy', 'Titus': 'Titus', 'Philem.': 'Philemon', 'Heb.': 'Hebrews',
      'Jas.': 'James', '1 Pet.': '1 Peter', '2 Pet.': '2 Peter', '1 Jn.': '1 John', '2 Jn.': '2 John', '3 Jn.': '3 John',
      'Jude': 'Jude', 'Rev.': 'Revelation'
    };
    return bookMap[abbrev] || abbrev;
  }

  generateSingleReference(ref) {
    // Handle complex cross-book patterns like "2 Chr. 35:10-Ez. 1:11"
    const crossBookMatch = ref.match(/^(.+?)\s+(\d+):(\d+)-\s*(.+?)\s+(\d+):(\d+)$/);
    if (crossBookMatch) {
      const [, book1, ch1, v1, book2, ch2, v2] = crossBookMatch;
      let html = this.generatePartialChapter(book1, ch1, v1, '999');
      html += this.generatePartialChapter(book2, ch2, '1', v2);
      return html;
    }
    
    // Handle verse ranges within same book like "Jer. 1:1-3:5"
    const verseRangeMatch = ref.match(/^(.+?)\s+(\d+):(\d+)-(\d+):(\d+)$/);
    if (verseRangeMatch) {
      const [, bookAbbrev, startCh, startV, endCh, endV] = verseRangeMatch;
      return this.generateVerseRange(bookAbbrev, startCh, startV, endCh, endV);
    }
    
    // Handle single verse ranges like "Jer. 1:1-15" (same chapter)
    const singleChapterVerseRange = ref.match(/^(.+?)\s+(\d+):(\d+)-(\d+)$/);
    if (singleChapterVerseRange) {
      const [, bookAbbrev, chapter, startV, endV] = singleChapterVerseRange;
      return this.generatePartialChapter(bookAbbrev, chapter, startV, endV);
    }
    
    // Handle chapter ranges like "Isa. 26-28"
    const chapterRangeMatch = ref.match(/^(.+?)\s+(\d+)-(\d+)$/);
    if (chapterRangeMatch) {
      const [, bookAbbrev, startCh, endCh] = chapterRangeMatch;
      return this.generateChapterRange(bookAbbrev, startCh, endCh);
    }
    
    // Handle single chapter like "1 Tim. 1"
    const singleMatch = ref.match(/^(.+?)\s+(\d+)$/);
    if (singleMatch) {
      const [, bookAbbrev, chapter] = singleMatch;
      return this.generateSingleChapter(bookAbbrev, chapter);
    }
    
    return '';
  }
  
  generatePartialChapter(bookAbbrev, chapter, startVerse, endVerse) {
    const bookName = this.expandBookName(bookAbbrev);
    const book = this.bibleText[bookName];
    if (!book || !book[chapter]) return '';
    
    let html = `<h5>${bookName} ${chapter}:${startVerse}${endVerse !== '999' ? '-' + endVerse : '+'}</h5>`;
    const chapterData = book[chapter];
    const maxVerse = Math.max(...Object.keys(chapterData).map(Number));
    const actualEndVerse = endVerse === '999' ? maxVerse : parseInt(endVerse);
    
    for (let v = parseInt(startVerse); v <= actualEndVerse; v++) {
      if (chapterData[v]) {
        html += `<p class="fnb"><span>${v}</span> ${chapterData[v]}</p>`;
      }
    }
    return html;
  }

  generateRangeReference(startRef, endRef) {
    // Handle "Isa. 1:1 - 2:22"
    const startMatch = startRef.match(/^(.+?)\s+(\d+):(\d+)$/);
    const endMatch = endRef.match(/^(\d+):(\d+)$/);
    if (startMatch && endMatch) {
      const [, bookAbbrev, startCh, startV] = startMatch;
      const [, endCh, endV] = endMatch;
      return this.generateVerseRange(bookAbbrev, startCh, startV, endCh, endV);
    }
    return '';
  }

  generateSingleChapter(bookAbbrev, chapter) {
    const bookName = this.expandBookName(bookAbbrev);
    const book = this.bibleText[bookName];
    if (!book || !book[chapter]) return '';
    
    let html = `<h5>${bookName} ${chapter}</h5>`;
    Object.entries(book[chapter]).forEach(([verse, text]) => {
      html += `<p class="fnb"><span>${verse}</span> ${text}</p>`;
    });
    return html;
  }

  generateChapterRange(bookAbbrev, startCh, endCh) {
    const bookName = this.expandBookName(bookAbbrev);
    const book = this.bibleText[bookName];
    if (!book) return '';
    
    let html = '';
    for (let ch = parseInt(startCh); ch <= parseInt(endCh); ch++) {
      if (book[ch]) {
        html += `<h5>${bookName} ${ch}</h5>`;
        Object.entries(book[ch]).forEach(([verse, text]) => {
          html += `<p class="fnb"><span>${verse}</span> ${text}</p>`;
        });
      }
    }
    return html;
  }

  generateVerseRange(bookAbbrev, startCh, startV, endCh, endV) {
    const bookName = this.expandBookName(bookAbbrev);
    const book = this.bibleText[bookName];
    if (!book) return '';
    
    let html = '';
    for (let ch = parseInt(startCh); ch <= parseInt(endCh); ch++) {
      const chapter = book[ch];
      if (!chapter) continue;
      
      html += `<h5>${bookName} ${ch}</h5>`;
      const firstVerse = (ch === parseInt(startCh)) ? parseInt(startV) : 1;
      const lastVerse = (ch === parseInt(endCh)) ? parseInt(endV) : Math.max(...Object.keys(chapter).map(Number));
      
      for (let v = firstVerse; v <= lastVerse; v++) {
        if (chapter[v]) {
          html += `<p class="fnb"><span>${v}</span> ${chapter[v]}</p>`;
        }
      }
    }
    return html;
  }
}

// Usage examples:
// KJV: const generator = new BibleGenerator('kjv');
// NKJV: const generator = new BibleGenerator('nkjv');

// Get version from URL parameter or default to KJV
const urlParams = new URLSearchParams(window.location.search);
const version = urlParams.get('version') || 'kjv';
const generator = new BibleGenerator(version);

generator.loadData().then(() => {
  console.log(`Bible generator loaded with ${version.toUpperCase()} version`);
});