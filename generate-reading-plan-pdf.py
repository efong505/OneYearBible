"""
Generate a printable PDF of the One Year Bible Reading Plan.

Usage: python generate-reading-plan-pdf.py [year]
If no year is provided, defaults to the current year.
Outputs: one-year-bible-reading-plan-[year].pdf
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# Color scheme
PRIMARY_COLOR = colors.HexColor('#2c3e50')
ACCENT_COLOR = colors.HexColor('#3498db')
SUNDAY_BG = colors.HexColor('#eaf2f8')
ALT_ROW_BG = colors.HexColor('#f8f9fa')
HEADER_BG = colors.HexColor('#2c3e50')
HEADER_TEXT = colors.white


def get_month_name(month_num):
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    return months[month_num - 1]


def get_day_of_week(year, month, day):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[datetime(year, month, day).weekday()]


def get_short_day(day_name):
    return day_name[:3]


def generate_pdf(year):
    plan_path = Path(__file__).parent / 'assets' / 'data' / 'reading-plan.json'
    logo_path = Path(__file__).parent / 'BibleReadingPlanLogo.png'
    output_path = Path(__file__).parent / f'one-year-bible-reading-plan-{year}.pdf'

    with open(plan_path, 'r') as f:
        plan = json.load(f)

    # Organize entries by month
    months_data = {}
    for date_code, entry in plan.items():
        month = int(date_code[:2])
        day = int(date_code[2:])
        if month not in months_data:
            months_data[month] = []
        months_data[month].append({
            'day': day,
            'date_code': date_code,
            'day_of_week': get_day_of_week(year, month, day),
            'old_testament': entry.get('oldTestament', ''),
            'new_testament': entry.get('newTestament', '')
        })

    # Sort each month by day
    for month in months_data:
        months_data[month].sort(key=lambda x: x['day'])

    # Create PDF
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=PRIMARY_COLOR,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    verse_style = ParagraphStyle(
        'VerseStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#555555'),
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )

    month_title_style = ParagraphStyle(
        'MonthTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=16,
        fontName='Helvetica-Bold'
    )

    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        fontName='Helvetica'
    )

    cell_style_bold = ParagraphStyle(
        'CellStyleBold',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        fontName='Helvetica-Bold'
    )

    branding_style = ParagraphStyle(
        'BrandingStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER
    )

    elements = []

    # --- Cover Page ---
    elements.append(Spacer(1, 1.5 * inch))

    if logo_path.exists():
        logo = Image(str(logo_path), width=2.5 * inch, height=2.5 * inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph('One Year Bible', title_style))
    elements.append(Paragraph('Reading Plan', title_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(str(year), ParagraphStyle(
        'YearStyle',
        parent=styles['Title'],
        fontSize=36,
        textColor=ACCENT_COLOR,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(
        '"Your word is a lamp for my feet, a light on my path."',
        verse_style
    ))
    elements.append(Paragraph('— Psalm 119:105', ParagraphStyle(
        'VerseRef',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#555555'),
        alignment=TA_CENTER,
        fontName='Helvetica'
    )))
    elements.append(Spacer(1, 1 * inch))
    elements.append(Paragraph('By Edward Fong | ekewaka.com', branding_style))
    elements.append(PageBreak())

    # --- Monthly Pages ---
    for month_num in range(1, 13):
        if month_num not in months_data:
            continue

        month_name = get_month_name(month_num)
        elements.append(Paragraph(f'{month_name} {year}', month_title_style))

        # Build table
        header = ['Date', 'Day', 'Old Testament', 'New Testament']
        table_data = [header]

        for entry in months_data[month_num]:
            day_short = get_short_day(entry['day_of_week'])
            ot = entry['old_testament'] if entry['old_testament'] else '—'
            nt = entry['new_testament'] if entry['new_testament'] else '—'

            table_data.append([
                f"{month_name[:3]} {entry['day']}",
                day_short,
                ot,
                nt
            ])

        # Column widths
        col_widths = [0.8 * inch, 0.5 * inch, 3.0 * inch, 3.0 * inch]

        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        # Table styling
        style_commands = [
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), HEADER_TEXT),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),

            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, PRIMARY_COLOR),

            # Alignment
            ('ALIGN', (0, 0), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]

        # Alternating row colors and Sunday highlighting
        for i, entry in enumerate(months_data[month_num], start=1):
            if entry['day_of_week'] == 'Sunday':
                style_commands.append(('BACKGROUND', (0, i), (-1, i), SUNDAY_BG))
                style_commands.append(('FONTNAME', (0, i), (-1, i), 'Helvetica-Oblique'))
            elif i % 2 == 0:
                style_commands.append(('BACKGROUND', (0, i), (-1, i), ALT_ROW_BG))

        table.setStyle(TableStyle(style_commands))
        elements.append(table)

        # Footer with branding
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(
            f'One Year Bible Reading Plan — {year} | ekewaka.com',
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8,
                          textColor=colors.HexColor('#aaaaaa'), alignment=TA_CENTER)
        ))

        if month_num < 12:
            elements.append(PageBreak())

    # Build PDF
    doc.build(elements)
    print(f"PDF generated: {output_path}")


if __name__ == '__main__':
    year = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().year
    generate_pdf(year)
