from django.http import HttpResponse
from django.shortcuts import render
from googleapiclient.errors import HttpError
#Подключение к Gmail api
from FoldersGmail.GmailAuth import gmail_auth, get_users
#Подключение моделей бд
from main_page.models import Users, Folder,Words
#Подключение формы для сохранения данных
from .forms import *


def get_emails(request):
    try:
        get_users()
        results = gmail_auth().users().messages().list(userId='me', labelIds=['INBOX']).execute()
        messages = results.get("messages", [])
        content_list = []
        for message in messages:
            msg = gmail_auth().users().messages().get(userId='me', id=message['id'], format='full').execute()
            content_list.append(msg)

        return render(request, 'email_list.html', {'emails': content_list})

    except HttpError as error:
        print(f"An error occurred: {error}")

def folders_work(request):
    try:
        folders = Folder.objects.filter(users_id=get_users().id)
        return render(request, 'folders_work.html', {'folders':folders})
    except:
        return render(request, 'folders_work.html')

def add_folder(request):
    #Если форма имеет метод пост
    if request.method == 'POST':
        #Выполняем по словарю POST
        form = AddFormFolder(request.POST)
        if form.is_valid():
            data_form = form.cleaned_data
            if not Folder.objects.filter(title=data_form['title'],users_id=get_users().id):
                save_folder = Folder.objects.create(title=data_form['title'], discription=data_form['discriprion'], users_id=get_users().id)
                if ',' in data_form['words']:
                    words_arr = data_form['words'].split(',')
                    for word in words_arr:
                        Words.objects.create(words=word, foldres_id=save_folder.id)

                    return render(request, 'add_folder.html', {'form': form})
                else:
                    Words.objects.create(words=data_form['words'], foldres_id=save_folder.id)
                    return render(request, 'add_folder.html', {'form': form})
            else:
                form = AddFormFolder()
                err_mess = "Such a folder already exists!"
                return render(request, 'add_folder.html', {'form': form,'err_mess': err_mess})
    else:
        form = AddFormFolder()
        return render(request, 'add_folder.html', {'form': form})

def open_folder(request, foldres_id):
    arr_words = Words.objects.filter(foldres_id=foldres_id)
    return render(request, 'view_folder.html', {'words':arr_words})
