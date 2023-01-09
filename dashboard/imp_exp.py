import pandas as pd
from django.core.files.storage import FileSystemStorage
from .models import ResearchPaper

def import_excel(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    if filename.split('.')[1] == 'csv':
        temp = pd.read_csv(f'./media/{filename}')
        temp.to_excel(f"./media/{filename.split('.')[0]}.xlsx", index=False)
        filename = f"{filename.split('.')[0]}.xlsx"

    col_include = [ 'faculty', 'authors', 'outside author', 'domain', 'title of paper', 'dept.', 'name of journal', 'name of conference', 'title of book', 'title of chapter', 'student', 'scholar', 'publication month', 'publication year', 'doi', 'index database']
    try:
        with pd.ExcelFile(f'./media/{filename}') as file_to_load:
            for sheet in file_to_load.sheet_names:
                data = pd.read_excel(f'./media/{filename}', sheet_name=sheet)
                data_new = data.dropna(how="all").fillna('')[col_include]
                authors = ''
                for rows in data_new.itertuples():
                    if (rows[3] != ''):
                        authors = rows[2]
                    else:
                        authors = ', '.join([str(rows[2]), str(rows[3])])

                    tbl_val = ResearchPaper.objects.create(faculty=rows[1], authors=f'{authors}', domain=rows[4], title_of_paper=rows[5], dept=rows[6], name_of_journal=rows[7], name_of_conference=rows[8], title_of_book=rows[9], title_of_chapter=rows[10], student=rows[11], scholar=rows[12], month=rows[13], year=rows[14], doi=rows[15], index_db=rows[16])

                    tbl_val.save()

        fs.delete(file.name)
        fs.delete(filename)
        success_message = 'Upload Successful. Details Added.'
        return success_message
    except:
        fs.delete(file.name)
        fs.delete(filename)
        error_message = 'Upload Failed. Please check content format.'
        return error_message