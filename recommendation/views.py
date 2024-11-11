from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .services import get_user_recommendations
from django.shortcuts import render

#from django.views.decorators.cache import cache_page

#@cache_page(60*15) #cache view for 15 minutes
def recommendation_view(request, user_id):
    recommendations = get_user_recommendations(user_id)
    return JsonResponse(recommendations, safe=False, json_dumps_params={'indent': 4})

def home(request):
    return render(request, 'home.html')
