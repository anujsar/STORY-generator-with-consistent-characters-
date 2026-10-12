import os
from ebooklib import epub

def create_epub_file(title: str, author: str, chapters: list, output_filename: str) -> str:
    """
    Compiles generated story chapters into a formatted .epub eBook.
    """
    book = epub.EpubBook()

    # Metadata Setup
    book.set_identifier("story_gen_" + title.lower().replace(" ", "_"))
    book.set_title(title)
    book.set_language("en")
    book.add_author(author if author.strip() else "AI Story Generator")

    epub_chapters = []

    # Build EPUB HTML content for each chapter
    for ch in chapters:
        c_num = ch["chapter_num"]
        c_title = f"Chapter {c_num}"
        c_file_name = f"chap_{c_num}.xhtml"

        chapter_item = epub.EpubHtml(title=c_title, file_name=c_file_name, lang="en")
        
        # Convert plain text line breaks to HTML paragraphs
        paragraphs = ch["text"].split("\n")
        html_body = f"<h1>{c_title}</h1>"
        for p in paragraphs:
            if p.strip():
                html_body += f"<p>{p.strip()}</p>"

        chapter_item.set_content(html_body)
        book.add_item(chapter_item)
        epub_chapters.append(chapter_item)

    # Table of Contents and Navigation Setup
    book.toc = tuple(epub_chapters)
    book.add_item(epub.EpubNCX())
    book.add_item(epub.EpubNav())

    # Styling
    style = 'BODY { font-family: Georgia, serif; line-height: 1.5; } h1 { text-align: center; margin-bottom: 1.5em; } p { margin-bottom: 1em; text-indent: 1em; }'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    book.spine = ["nav"] + epub_chapters

    # Ensure output path exists
    output_path = os.path.join("outputs", output_filename)
    os.makedirs("outputs", exist_ok=True)

    # Save EPUB
    epub.write_epub(output_path, book, {})
    return output_path