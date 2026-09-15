#!/usr/bin/env python3
"""
Converts local_business_leads.csv into a beautifully formatted Excel / Google Sheets workbook (.xlsx)
with styled headers, column auto-widths, and status tracking columns.
"""

import csv
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def convert_csv_to_excel(csv_path: str = "local_business_leads.csv", xlsx_path: str = "local_business_leads.xlsx"):
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Local CT Business Leads"

    # Read CSV data
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)

    if not data:
        print("CSV is empty.")
        return

    # Add Outreach Tracking Columns if not present
    original_headers = data[0]
    tracking_headers = ["Outreach Status", "Notes / Follow Up"]
    full_headers = original_headers + tracking_headers
    ws.append(full_headers)

    # Styles
    header_fill = PatternFill(start_color="003EC7", end_color="003EC7", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    high_conf_fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid") # Emerald
    med_conf_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # Amber
    flagged_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")  # Rose

    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )

    # Format Header Row
    for col_num, header_title in enumerate(full_headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # Append Data Rows
    for row_idx, row in enumerate(data[1:], start=2):
        row_data = row + ["Not Contacted", ""]
        ws.append(row_data)
        
        # Color code Confidence Flag column (col 6)
        conf_cell = ws.cell(row=row_idx, column=6)
        conf_val = str(conf_cell.value or "")
        if "High" in conf_val:
            conf_cell.fill = high_conf_fill
        elif "Medium" in conf_val:
            conf_cell.fill = med_conf_fill
        else:
            conf_cell.fill = flagged_fill

        # Add borders to row cells
        for col_num in range(1, len(full_headers) + 1):
            c = ws.cell(row=row_idx, column=col_num)
            c.border = thin_border
            c.alignment = Alignment(vertical="center")

    # Auto-adjust Column Widths
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    ws.row_dimensions[1].height = 28
    wb.save(xlsx_path)
    print(f"✅ Created formatted spreadsheet workbook: '{xlsx_path}'")

if __name__ == "__main__":
    convert_csv_to_excel()
