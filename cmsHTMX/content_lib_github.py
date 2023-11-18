from github import Github, Auth
from slugify import slugify
import os

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
    auth = Auth.Token(os.getenv("DGTOKEN"))
    g = Github(auth=auth)
    user = g.get_user()
    return user.get_repo(os.getenv("BLOG_REPO"))

def getFilesinContentFolder():
    repo = getRepo()
    return repo.get_contents(os.getenv("CONTENT_FOLDER"))

def getFileContent(filePath):
    repo = getRepo()
    return repo.get_contents(filePath)

def updateMarkdownFile(slug, fm, content):
    filePath = f'{os.getenv("CONTENT_FOLDER")}/{slug}.mdx'
    full_content = fm + content
    repo = getRepo()
    fc = repo.get_contents(filePath)
    return repo.update_file(filePath, "Edit blog post content", full_content, fc.sha)

def createMarkdownFile(slug, fm, content):
    filePath = f'{os.getenv("CONTENT_FOLDER")}/{slug}.mdx'
    full_content = fm + content
    repo = getRepo()
    return repo.create_file(filePath, "New blog post", full_content)