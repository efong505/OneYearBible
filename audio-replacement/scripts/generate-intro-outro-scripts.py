"""
Generate intro/outro scripts for all 365 days.
Reads reading-plan.json, expands all abbreviations to full book names,
and outputs SSML-safe text files ready for Polly (Danielle Long-Form Neural).
"""

import json
import os
import re

# Abbreviation to full book name mapping
BOOK_ABBREVIATIONS = {
    # Old Testament
    "Gen.": "Genesis",
    "Ex.": "Exodus",
    "Lev.": "Leviticus",
    "Num.": "Numbers",
    "Deut.": "Deuteronomy",
    "Josh.": "Joshua",
    "Jdgs.": "Judges",
    "Ruth": "Ruth",
    "1 Sam.": "1 Samuel",
    "2 Sam.": "2 Samuel",
    "1 Kgs.": "1 Kings",
    "2 Kgs.": "2 Kings",
    "1 Chr.": "1 Chronicles",
    "2 Chr.": "2 Chronicles",
    "Ez.": "Ezra",
    "Ezra": "Ezra",
    "Neh.": "Nehemiah",
    "Est.": "Esther",
    "Job": "Job",
    "Ps.": "Psalms",
    "Prov.": "Proverbs",
    "Eccl.": "Ecclesiastes",
    "Songs": "Song of Solomon",
    "Isa.": "Isaiah",
    "Jer.": "Jeremiah",
    "Lam.": "Lamentations",
    "Ezek.": "Ezekiel",
    "Dan.": "Daniel",
    "Hos.": "Hosea",
    "Joel": "Joel",
    "Amos": "Amos",
    "Obad.": "Obadiah",
    "Jon.": "Jonah",
    "Mic.": "Micah",
    "Nah.": "Nahum",
    "Hab.": "Habakkuk",
    "Zeph.": "Zephaniah",
    "Hag.": "Haggai",
    "Zech.": "Zechariah",
    "Mal.": "Malachi",
    # New Testament
    "Matt.": "Matthew",
    "Mark": "Mark",
    "Luke": "Luke",
    "John": "John",
    "Acts": "Acts",
    "Rom.": "Romans",
    "1 Cor.": "1 Corinthians",
    "2 Cor.": "2 Corinthians",
    "Gal.": "Galatians",
    "Eph.": "Ephesians",
    "Phil.": "Philippians",
    "Col.": "Colossians",
    "1 Thess.": "1 Thessalonians",
    "2 Thess.": "2 Thessalonians",
    "1 Tim.": "1 Timothy",
    "2 Tim.": "2 Timothy",
    "Titus": "Titus",
    "Philem.": "Philemon",
    "Heb.": "Hebrews",
    "Jas.": "James",
    "1 Pet.": "1 Peter",
    "2 Pet.": "2 Peter",
    "1 Jn.": "1 John",
    "2 Jn.": "2 John",
    "3 Jn.": "3 John",
    "Jude": "Jude",
    "Rev.": "Revelation",
}


def expand_abbreviations(text):
    """Replace all book abbreviations with full names."""
    if not text:
        return ""
    # Sort by length descending so longer matches are tried first
    # (e.g., "1 Sam." before "Sam.", "2 Chr." before "Chr.")
    sorted_abbrevs = sorted(BOOK_ABBREVIATIONS.keys(), key=len, reverse=True)
    for abbrev in sorted_abbrevs:
        if abbrev in text:
            text = text.replace(abbrev, BOOK_ABBREVIATIONS[abbrev])
    return text


def format_chapter_verse(text):
    """Convert chapter:verse notation to spoken form.
    '1:1' -> 'chapter 1 verse 1'
    '3:7' -> 'chapter 3 verse 7'
    """
    # Replace all chapter:verse patterns
    text = re.sub(r'(\d+):(\d+)', r'chapter \1 verse \2', text)
    return text


def format_passages(old_testament, new_testament):
    """Format the passages string for spoken audio."""
    ot = expand_abbreviations(old_testament)
    nt = expand_abbreviations(new_testament)

    # First, replace hyphens with "through" BEFORE converting chapter:verse
    # Cross-book with chapter:verse on both sides
    ot = re.sub(r'(\d+:\d+)-(\d+:\d+)', r'\1 through \2', ot)
    ot = re.sub(r'(\d+:\d+)-\s*([A-Z1-9])', r'\1 through \2', ot)
    # Chapter number followed by a book name (e.g., "13-Esther" or "27-Numbers")
    ot = re.sub(r'(\d+)-\s*([A-Z])', r'\1 through \2', ot)
    # Simple chapter ranges like "Psalms 1-5" or "Isaiah 14-17"
    ot = re.sub(r'(\d+)-(\d+)(?!:)', r'\1 through \2', ot)

    nt = re.sub(r'(\d+:\d+)-(\d+:\d+)', r'\1 through \2', nt)
    nt = re.sub(r'(\d+:\d+)-\s*([A-Z1-9])', r'\1 through \2', nt)
    nt = re.sub(r'(\d+)-\s*([A-Z])', r'\1 through \2', nt)
    nt = re.sub(r'(\d+)-(\d+)(?!:)', r'\1 through \2', nt)

    # Now convert chapter:verse to spoken form
    ot = format_chapter_verse(ot)
    nt = format_chapter_verse(nt)

    if ot and nt:
        return f"{ot} and {nt}"
    elif ot:
        return ot
    elif nt:
        return nt
    return ""


def add_ordinal(day_num):
    """Convert day number to ordinal (1 -> 1st, 2 -> 2nd, etc.)."""
    if 11 <= day_num <= 13:
        return f"{day_num}th"
    last_digit = day_num % 10
    if last_digit == 1:
        return f"{day_num}st"
    elif last_digit == 2:
        return f"{day_num}nd"
    elif last_digit == 3:
        return f"{day_num}rd"
    else:
        return f"{day_num}th"


def format_date_for_speech(date_str):
    """Convert 'January 1' to 'January 1st'."""
    parts = date_str.split(" ")
    month = parts[0]
    day_num = int(parts[1])
    return f"{month} {add_ordinal(day_num)}"


def make_ssml_safe(text):
    """Escape characters that are invalid in SSML."""
    text = text.replace("&", "and")
    text = text.replace("<", "")
    text = text.replace(">", "")
    return text


def generate_intro(date_str, passages):
    """Generate the intro script."""
    spoken_date = format_date_for_speech(date_str)
    intro = (
        f"Welcome to today's One Year Bible reading for {spoken_date}. "
        f"We're so glad you're joining us on this journey of reading through the Bible in one year. "
        f"Today's passages are {passages}. Let's begin."
    )
    return make_ssml_safe(intro)


def generate_outro():
    """Generate the outro script (same for all days)."""
    return (
        "That concludes today's reading. "
        "May God's word richly bless you today. "
        "We look forward to seeing you tomorrow."
    )


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))  # audio-replacement/scripts -> project root
    reading_plan_path = os.path.join(project_root, "assets", "data", "reading-plan.json")

    with open(reading_plan_path, "r", encoding="utf-8") as f:
        reading_plan = json.load(f)

    # Create output directory
    audio_replacement_dir = os.path.dirname(script_dir)  # audio-replacement/
    output_dir = os.path.join(audio_replacement_dir, "intro-outro-scripts")
    os.makedirs(output_dir, exist_ok=True)

    # Generate scripts for all days
    outro_text = generate_outro()
    count = 0
    # Custom scripts that should not be overwritten
    custom_files = {"0101_intro.txt", "1231_intro.txt", "1231_outro.txt"}

    for date_code, entry in sorted(reading_plan.items()):
        date_str = entry["date"]
        old_testament = entry.get("oldTestament", "")
        new_testament = entry.get("newTestament", "")

        passages = format_passages(old_testament, new_testament)
        intro_text = generate_intro(date_str, passages)

        # Write intro (skip custom files)
        intro_filename = f"{date_code}_intro.txt"
        if intro_filename not in custom_files:
            intro_path = os.path.join(output_dir, intro_filename)
            with open(intro_path, "w", encoding="utf-8") as f:
                f.write(intro_text)

        # Write outro (skip custom files)
        outro_filename = f"{date_code}_outro.txt"
        if outro_filename not in custom_files:
            outro_path = os.path.join(output_dir, outro_filename)
            with open(outro_path, "w", encoding="utf-8") as f:
                f.write(outro_text)

        count += 1

    print(f"Generated {count} intro/outro script pairs in: {output_dir}")
    print(f"\nSample intro (0101):")
    sample_path = os.path.join(output_dir, "0101_intro.txt")
    with open(sample_path, "r", encoding="utf-8") as f:
        print(f.read())
    print(f"\nSample intro (0307):")
    sample_path = os.path.join(output_dir, "0307_intro.txt")
    with open(sample_path, "r", encoding="utf-8") as f:
        print(f.read())
    print(f"\nSample intro (1201 - has Rev.):")
    sample_path = os.path.join(output_dir, "1201_intro.txt")
    with open(sample_path, "r", encoding="utf-8") as f:
        print(f.read())
    print(f"\nOutro (same for all):")
    print(outro_text)

    # Calculate approximate character count for Polly billing
    total_chars = 0
    for date_code in reading_plan:
        intro_path = os.path.join(output_dir, f"{date_code}_intro.txt")
        with open(intro_path, "r", encoding="utf-8") as f:
            total_chars += len(f.read())
        total_chars += len(outro_text)

    print(f"\nTotal characters for Polly: ~{total_chars:,}")
    print(f"Neural free tier: 1,000,000 chars/month")
    print(f"You'll use: {total_chars/1_000_000*100:.1f}% of monthly free tier")


if __name__ == "__main__":
    main()
