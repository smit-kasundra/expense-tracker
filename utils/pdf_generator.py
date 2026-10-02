import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

def generate_financial_report(user, transactions, totals, file_path):
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"Financial Report for {user.username}", styles['Title']))
    elements.append(Paragraph(f"Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Summary
    elements.append(Paragraph("Account Summary", styles['Heading2']))
    summary_data = [
        ['Total Income', f"Rs. {totals['income']:.2f}"],
        ['Total Expenses', f"Rs. {totals['expense']:.2f}"],
        ['Current Balance', f"Rs. {totals['balance']:.2f}"]
    ]
    summary_table = Table(summary_data, colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 24))

    # Transactions Table
    elements.append(Paragraph("Recent Transactions", styles['Heading2']))
    if transactions:
        tx_data = [['Date', 'Category', 'Type', 'Amount']]
        for tx in transactions[:50]: # limit to 50 for the report
            tx_data.append([
                tx.date.strftime('%Y-%m-%d'),
                tx.category.name,
                tx.type.capitalize(),
                f"Rs. {tx.amount:.2f}"
            ])
        
        tx_table = Table(tx_data, colWidths=[100, 150, 100, 100])
        tx_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(tx_table)
    else:
        elements.append(Paragraph("No transactions available.", styles['Normal']))

    doc.build(elements)
