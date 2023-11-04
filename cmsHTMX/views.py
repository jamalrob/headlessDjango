from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from cms.utils import updateMarkdownFile, createMarkdownFile, getFilesinContentFolder, getRepo

def index(request):
    if request.user.is_authenticated:
        #slug = 'the-argument-for-indirect-realism'
        #repo = getRepo();
        #filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'
        # [t.strip() for t in data['tags'].split(',')]
        template = loader.get_template("chooseFileHTMX.html")
        context = {}
        return HttpResponse(template.render(context, request))
    return redirect("/admin/login/?next=/cms/")


def getFiles(request):
    if request.user.is_authenticated:

        # Use a sanitizer like bleach here
        files = getFilesinContentFolder()

        files = list(map(lambda x: x.path.replace('content/', '').replace('.mdx', ''), files))

        context = {
            'files': files
        }
        template = loader.get_template("filesList.html")
        return HttpResponse(template.render(context, request))

        #return JsonResponse({
        #    'files': files
        #}, status=200)