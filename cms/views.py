from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
import requests
from pprint import pprint
import base64
from github import Github, Auth
from django.conf import settings
import markdown
import frontmatter

bucket_url = f'{settings.IMG_BUCKET}/tr:w-{settings.IMG_BODY["width"]},q-{settings.IMG_BODY["quality"]}'

def getRepo():
    auth = Auth.Token(settings.DGTOKEN)
    g = Github(auth=auth)
    user = g.get_user()
    return user.get_repo(settings.BLOG_REPO)

def updateMarkdownFile(slug, fm, content):
    repo = getRepo();
    filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'
    fc = repo.get_contents(filePath)
    full_content = fm + content
    repo.update_file(filePath, "Edit blog post content", full_content, fc.sha)
    return "ok"
        

def save(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            title = request.POST.get('title', None)
            date = request.POST.get('date', None)
            tags = request.POST.get('tags', None)
            content = request.POST.get('content', None)

            slug = 'the-argument-for-indirect-realism'

            # fm, content = frontmatter.parse(

            # Rebuild the frontmatter
            fmString = (
                "---"
                f"\ntitle: '{title}'"
                f"\ndate: '{date}'"
                f"\ntags: {tags}"
                "\n---\n"
            )

            # fm, content = frontmatter.parse(fmString)
            #print(fm)
            #print(content)

            ud = updateMarkdownFile(slug, fmString, content)
            return JsonResponse({'status': 'ok'}, status=200)


            return JsonResponse({'status': 'ok'}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

def index(request):

    slug = 'the-argument-for-indirect-realism'
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
    
    template = loader.get_template("index.html")
    context = {
        "title": data["title"],
        "date": data["date"],
        "tags": data['tags'],
        "md_content": data.content,
        "html": html
    }
    return HttpResponse(template.render(context, request))


def login(request):

    return HttpResponse()
