from django.shortcuts import render

# Create your views here.
def feeds(request):
    user = request.user
    is_authenticated = user.is_authenticated



    return render(request, "posts/feeds.html")