from django.shortcuts import render
from omnikit_commands_tester.testers.temp_basal_tester import extractor

#extractor(file1)
def tempbasal_tester(request):
    if request.method == 'POST':
        file1 = request.FILES['myfile']
            #contentOfFile = file1.read()
        contentOfFile = extractor(file1)
        if file1:
            return render(request, 'testers.html', {'file': file1, 'contentOfFile': contentOfFile})
    else:
        return render(request, 'testers.html', {'file': None, 'contentOfFile':None})
