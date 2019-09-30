from django.http import HttpResponse


def index(request):
    return HttpResponse("<Response><Say voice = 'woman' language = 'en-us'>We did not get any digits from you</Say></Response>")