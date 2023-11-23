A headless CMS using **Django, HTMX, and Hyperscript**, built primarily as a way of learning the latter two and demonstrating reactive interfaces without the use of JavaScript frameworks or hand-written JavaScript code. Currently it's coupled with my actual blog, which is a **Next.js** static site: https://github.com/jamalrob/blog.alistairrobinson.me.

The project achieves the following:
- Integration of Django templating with **HTMX and Hyperscript**--only a tiny amount of JavaScript
- Editing of the blog's mdx files, accessed via the **Github API**
- Client-side **active search** by slug name
- Markdown editor with live preview
- Use of partial templates to allow HTMX to request small chunks of HTML (not JSON) from Django
- Suggested improvements via **GPT API**
- **Locality of Behaviour**: "The behaviour of a unit of code should be as obvious as possible by looking only at that unit of code"
    - Inline script: fully inline in the HTML elements where possible
    - Or in script tags within the same server template
    - Inline CSS in style tags, emulating the CSS isolation in Svelte components
    - Effectively:
        - DRY, separation of concerns, and modularization in Django
        - But locality of behaviour, with inline code and styles, on the front-end

Separately, there is a Github webhook implemented with a Flask endpoint separate from the CMS itself. It pulls the code and restarts the application when code is pushed to this repository. See https://github.com/jamalrob/ghook.