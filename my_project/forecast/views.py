from django.shortcuts import render


def main(request):
    return render(request, 'main.html', context={})


def statistic(request):
    return render(request, 'main.html', context={})


def about(request):
    return render(request, 'main.html', context={})
