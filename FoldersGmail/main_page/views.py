from django.shortcuts import render



def main(request):
    return render(request, 'main.html')

def info(request):
    return  render(request, 'info.html')
