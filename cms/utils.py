from github import Github, Auth
from django.conf import settings

def getRepo():
    auth = Auth.Token(settings.DGTOKEN)
    g = Github(auth=auth)
    user = g.get_user()
    return user.get_repo(settings.BLOG_REPO)

def getFilesinContentFolder():
    repo = getRepo();
    files = repo.get_contents(settings.CONTENT_FOLDER)
    for fil in files:
        print(fil)
    return files

def updateMarkdownFile(slug, fm, content):
    repo = getRepo();
    filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'
    fc = repo.get_contents(filePath)
    full_content = fm + content
    repo.update_file(filePath, "Edit blog post content", full_content, fc.sha)
    return "ok"