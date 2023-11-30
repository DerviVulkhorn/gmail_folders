import concurrent
import locale

from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from googleapiclient.errors import HttpError
#Подключение к Gmail api
from FoldersGmail.GmailAuth import gmail_auth, get_users, get_message_text
#Подключение моделей бд
from main_page.models import Users, Folder,Words
#Подключение формы для сохранения данных
from .forms import *

@cache_page(60 * 15)
def get_emails(request):
    try:
        get_users()
        results = gmail_auth().users().messages().list(userId='me', labelIds=['INBOX']).execute()
        messages = results.get("messages", [])
        content_list = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            def get_message(message_id):
                return gmail_auth().users().messages().get(userId='me', id=message_id, format='full').execute()

            futures = {executor.submit(get_message, message['id']): message for message in messages}
            for future in concurrent.futures.as_completed(futures):
                try:
                    content_list.append(future.result())  # Попытка получить результат из future
                except HttpError as error:
                    print(f"An error occurred while processing email: {error}")

        return render(request, 'email_list.html', {'emails': content_list})

    except HttpError as error:
        print(f"An error occurred while fetching emails: {error}")
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

                    return redirect('folders_work');
                else:
                    Words.objects.create(words=data_form['words'], foldres_id=save_folder.id)
                    return redirect('folders_work');
            else:
                form = AddFormFolder()
                err_mess = "Such a folder already exists!"
                return render(request, 'add_folder.html', {'form': form,'err_mess': err_mess})
    else:
        form = AddFormFolder()
        return render(request, 'add_folder.html', {'form': form})

@cache_page(60 * 15)
def open_folder(request, foldres_id):
    sorted_mess = []
    arr_words = Words.objects.filter(foldres_id=foldres_id)
    results = gmail_auth().users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
    if messages:  # Проверяем, есть ли сообщения
        for message in messages:
            message_id = message['id']  # Берем ID сообщения
            message = gmail_auth().users().messages().get(userId='me', id=message_id).execute()
            message_text = get_message_text(message['id'])
            print(message_text)
            for word in arr_words:
                if word.words in message_text:
                    print(word.words)
                    sorted_mess.append(message_text)
    return render(request, 'view_folder.html', {'sorted_mess': sorted_mess, 'arr_words':arr_words})

def delete_folder(request, folders_id):
    folder = Folder.objects.get(id = folders_id)
    arr_words = Words.objects.filter(foldres_id = folder)
    for word in arr_words:
        word.delete()
    folder.delete()
    return redirect('folders_work');