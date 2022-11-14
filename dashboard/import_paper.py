import pandas as pd
from django.core.files.storage import FileSystemStorage
from .models import ResearchPaper

def import_excel(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    data = pd.read_excel(f'./media/{filename}')
    data_new = data.dropna(how="all").fillna('')
    try:
        for rows in data_new.itertuples():
            if (rows[3] != ''):
                authors = rows[2]
            else:
                authors = ', '.join([rows[2], rows[3]])

            if (rows[6] != ''):
                tbl_val = ResearchPaper.objects.create(authors=f'{authors}', domain=rows[1], affilation=rows[4], month=rows[5], year=int(rows[6]), doi=rows[7])
            else:
                tbl_val = ResearchPaper.objects.create(authors=f'{authors}', domain=rows[1], affilation=rows[4], month=rows[5], doi=rows[7])

            tbl_val.save()
        
        fs.delete(file.name)
        success_message = 'Upload Successful. Details Added.'
        return success_message
    except:
        fs.delete(file.name)
        error_message = 'Upload Failed. Please check content format.'
        return error_message
