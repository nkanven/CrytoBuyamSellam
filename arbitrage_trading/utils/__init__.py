import os, requests
from dotenv import load_dotenv
import xlsxwriter

load_dotenv()


def notify(text):
    url = f"https://api.telegram.org/{os.environ.get('TELEGRAM_BOT_ID')}/sendMessage?chat_id={os.environ.get('TELEGRAM_CHAT_ID')}&text={text}"
    requests.get(url)

def create_xlsx(file_name, heads, contents):
    """
    func to create xlsx file used to import data to Eduka via API
    @param file_name: file name
    @param heads: table heads
    @param contents: excel content
    @return: void
    """
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(f'{file_name}.xlsx')
    worksheet = workbook.add_worksheet()
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    # Adjust the column width.
    worksheet.set_column(1, 1, 35)
    i = 0
    row = 1
    col = 0
    for head in heads:
        letter = 65 + i
        worksheet.write(f"{chr(letter)}1", head, bold)
        i += 1

    print(contents[0])
    for content in contents:
        worksheet.write_string(row, col, str(content[0]))
        j = 1
        for _c in content[1:]:
            worksheet.write_string(row, col + j, str(_c))
            j += 1
        row += 1

    workbook.close()
