from xlsxwriter import Workbook
from io import BytesIO
from .reader import read_file
from django.core.files.uploadedfile import InMemoryUploadedFile

TAX_RANGE = 5000000
LOWER_TAX = 0.13
HIGHER_TAX = 0.15


def get_income_tax(income) -> int:
    """
    Calculate income tax based on specified tax rates.

    Parameters:
    - income (float): The income amount.

    Returns:
    int: Calculated income tax.
    """
    lower_bound_part = LOWER_TAX * min(float(income), TAX_RANGE)
    higher_bound_part = HIGHER_TAX * max(0, income - TAX_RANGE)
    return round(lower_bound_part + higher_bound_part)


def add_header(wb: Workbook) -> None:
    """
    Add header to the worksheet with specified styles.

    Parameters:
    - wb (Workbook): The XlsxWriter Workbook object.
    """
    # Styles for header cells from rept_header.xlsx
    header_style = wb.add_format({
        'bold': True,
        'size': 10,
        'font_name': 'Arial',
        'color': '00005c',
        'border': 1,
        'border_color': 'A0A0A0',
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True,
        'fg_color': 'cbe4e5',
    })
    ws = wb.get_worksheet_by_name('Отчет')
    ws.merge_range('A1:A2', 'Филиал', cell_format=header_style)
    ws.merge_range('B1:B2', 'Сотрудник', cell_format=header_style)
    ws.merge_range('C1:C2', 'Налоговая база', cell_format=header_style)
    ws.merge_range('D1:E1', 'Налог', cell_format=header_style)
    ws.write('D2', 'Исчислено всего', header_style)
    ws.write('E2', 'Исчислено всего по формуле', header_style)
    ws.merge_range('F1:F2', 'Отклонения', cell_format=header_style)


def get_processed_data(file: InMemoryUploadedFile) -> list[list]:
    """
    Process data from the input file and return a list of processed results.

    Parameters:
    - file (InMemoryUploadedFile): The uploaded file containing data.

    Returns:
    List[List]: A list of processed data.
    """
    data = read_file(file)
    del data[0:3]
    result = []
    for line in data:
        result_line = []
        result_line.append(line[0])
        result_line.append(line[1])
        result_line.append(line[4])
        if not line[1] or not line[5]:
            continue
        result_line.append(line[5])
        calculated_income_tax = get_income_tax(line[4])
        result_line.append(calculated_income_tax)
        result_line.append(line[5] - calculated_income_tax)
        result.append(result_line)
    result.sort(key=lambda x: x[5], reverse=True)
    return result


def write_data(wb: Workbook, data: list[list[str | float]]) -> None:
    """
    Write processed data to the worksheet with specified styles.

    Parameters:
    - wb (Workbook): The XlsxWriter Workbook object.
    - data (List[List]): The processed data to be written to the worksheet.
    """
    ws = wb.get_worksheet_by_name('Отчет')
    # Стили для столбца "Отклонения"
    tax_green = wb.add_format({
        'fg_color': '00ff00'
    })
    tax_red = wb.add_format({
        'fg_color': 'ff0000'
    })
    for line_number, line in enumerate(data, start=2):
        ws.write_string(line_number, 0, line[0])
        ws.write_string(line_number, 1, line[1])
        ws.write_number(line_number, 2, line[2])
        ws.write_number(line_number, 3, line[3])
        ws.write_number(line_number, 4, line[4])
        default_format = tax_green
        if line[5] != 0:
            default_format = tax_red
        ws.write_number(
            line_number, 5, line[5], cell_format=default_format)


def get_tax(file: InMemoryUploadedFile) -> BytesIO:
    """
    Generate a tax report and return it as a BytesIO object.

    Parameters:
    - file (InMemoryUploadedFile): The uploaded file containing data.

    Returns:
    BytesIO: The generated tax report in BytesIO format.
    """
    book = BytesIO()
    with Workbook(book) as wb:
        ws = wb.add_worksheet('Отчет')
        add_header(wb)
        data = get_processed_data(file)
        write_data(wb, data)
        ws.autofit()
    book.seek(0)
    return book
