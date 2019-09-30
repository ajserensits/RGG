from django.http import HttpResponse


def index(request):
#    param = request.GET.get('var')
    return HttpResponse("<Response><Say voice = 'woman' language = 'en-us'>We are on Python</Say></Response>" , content_type="application/xml")