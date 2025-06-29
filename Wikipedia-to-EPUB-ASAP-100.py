import re
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import wikipediaapi
from ebooklib import epub

version = '1.00'

def sanitize_filename(name):
    # sanitize the filename: lowercase, replace spaces with underscores, remove invalid chars
    name = name.lower()
    name = re.sub(r'\s+', '_', name)  # replace spaces with underscore
    name = re.sub(r'[^a-z0-9_\-]', '', name)  # keep only letters, numbers, underscores, and dashes
    return name

def create_cover(title):
    # create a simple cover image with the title text centered
    img = Image.new('RGB', (600, 800), color='white')  # create white image 600x800 px
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # try to use arial font size 40
    except:
        font = ImageFont.load_default()  # fallback to default font if arial not found
    d.text((50, 350), title, fill='black', font=font)  # draw title text on image
    output = BytesIO()
    img.save(output, format='JPEG')  # save image to bytes buffer as jpeg
    return output.getvalue()

def fetch_sections(page, level=2, file_counter=None):
    # recursively fetch page sections and subsections up to level 5
    # return a list of tuples (epub chapter object, section object, level)
    if file_counter is None:
        file_counter = {'count': 0}  # counter dict to track unique filenames and uids

    chapters = []
    for section in page.sections:
        title = section.title.strip()
        content = section.text.strip()
        if not content:
            continue  # skip empty sections

        file_counter['count'] += 1
        filename = f"{sanitize_filename(title)}_{file_counter['count']}.xhtml"  # unique filename
        uid = f"chapter_{file_counter['count']}"  # unique id for epub

        chapter = epub.EpubHtml(
            uid=uid,
            title=title,
            file_name=filename,
            lang='en'
        )
        # create html content with section title as header and text paragraphs
        html_content = f"<h{level}>{title}</h{level}><p>{content.replace(chr(10), '<br/>')}</p>"
        chapter.content = html_content
        chapters.append((chapter, section, level))

        # recursive call to get subsections increasing the header level, max 5
        chapters.extend(fetch_sections(section, level=min(level + 1, 5), file_counter=file_counter))
    return chapters

def build_epub(title, page):
    # build an epub book from a wikipedia page and its sections
    book = epub.EpubBook()
    book.set_identifier(sanitize_filename(title))  # unique identifier from title
    book.set_title(title)  # set book title
    book.set_language('en')  # set language
    book.add_author("Wikipedia")  # author as wikipedia

    safe_title = sanitize_filename(title)

    # create and set cover image for epub
    cover_data = create_cover(title)
    book.set_cover("cover.jpg", cover_data)

    # css styling for the epub content
    style = '''
    body { font-family: serif; line-height: 1.4; padding: 1em; }
    h1, h2, h3, h4, h5 { margin-top: 1.5em; }
    p { margin-bottom: 1em; }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # create the introduction page with page summary
    intro_file = "intro_1.xhtml"
    intro_uid = "intro_1"
    intro = epub.EpubHtml(title=title, file_name=intro_file, lang='en', uid=intro_uid)
    intro.content = f"<h1>{title}</h1><p>{page.summary.replace(chr(10), '<br/>')}</p>"
    intro.add_item(nav_css)

    # fetch all sections recursively as chapters
    chapters = fetch_sections(page)
    chapter_objs = [c[0] for c in chapters]

    # add all chapters to the book and add css
    for chapter in chapter_objs:
        chapter.add_item(nav_css)
        book.add_item(chapter)

    # add the intro page once after all chapters
    book.add_item(intro)

    # add navigation and table of contents files
    book.add_item(epub.EpubNav())
    book.add_item(epub.EpubNcx())

    # set table of contents and spine order without duplicates
    if chapter_objs:
        book.toc = [epub.Section(title)] + chapter_objs
        book.spine = ['nav', intro] + chapter_objs
    else:
        book.toc = [intro]
        book.spine = ['nav', intro]

    filename = f"{safe_title}.epub"
    epub.write_epub(filename, book, {})  # write the epub file to disk
    print(f"✅ epub created: {filename}")

def main():
    # initialize wikipedia api with user agent (required by wikipedia)
    wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent='WikiToEPUB/1.0 (python script)'
    )

    # read wikipedia page URLs from file wiki.txt (one per line)
    with open("wiki.txt", "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    # iterate over links, build epub for each existing page
    for url in links:
        title = url.split('/')[-1]
        page = wiki.page(title)
        if not page.exists():
            print(f"⚠️ page not found: {title}")
            continue
        build_epub(title, page)

if __name__ == "__main__":
    main()



