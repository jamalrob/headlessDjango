from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
import requests
from pprint import pprint
import base64
from django.conf import settings
import markdown
import frontmatter
from django.shortcuts import redirect
from cms.utils import updateMarkdownFile, getFilesinContentFolder, getRepo


bucket_url = f'{settings.IMG_BUCKET}/tr:w-{settings.IMG_BODY["width"]},q-{settings.IMG_BODY["quality"]}'

def topindex(request):
    if request.user.is_authenticated:
        return redirect("/cms/")
    return redirect("/admin/login/?next=/cms/")

def index(request):
    if request.user.is_authenticated:
        slug = 'the-argument-for-indirect-realism'
        repo = getRepo();
        filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'    
        # [t.strip() for t in data['tags'].split(',')]

        # Use a sanitizer like bleach here
        files = getFilesinContentFolder()
        
        files = list(map(lambda x: x.path.replace('content/', '').replace('.mdx', ''), files))
        template = loader.get_template("chooseFile.html")
        context = {
            'files': files
        }
        return HttpResponse(template.render(context, request))
    return redirect("/admin/login/?next=/cms/")

def save(request, slug):
    if request.user.is_authenticated:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                title = request.POST.get('title', None)
                date = request.POST.get('date', None)
                tags = request.POST.get('tags', None)
                image = request.POST.get('image', None)
                imageClass = request.POST.get('imageClass', None)
                content = request.POST.get('content', None)

                # fm, content = frontmatter.parse(

                # Rebuild the frontmatter
                fmString = (
                    "---"
                    f"\ntitle: '{title}'"
                    f"\ndate: '{date}'"
                    f"\ntags: {tags}"
                    f"\nimage: {image}"
                    f"\nimageClass: {imageClass}"
                    "\n---\n"
                )

                print(fmString)


                # fm, content = frontmatter.parse(fmString)
                #ud = updateMarkdownFile(slug, fmString, content)
                return JsonResponse({'status': 'ok'}, status=200)


                return JsonResponse({'status': 'ok'}, status=200)
            return JsonResponse({'status': 'Invalid request'}, status=400)
        else:
            return HttpResponseBadRequest('Invalid request')
    return redirect("/admin/login/?next=/cms/")


def edit(request, slug):
    if request.user.is_authenticated:
        repo = getRepo();
        filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'    
        file_content = repo.get_contents(filePath)
        txt = file_content.decoded_content.decode()
        data = frontmatter.loads(txt)
        md = markdown.Markdown()
        html = md.convert(data.content.replace('/bucket', bucket_url))

        # NOTE: tags as an array:
        # [t.strip() for t in data['tags'].split(',')]

        # Use a sanitizer like bleach here

        title = data.get("title") or ''
        date = data.get("date") or ''
        tags = data.get("tags") or ''
        image = data.get("image") or ''
        imageClass = data.get("imageClass") or ''
        
        template = loader.get_template("edit.html")
        context = {
            "title": title,
            "date": date,
            "tags": tags,
            "image": image,
            "slug": slug,
            "imageClass": imageClass,
            "md_content": data.content,
            "html": html
        }
        return HttpResponse(template.render(context, request))
    return redirect("/admin/login/?next=/")
