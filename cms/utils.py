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
    filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'
    repo = getRepo();
    fc = repo.get_contents(filePath)
    full_content = fm + content

    # RETURNS e.g..
    # {'content': ContentFile(path="content/a-test-title-2.mdx"), 'commit': Commit(sha="57ef9705105d18a3554c6a15d39bf6fe5c428b38")}
    return repo.update_file(filePath, "Edit blog post content", full_content, fc.sha)

def createMarkdownFile(slug, fm, content):
    filePath = f'{settings.CONTENT_FOLDER}/{slug}.mdx'
    full_content = fm + content
    
    repo = getRepo();

    # RETURNS e.g..
    # {'content': ContentFile(path="content/a-test-title-2.mdx"), 'commit': Commit(sha="57ef9705105d18a3554c6a15d39bf6fe5c428b38")}    
    return repo.create_file(filePath, "New blog post", full_content)