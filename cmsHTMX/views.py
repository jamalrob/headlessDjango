from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from cms.utils import updateMarkdownFile, createMarkdownFile, getFilesinContentFolder, getRepo
from django.conf import settings
import markdown
import frontmatter

bucket_url = f'{settings.IMG_BUCKET}/tr:w-{settings.IMG_BODY["width"]},q-{settings.IMG_BODY["quality"]}'

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


def get_files(request):
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


def get_post(request, slug):
    if request.user.is_authenticated:

        repo = getRepo();
        data = {}
        md_as_html = ''
        md_content = ''
        if slug:
            filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'
            file_content = repo.get_contents(filePath)
            txt = file_content.decoded_content.decode()
            data = frontmatter.loads(txt)
            md = markdown.Markdown()
            md_as_html = md.convert(data.content.replace('/bucket', bucket_url))
            md_content = data.content

            # NOTE: tags as an array:
            # [t.strip() for t in data['tags'].split(',')]


        # Use a sanitizer like bleach here

        title = data.get("title") or ''
        date = data.get("date") or ''
        tags = data.get("tags") or ''
        image = data.get("image") or 'false'
        if image == True:
            image = 'true'
        imageClass = data.get("imageClass") or ''
        html = md_as_html or ''

        template = loader.get_template("edit.html")
        context = {
            "title": title,
            "date": date,
            "tags": tags,
            "image": image,
            "slug": slug,
            "imageClass": imageClass,
            "md_content": md_content,
            "imagekit_bucket": settings.IMG_BUCKET,
            "html": html,
            'host': settings.HOST
        }
        template = loader.get_template("editHTMX.html")
        return HttpResponse(template.render(context, request))