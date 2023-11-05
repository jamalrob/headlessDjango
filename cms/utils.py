from github import Github, Auth
from django.conf import settings


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