from github import Github, Auth
from slugify import slugify

class DocumentStore:

    def __init__(self, content_folder, dgtoken, repo_name):
        auth = Auth.Token(dgtoken)
        g = Github(auth=auth)
        user = g.get_user()
        self.__repo = user.get_repo(repo_name)
        self.__content_folder = content_folder

    def build_content(self, request, draft):
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

    def updateOrCreate(self, post, slug):
        result = ""
        if slug:
            if self.__updateMarkdownFile(slug, post.get("fmString"), post.get("content")):
                result = '<span class="status">UPDATED</span>'
        else:
            if self.__createMarkdownFile(slugify(post.get("title")), post.get("fmString"), post.get("content")):
                result = '<span class="status">CREATED</span>'
        return result

    def getFilesinContentFolder(self):
        return self.__repo.get_contents(self.__content_folder)

    def getFileContent(self, filePath):
        return self.__repo.get_contents(filePath)

    def __updateMarkdownFile(self, slug, fm, content):
        filePath = f'{self.__content_folder}/{slug}.mdx'
        full_content = fm + content
        fc = self.__repo.get_contents(filePath)
        return self.__repo.update_file(filePath, "Edit blog post content", full_content, fc.sha)

    def __createMarkdownFile(self, slug, fm, content):
        filePath = f'{self.__content_folder}/{slug}.mdx'
        full_content = fm + content
        return self.__repo.create_file(filePath, "New blog post", full_content)