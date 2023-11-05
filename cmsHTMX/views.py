from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from cms.utils import updateMarkdownFile, createMarkdownFile, getFilesinContentFolder, getRepo
from django.conf import settings
import markdown
import frontmatter
import openai
from slugify import slugify

bucket_url = f'{settings.IMG_BUCKET}/tr:w-{settings.IMG_BODY["width"]},q-{settings.IMG_BODY["quality"]}'

def cmshtmx_index(request):
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


def get_suggestion(request):
    if request.user.is_authenticated:
        openai.api_key = settings.AI_SECRET_KEY

        content_to_fix = request.POST.get('content_to_fix')
        setup = """ You are a blog writer's personal editor, and
                    your job is to offer suggestions for improvement,
                    given content written by the user (writer)."""

        #content = "There once was a green large lake at the bottom of my garden but now it's gone and I be unsure exakerly why."
        content = f'Here is an excerpt from my latest article: { content_to_fix }'

        suggestion = "Lorem Ipsum is simply dummy\n\n text of the printing\n\n and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,\n\n when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

        #completion = openai.ChatCompletion.create(
        #    model="gpt-3.5-turbo",
        #    #model="gpt-4", # No access till I pay
        #    messages=[
        #        {"role": "system", "content": setup},
        #        {"role": "user", "content": content}
        #    ]
        #)
        #suggestion = completion.choices[0].message.content

        context = {
            'original': content,
            'answer': suggestion.replace("\n","<br />")
        }
        template = loader.get_template("suggestion.html")
        return HttpResponse(template.render(context, request))


def save(request, slug=''):
    if request.user.is_authenticated:
        if request.method == 'POST':

            CHECKBOX_MAPPING = {'on': 'true', 'off': 'false'}

            title = request.POST.get('title', '')
            date = request.POST.get('date', '')
            tags = request.POST.get('tags', '')
            image = CHECKBOX_MAPPING.get(request.POST.get('image'), '')
            imageClass = request.POST.get('imageClass', '')
            content = request.POST.get('content', '')
            draft = request.POST.get('draft', '')

            # fm, content = frontmatter.parse(

            # Rebuild the frontmatter
            fmString = (
                "---"
                f"\ntitle: '{title}'"
                f"\ndate: '{date}'"
                f"\ntags: {tags}"
                f"\nimage: {image}"
                f"\nimageClass: {imageClass}"
                f"\ndraft: {draft}"
                "\n---\n"
            )

            result = {}
            if slug:
                result = updateMarkdownFile(slug, fmString, content)
                return JsonResponse({
                    'status': 'updated',
                    'slug': slug,
                    'host': settings.HOST
                    }, status=200)
            else:
                slug = slugify(title)
                result = createMarkdownFile(slug, fmString, content)
                # RETURNS e.g..
                # {'content': ContentFile(path="content/a-test-title-2.mdx"), 'commit': Commit(sha="57ef9705105d18a3554c6a15d39bf6fe5c428b38")}
                return JsonResponse({
                    'status': 'created',
                    'slug': slug,
                    'host': settings.HOST
                    }, status=200)


            return JsonResponse({'status': 'Invalid request'}, status=400)

        return HttpResponseBadRequest('Invalid request')
    return redirect("/admin/login/?next=/cms/")