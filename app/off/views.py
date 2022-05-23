from django.shortcuts import render

from off.fetcher import ApiConsulter


# Create your views here.
def database(request):
    """Re-init database view"""
    consulter = ApiConsulter()
    consulter.db_save()
    return render(request, "off/database.html")
