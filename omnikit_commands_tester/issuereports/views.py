from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.views.generic.edit import CreateView
# from django.urls import reverse_lazy
# from django.contrib.staticfiles.templatetags.staticfiles import static

# from omnikit_commands_tester.issuereports.models import Document
# from django.views import generic
from omnikit_commands_tester.issuereports.temp_basal_tester import extractor


# class DocumentCreateView(CreateView):
#     model = Document
#     fields = ['upload', ]
#     success_url = reverse_lazy('uploads')
#     doc_created = Document.objects.last()
#     if doc_created:
#         print(doc_created)
#         print(doc_created.upload)
#         print(doc_created)
#         url = static("{}".format(doc_created.upload))
#         print(url)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         documents = Document.objects.all()
#         context['documents'] = documents
#         return context


# class DocumentDetailView(generic.DetailView):
#     model = Document

#     fields = ['upload', ]


def tempbasal_tester(request):
    if request.method == 'POST':
        file1 = request.FILES['myfile']
        # contentOfFile = file1.read()
        contentOfFile = extractor(file1)
        if file1:
            return render(request, 'testers.html', {'file': file1, 'contentOfFile': contentOfFile})
    else:
        return render(request, 'testers.html', {'file': None, 'contentOfFile':None})
