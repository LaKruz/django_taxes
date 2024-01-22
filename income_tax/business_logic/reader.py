from python_calamine import CalamineWorkbook
from django.core.files.uploadedfile import InMemoryUploadedFile


def read_file(file: InMemoryUploadedFile):
    """
    Read data from the input InMemoryUploadedFile using Calamine library.

    Parameters:
    - file (InMemoryUploadedFile): The uploaded file containing data.

    Returns:
    List[List]: A list of lists representing the data read from the file.
    """
    workbook = CalamineWorkbook.from_filelike(file)
    return workbook.get_sheet_by_index(0).to_python()
