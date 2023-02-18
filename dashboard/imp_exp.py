import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import ResearchPaper

def import_excel(request, file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    if filename.split('.')[1] == 'csv':
        temp = pd.read_csv(f'./media/{filename}')
        temp.to_excel(f"./media/{filename.split('.')[0]}.xlsx", index=False)
        filename = f"{filename.split('.')[0]}.xlsx"

    col_include = [ 'faculty', 'authors', 'outside authors', 'domain', 'title of paper', 'dept.', 'name of journal', 'name of conference', 'title of book', 'title of chapter', 'student', 'scholar', 'publication month', 'publication year', 'doi', 'index database']
    with pd.ExcelFile(f'./media/{filename}') as file_to_load:
        message = 'Upload Failed Check File Content, '
        for sheet in file_to_load.sheet_names:
            data = pd.read_excel(f'./media/{filename}', sheet_name=sheet)
            data = data.dropna(how="all").fillna('')[col_include]
            for rows in data.itertuples():
                if (ResearchPaper.objects.filter(title_of_paper__iexact = str(rows[5])).exists()):
                    # Update the already existing row with new user
                    curr_paper = ResearchPaper.objects.get(title_of_paper = str(rows[5]))
                    curr_paper.authors = curr_paper.authors + f' {rows[2]}'
                    curr_paper.authors = curr_paper.authors.rstrip(', ')
                    curr_paper.outside_authors = curr_paper.outside_authors + f' {rows[3]}'
                    curr_paper.outside_authors = curr_paper.outside_authors.rstrip(', ')
                    curr_paper.save()
                    curr_user = User.objects.get(pk=request.user.pk)
                    curr_paper.users_associated.add(curr_user)
                else:
                    if len(rows[1]) > 5:
                        message += f'Possible error in row {rows[0] + 1}'
                        return (message, fs)
                    elif not str(rows[2]).strip():
                        message += f'Authors field cannot be empty in row {rows[0] + 1}'
                        return (message, fs)
                    elif not str(rows[5]).strip():
                        message += f'Title of Papers field cannot be empty in row {rows[0] + 1}'
                        return (message, fs)
                    elif len(rows[11]) > 3:
                        message += f'Possible error in row {rows[0] + 1}'
                        return (message, fs)
                    elif len(rows[12]) > 3:
                        message += f'Possible error in row {rows[0] + 1}'
                        return (message, fs)
                    elif str(rows[13]).isdigit():
                        message += f'Month should not be in number in row {rows[0] + 1}'
                        return (message, fs)
                    elif str(rows[14]).strip():
                        if '-' in str(rows[14]) and len(str(rows[14]).split('-')[0]) == 4 and len(str(rows[14]).split('-')[1]) == 4:
                            message += f'Year column should be in the format of YYYY-YYYY in row {rows[0] + 1}'
                            return (message, fs)
                    elif str(rows[15]).strip():
                        validate = URLValidator(schemes=['doi', 'http', 'https', 'fpt', 'ftps'])
                        try:
                            validate(str(rows[15]))
                        except ValidationError:
                            message += f'Provided doi is not a valid url in row {rows[0] + 1}'
                            return (message, fs)
                    else:
                        tbl_val = ResearchPaper.objects.create(
                            faculty=rows[1], 
                            authors=rows[2], 
                            outside_authors=rows[3],
                            domain=rows[4], 
                            title_of_paper=rows[5], 
                            dept=rows[6], 
                            name_of_journal=rows[7], 
                            name_of_conference=rows[8], 
                            title_of_book=rows[9], 
                            title_of_chapter=rows[10], 
                            student=rows[11], 
                            scholar=rows[12], 
                            month=rows[13], 
                            year=rows[14], 
                            doi=rows[15], 
                            index_db=rows[16])

                        tbl_val.save()
                    # curr_user = User.objects.get(pk=request.user.pk)
                    # tbl_val.users_accociated.add(curr_user)
                    # ------------------------------------------------
                        tbl_val.users_associated.add(request.user)
        message = 'Upload Successful. Details Added.'
    # except:
        return (message, fs)
