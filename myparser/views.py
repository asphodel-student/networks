from django.http import HttpResponse, FileResponse
from django.shortcuts import render
import os
from django.conf import settings

from . import littleparser

def form_view(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        path_to_data = littleparser.parse_this_page(link)
        file_path = os.path.join(settings.MEDIA_ROOT, path_to_data)
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        return response
    else:
        return render(request, 'form.html')
    