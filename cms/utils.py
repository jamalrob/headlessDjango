from github import Github, Auth
from django.conf import settings
from slugify import slugify

def build_content(request, draft):

    CHECKBOX_MAPPING = {'on': 'true', 'off': 'false'}
    content = request.POST.get('content', '')
    title = request.POST.get('title', '')
    if draft or draft == 'true':
        draft = 'true'
    else:
        draft = 'false'


    fmString = (
        "---"
        f"\ntitle: '{title}'"
        f"\ndate: '{request.POST.get('date', '')}'"
        f"\ntags: {request.POST.get('tags', '')}"
        f"\nimage: {CHECKBOX_MAPPING.get(request.POST.get('image'), '')}"
        f"\nimageClass: {request.POST.get('imageClass', '')}"
        f"\ndraft: {draft}"
        "\n---\n"
    )

    return {
        "fmString": fmString,
        "content": content,
        "title": title
    }

def updateOrCreate(post, slug):
    result = ""
    if slug:
        if updateMarkdownFile(slug, post.get("fmString"), post.get("content")):
            result = '<span class="status">UPDATED</span>'
    else:
        if createMarkdownFile(slugify(post.get("title")), post.get("fmString"), post.get("content")):
            result = '<span class="status">CREATED</span>'
    return result

def getRepo():
    auth = Auth.Token(settings.DGTOKEN)
    g = Github(auth=auth)
    user = g.get_user()
    return user.get_repo(settings.BLOG_REPO)

def getFilesinContentFolder():
    repo = getRepo();
    return repo.get_contents(settings.CONTENT_FOLDER)

def updateMarkdownFile(slug, fm, content):
    filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'
    full_content = fm + content
    repo = getRepo();
    fc = repo.get_contents(filePath)
    return repo.update_file(filePath, "Edit blog post content", full_content, fc.sha)

    # RETURNS e.g..
    # {'content': ContentFile(path="content/a-test-title-2.mdx"), 'commit': Commit(sha="57ef9705105d18a3554c6a15d39bf6fe5c428b38")}

def createMarkdownFile(slug, fm, content):
    filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'
    full_content = fm + content
    repo = getRepo();
    return repo.create_file(filePath, "New blog post", full_content)

    # RETURNS e.g..
    # {'content': ContentFile(path="content/a-test-title-2.mdx"), 'commit': Commit(sha="57ef9705105d18a3554c6a15d39bf6fe5c428b38")}