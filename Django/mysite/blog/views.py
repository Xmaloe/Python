from django.http import HttpResponse

def post_view(request):
    return HttpResponse("Hello World")