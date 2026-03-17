import os
from datetime import datetime


def calculate_mttr(incident):
    """Calculate Mean Time To Recovery in minutes."""
    if incident.start_time and incident.end_time:
        delta = incident.end_time - incident.start_time
        return round(delta.total_seconds() / 60, 2)
    return 0


def generate_postmortem_pdf(incident, postmortem, mttr):
    """Generate a PDF report for the post-mortem."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib import colors
        from reportlab.lib.units import cm

        output_dir = os.path.join(os.getcwd(), 'deliverables')
        os.makedirs(output_dir, exist_ok=True)
        filename = f"postmortem_incident_{incident.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
        filepath = os.path.join(output_dir, filename)

        doc = SimpleDocTemplate(filepath, pagesize=A4,
                                rightMargin=2 * cm, leftMargin=2 * cm,
                                topMargin=2 * cm, bottomMargin=2 * cm)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=20, spaceAfter=12)
        story.append(Paragraph("Incident Post-Mortem Report", title_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        story.append(Spacer(1, 12))

        # Incident metadata table
        meta = [
            ['Incident ID', str(incident.id), 'Severity', incident.severity],
            ['Title', incident.title, 'Status', incident.status],
            ['Start Time', str(incident.start_time), 'End Time', str(incident.end_time or 'Ongoing')],
            ['Detected By', incident.detected_by or 'N/A', 'Reported By', incident.reported_by or 'N/A'],
            ['MTTR', f"{mttr} minutes", '', ''],
        ]
        table = Table(meta, colWidths=[3.5 * cm, 7 * cm, 3.5 * cm, 7 * cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8EAF6')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#E8EAF6')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(table)
        story.append(Spacer(1, 16))

        def section(title, content):
            story.append(Paragraph(title, styles['Heading2']))
            story.append(Paragraph(content or 'N/A', styles['BodyText']))
            story.append(Spacer(1, 10))

        section("Summary", postmortem.summary)
        section("Impact", postmortem.impact)
        section("Root Cause", postmortem.root_cause)
        section("Detection Method", postmortem.detection_method)
        section("Resolution Steps", postmortem.resolution_steps)
        section("Lessons Learned", postmortem.lessons_learned)

        # Timeline
        if postmortem.timeline:
            story.append(Paragraph("Incident Timeline", styles['Heading2']))
            tl_data = [['Time', 'Event']]
            for entry in postmortem.timeline:
                tl_data.append([entry.get('time', ''), entry.get('event', '')])
            tl_table = Table(tl_data, colWidths=[5 * cm, 16 * cm])
            tl_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3F51B5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ]))
            story.append(tl_table)
            story.append(Spacer(1, 10))

        # Action items
        if postmortem.action_items:
            story.append(Paragraph("Action Items", styles['Heading2']))
            ai_data = [['Task', 'Owner', 'Due Date']]
            for item in postmortem.action_items:
                ai_data.append([item.get('task', ''), item.get('owner', ''), item.get('due_date', '')])
            ai_table = Table(ai_data, colWidths=[10 * cm, 5 * cm, 6 * cm])
            ai_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3F51B5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ]))
            story.append(ai_table)

        doc.build(story)
        return filepath

    except Exception as e:
        return f"PDF generation failed: {str(e)}"
