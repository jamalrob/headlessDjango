from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from cmsHTMX.document_store import DocumentStore
from django.conf import settings
import markdown
import frontmatter
import openai
from django.contrib.auth.decorators import login_required

BUCKET_URL = f'{settings.IMG_BUCKET}/tr:w-{settings.IMG_BODY["width"]},q-{settings.IMG_BODY["quality"]}'
CONTENT_FOLDER = settings.CONTENT_FOLDER
DGTOKEN = settings.DGTOKEN
REPO_NAME = settings.BLOG_REPO

@login_required
def cmshtmx_index(request):
    if 'cmshtmx' not in request.path:
        return redirect("/cmshtmx/")
    template = loader.get_template("chooseFileHTMX.html")
    context = {}
    return HttpResponse(template.render(context, request))


@login_required
def get_files(request):
    ds = DocumentStore(CONTENT_FOLDER, DGTOKEN, REPO_NAME)
    files = ds.getFilesinContentFolder()
    files = list(map(lambda x: x.path.replace('content/', '').replace('.mdx', ''), files))
    context = {
        'files': files
    }
    template = loader.get_template("_filesList.html")
    return HttpResponse(template.render(context, request))


@login_required
def get_post(request, slug=''):
    data = {}
    md_as_html = ''
    md_content = ''
    ds = DocumentStore(CONTENT_FOLDER, DGTOKEN, REPO_NAME)
    if slug:
        filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'
        txt = ds.getFileContent(filePath).decoded_content.decode()
        data = frontmatter.loads(txt)
        md = markdown.Markdown()
        md_as_html = md.convert(data.content.replace('/bucket', BUCKET_URL))
        md_content = data.content

    title = data.get("title") or ''
    date = data.get("date") or ''
    tags = data.get("tags") or ''

    draft = True
    if data.get("draft") in ['false', '', False, None]:
        draft = False

    image = True
    if data.get("image") in ['false', '', False, None]:
        image = False

    imageClass = data.get("imageClass") or ''

    post = {
        "title": title,
        "date": date,
        "tags": tags,
        "image": image,
        "draft": draft,
        "slug": slug,
        "imageClass": imageClass,
        "md_content": md_content,
        "html": md_as_html or '',
    }

    context = {
        "post": post,
        "imagekit_bucket": settings.IMG_BUCKET,
    }
    template = loader.get_template("editHTMX.html")
    return HttpResponse(template.render(context, request))

@login_required
def get_suggestion(request):
    openai.api_key = settings.AI_SECRET_KEY

    content_to_fix = request.POST.get('content_to_fix')
    setup = """ You are a blog writer's personal editor, and
                your job is to offer suggestions for improvement,
                given content written by the user (writer)."""

    # TESTING
    # content = "There once was a green large lake at the bottom of my garden but now it's gone and I be unsure exakerly why."

    # REAL
    content = f'Here is an excerpt from my latest article: { content_to_fix }'

    # TESTING
    #suggestion = "Lorem Ipsum is simply dummy\n\n text of the printing\n\n and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,\n\n when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

    # REAL
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": setup},
            {"role": "user", "content": content}
        ]
    )
    suggestion = completion.choices[0].message.content

    # TESTING
    #import time
    #time.sleep(2)

    context = {
        'original': content_to_fix,
        'answer': suggestion.replace("\n","<br />")
    }
    template = loader.get_template("_suggestion.html")
    return HttpResponse(template.render(context, request))


@login_required
def publish(request):
    slug = request.POST.get('slug', '')
    ds = DocumentStore(CONTENT_FOLDER, DGTOKEN, REPO_NAME)
    post = ds.build_content(request, draft=False)
    return HttpResponse(ds.updateOrCreate(post, slug))


@login_required
def save_draft(request):
    """ Unpublishes existing posts as well as saving new drafts,
        since all it does it build the content and frontmatter with draft=True
    """
    slug = request.POST.get('slug', '')
    ds = DocumentStore(CONTENT_FOLDER, DGTOKEN, REPO_NAME)
    post = ds.build_content(request, draft=True)
    return HttpResponse(ds.updateOrCreate(post, slug))