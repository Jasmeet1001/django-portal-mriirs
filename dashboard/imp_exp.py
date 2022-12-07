import pandas as pd
from django.core.files.storage import FileSystemStorage
from .models import ResearchPaper

def import_excel(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    excel_file = pd.ExcelFile(f'./media/{filename}')
    col_include = [ 'faculty', 'authors', 'outside author', 'title of paper', 'dept.', 'name of journal', 'name of conference', 'title of book', 'title of chapter', 'scholar', 'publication month', 'publication year', 'doi', 'scopus id']
    try:
        with pd.ExcelFile(f'./media/{filename}') as excel_file:
            for sheet in excel_file.sheet_names:
                data = pd.read_excel(f'./media/{filename}', sheet_name=sheet)
                data_new = data.dropna(how="all").fillna('')[col_include]
                authors = ''
                for rows in data_new.itertuples():
                    if (rows[3] != ''):
                        authors = rows[2]
                    else:
                        authors = ', '.join([str(rows[2]), str(rows[3])])

                    tbl_val = ResearchPaper.objects.create(faculty=rows[1], authors=f'{authors}', title_of_paper=rows[4], dept=rows[5], name_of_journal=rows[6], name_of_conference=rows[7], title_of_book=rows[8], title_of_chapter=rows[9], scholar=rows[10], month=rows[11], year=rows[12])

                    tbl_val.save()

        fs.delete(file.name)
        success_message = 'Upload Successful. Details Added.'
        return success_message
    except:
        fs.delete(file.name)
        error_message = 'Upload Failed. Please check content format.'
        return error_message