"""
Generate corrected intro/outro scripts for Julia's version.
Fixes:
1. Abbreviations expanded to full book names
2. Chapter:verse notation spoken properly (chapter X verse Y)
3. Hyphens converted to "through"
4. Personal messages reframed so Danielle naturally weaves in Ed's words
   (instead of speaking AS Ed)

Uses same Polly voice (Danielle Long-Form Neural) and same approach as general public version.
"""

import json
import os
import re
import random

# Same abbreviation mapping as the general public script
BOOK_ABBREVIATIONS = {
    "Gen.": "Genesis", "Ex.": "Exodus", "Lev.": "Leviticus",
    "Num.": "Numbers", "Deut.": "Deuteronomy", "Josh.": "Joshua",
    "Jdgs.": "Judges", "Ruth": "Ruth",
    "1 Sam.": "1 Samuel", "2 Sam.": "2 Samuel",
    "1 Kgs.": "1 Kings", "2 Kgs.": "2 Kings",
    "1 Chr.": "1 Chronicles", "2 Chr.": "2 Chronicles",
    "Ez.": "Ezra", "Ezra": "Ezra", "Neh.": "Nehemiah",
    "Est.": "Esther", "Job": "Job", "Ps.": "Psalms",
    "Prov.": "Proverbs", "Eccl.": "Ecclesiastes",
    "Songs": "Song of Solomon", "Isa.": "Isaiah",
    "Jer.": "Jeremiah", "Lam.": "Lamentations",
    "Ezek.": "Ezekiel", "Dan.": "Daniel", "Hos.": "Hosea",
    "Joel": "Joel", "Amos": "Amos", "Obad.": "Obadiah",
    "Jon.": "Jonah", "Mic.": "Micah", "Nah.": "Nahum",
    "Hab.": "Habakkuk", "Zeph.": "Zephaniah",
    "Hag.": "Haggai", "Zech.": "Zechariah", "Mal.": "Malachi",
    "Matt.": "Matthew", "Mark": "Mark", "Luke": "Luke",
    "John": "John", "Acts": "Acts", "Rom.": "Romans",
    "1 Cor.": "1 Corinthians", "2 Cor.": "2 Corinthians",
    "Gal.": "Galatians", "Eph.": "Ephesians",
    "Phil.": "Philippians", "Col.": "Colossians",
    "1 Thess.": "1 Thessalonians", "2 Thess.": "2 Thessalonians",
    "1 Tim.": "1 Timothy", "2 Tim.": "2 Timothy",
    "Titus": "Titus", "Philem.": "Philemon", "Heb.": "Hebrews",
    "Jas.": "James", "1 Pet.": "1 Peter", "2 Pet.": "2 Peter",
    "1 Jn.": "1 John", "2 Jn.": "2 John", "3 Jn.": "3 John",
    "Jude": "Jude", "Rev.": "Revelation",
}

# Special intro for January 1st
INTRO_0101 = (
    "Good morning Julia! Happy New Year! Ed is so proud of you for committing to the One Year Bible reading plan. "
    "He says this is going to be such a blessing in your life, and he's excited to walk through God's word with you every single day. "
    "Today is January 1st, and we're starting at the very beginning. "
    "Today's passages are {passages}. Let's begin this incredible journey together."
)

# Special intro for December 31st
INTRO_1231 = (
    "Julia! It's December 31st, and Ed wanted me to tell you something. "
    "He is so incredibly proud of you. You did it! You made it through the entire One Year Bible reading plan. "
    "He says that takes real dedication and faithfulness, and he's honored to have been part of this journey with you. "
    "Today's final passages are {passages}. Let's finish strong."
)

# Special outro for December 31st
OUTRO_1231 = (
    "Congratulations, Julia! You have completed the One Year Bible reading plan! "
    "Ed says he couldn't be more proud of you. He wants you to know that this is something you can do again and again, year after year. "
    "Each time through, God reveals something new. Ed hopes you'll join him again next year. "
    "He loves you so much, and may God's word continue to dwell richly in your heart."
)

# Reframed intros - Danielle naturally weaves in Ed's messages
INTROS = [
    "Good morning Julia! Ed wanted me to let you know he's prepared today's reading just for you. He says you light up every room you enter, and today we're going to let God's word light up your heart. It's {date}, and today's passages are {passages}. Let's begin.",
    "Rise and shine, Julia! Ed asked me to tell you that you're more precious than rubies. He's picked out today's treasures from Scripture just for you. It's {date}, and we're reading {passages}. Let's dive in.",
    "Good morning beautiful! Ed says to tell you that you're his favorite person to read to. It's {date}, and he's lovingly prepared today's One Year Bible reading. Today's passages are {passages}. Let's get started.",
    "Hello Julia! Ed wanted you to know that reading God's word for you is one of his favorite ways to show love. It's {date}, and today we're reading {passages}. Grab your coffee and let's begin.",
    "Wake up, Julia! Ed says you're the answer to prayers he didn't even know he was praying. He's prepared another spiritual feast for you today, {date}. Today's passages are {passages}. Let's see what God has in store.",
    "Good morning, gorgeous! Ed asked me to remind you that you're fearfully and wonderfully made. It's {date}, and today's reading is {passages}. Let's explore God's word together.",
    "Julia, Ed says good morning! He wants you to know you're his treasure, his joy, and his best friend. It's {date}, and he's prepared today's passages for you. We're reading {passages}. Let's begin.",
    "Hey Julia! Ed wanted me to tell you that he's grateful for every moment with you. It's {date}, and today's One Year Bible reading covers {passages}. Let's get into God's word.",
]

# Reframed outros - Danielle naturally weaves in Ed's closing messages
OUTROS = [
    "That concludes today's reading. Ed wants you to know that you make every day brighter than the promises we just read about. He loves you more than words can express. See you tomorrow, Julia!",
    "And that wraps up today's Scripture. Ed says you're his answered prayer and he's grateful for every moment with you. May God's blessings follow you everywhere you go today.",
    "That's a wrap on today's reading! Ed hopes this filled your heart as much as you fill his every single day. Remember, you're loved beyond measure, by God and by your devoted husband.",
    "Another beautiful day of Scripture complete. Ed wanted me to remind you that you're the melody to his heart's song, and these scriptures are just the harmony. He loves you to the moon and back.",
    "And that concludes today's passages. Ed says he feels blessed to be your husband and he's thinking of you right now. Until tomorrow's reading, may God's word dwell richly in your heart.",
    "That's all for today's reading, Julia. Ed wants you to know that you're his sunshine and his best friend. Sweet dreams, and he'll have another reading ready for you tomorrow.",
    "Today's reading is complete. Ed asked me to tell you that he loves you more than all the words in this Bible combined. May God's peace be with you today, Julia.",
    "And we're done for today! Ed says you're the best thing that ever happened to him. He hopes God's word blessed you today as much as you bless him every day. See you tomorrow!",
]


def expand_abbreviations(text):
    """Replace all book abbreviations with full names."""
    if not text:
        return ""
    sorted_abbrevs = sorted(BOOK_ABBREVIATIONS.keys(), key=len, reverse=True)
    for abbrev in sorted_abbrevs:
        if abbrev in text:
            text = text.replace(abbrev, BOOK_ABBREVIATIONS[abbrev])
    return text


def format_passages(old_testament, new_testament):
    """Format passages for natural spoken audio."""
    ot = expand_abbreviations(old_testament)
    nt = expand_abbreviations(new_testament)

    # Replace hyphens with "through" BEFORE converting chapter:verse
    for t in [ot, nt]:
        pass  # We'll process each separately below

    def process_passage(text):
        if not text:
            return ""
        # Cross-book with chapter:verse on both sides
        text = re.sub(r'(\d+:\d+)-(\d+:\d+)', r'\1 through \2', text)
        # Chapter:verse followed by a book name
        text = re.sub(r'(\d+:\d+)-\s*([A-Z1-9])', r'\1 through \2', text)
        # Chapter number followed by a book name (e.g., "13-Esther")
        text = re.sub(r'(\d+)-\s*([A-Z])', r'\1 through \2', text)
        # Simple chapter ranges like "Psalms 1-5"
        text = re.sub(r'(\d+)-(\d+)(?!:)', r'\1 through \2', text)
        # Now convert chapter:verse to spoken form
        text = re.sub(r'(\d+):(\d+)', r'chapter \1 verse \2', text)
        return text

    ot = process_passage(ot)
    nt = process_passage(nt)

    if ot and nt:
        return f"{ot} and {nt}"
    elif ot:
        return ot
    elif nt:
        return nt
    return ""


def add_ordinal(day_num):
    """Convert day number to ordinal."""
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
    """Convert 'January 1' to 'January 1st' (no year, so it's reusable annually)."""
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


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    reading_plan_path = os.path.join(project_root, "assets", "data", "reading-plan.json")

    with open(reading_plan_path, "r", encoding="utf-8") as f:
        reading_plan = json.load(f)

    # Output directory
    audio_replacement_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(audio_replacement_dir, "julia-intro-outro-scripts")
    os.makedirs(output_dir, exist_ok=True)

    # Use a fixed seed so results are reproducible but varied
    random.seed(42)

    count = 0
    for date_code, entry in sorted(reading_plan.items()):
        date_str = entry["date"]
        old_testament = entry.get("oldTestament", "")
        new_testament = entry.get("newTestament", "")

        spoken_date = format_date_for_speech(date_str)
        passages = format_passages(old_testament, new_testament)

        # Special handling for first and last day
        if date_code == "0101":
            intro_text = INTRO_0101.format(passages=passages)
            outro_template = OUTROS[0]
        elif date_code == "1231":
            intro_text = INTRO_1231.format(passages=passages)
            outro_template = OUTRO_1231
        else:
            intro_template = INTROS[count % len(INTROS)]
            intro_text = intro_template.format(date=spoken_date, passages=passages)
            outro_template = OUTROS[count % len(OUTROS)]

        if date_code == "1231":
            outro_text = OUTRO_1231
        else:
            outro_text = outro_template if date_code == "0101" else outro_template

        intro_text = make_ssml_safe(intro_text)
        outro_text = make_ssml_safe(outro_text)

        # Write intro
        intro_path = os.path.join(output_dir, f"{date_code}_intro.txt")
        with open(intro_path, "w", encoding="utf-8") as f:
            f.write(intro_text)

        # Write outro
        outro_path = os.path.join(output_dir, f"{date_code}_outro.txt")
        with open(outro_path, "w", encoding="utf-8") as f:
            f.write(outro_text)

        count += 1

    print(f"Generated {count} intro/outro script pairs in: {output_dir}")

    # Show samples
    print(f"\n--- Sample intro (0101): ---")
    with open(os.path.join(output_dir, "0101_intro.txt"), "r") as f:
        print(f.read())
    print(f"\n--- Sample intro (0512): ---")
    with open(os.path.join(output_dir, "0512_intro.txt"), "r") as f:
        print(f.read())
    print(f"\n--- Sample intro (1201 - has Rev.): ---")
    with open(os.path.join(output_dir, "1201_intro.txt"), "r") as f:
        print(f.read())
    print(f"\n--- Sample outro (0101): ---")
    with open(os.path.join(output_dir, "0101_outro.txt"), "r") as f:
        print(f.read())

    # Character count estimate
    total_chars = 0
    for date_code in reading_plan:
        intro_path = os.path.join(output_dir, f"{date_code}_intro.txt")
        outro_path = os.path.join(output_dir, f"{date_code}_outro.txt")
        with open(intro_path, "r") as f:
            total_chars += len(f.read())
        with open(outro_path, "r") as f:
            total_chars += len(f.read())

    print(f"\nTotal characters for Polly: ~{total_chars:,}")
    print(f"Neural free tier: 1,000,000 chars/month")
    print(f"You'll use: {total_chars/1_000_000*100:.1f}% of monthly free tier")


if __name__ == "__main__":
    main()
