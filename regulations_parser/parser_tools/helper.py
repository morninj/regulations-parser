from parser_tools.models import Regulation, Page, Incorporation
from regulations_parser.settings import DATA_PATH
import pyPdf
import os
import re

def generate_regulation_pages(regulation):
    '''Create a Page object for each page of a given chunk of regulations.

    Chunks are expressed as Regulation objects and passed to this function
    as the regulation keyword argument.
    '''
    pages = []
    # Log request
    with open(DATA_PATH + 'logs/activity.log', 'a') as activity_log:
        activity_log.write('Received request to generate pages for regulation pk=' \
            + str(regulation.pk) + ', media=' + regulation.media + \
            ', filename=' + regulation.filename + '...')
        activity_log.write('\n')
    if regulation.media == 'PDF':
        # Log activity
        with open(DATA_PATH + 'logs/activity.log', 'a') as activity_log:
            activity_log.write('-- Generating PDF pages for regulation pk=' + str(regulation.pk) + ', media=' + regulation.media + '...')
            activity_log.write('\n')
        # Extract PDF pages
        try:
            pdf = pyPdf.PdfFileReader(file(DATA_PATH + regulation.filename, 'rb'))
            if pdf.getIsEncrypted():
                pdf.decrypt('')
            for i in range(0, pdf.getNumPages()):
                this_page = pdf.getPage(i).extractText() + "\n"
                this_page = " ".join(this_page.replace(u"\xa0", " ").strip().split())
                pages.append(this_page.encode("ascii", "xmlcharrefreplace"))
        except Exception, e:
            os.system('echo "' + DATA_PATH + 'logs/error.log" > /var/tmp/parselog')
            with open(DATA_PATH + 'logs/error.log', 'a') as error_log:
                error_log.write(str(e))
                error_log.write('\n')
            return False
    elif regulation.media == 'HTML':
        # Log activity
        with open(DATA_PATH + 'logs/activity.log', 'a') as activity_log:
            activity_log.write('-- Generating HTML page for regulation pk=' + str(regulation.pk) + ', media=' + regulation.media + '...')
            activity_log.write('\n')
        # Extract HTML content
        html_file = open(DATA_PATH + regulation.filename, 'r')
        strip_tags = re.compile(r'<.*?>')
        pages.append(strip_tags.sub('', html_file.read()))
    # Create Page object for each page
    for page_number, page_contents in enumerate(pages):
        try:
            page_contents = unicode(page_contents)
        except UnicodeDecodeError:
            page_contents = unicode(str(page_contents).encode('string_escape'))
        new_page = Page(
            regulation=regulation,
            page_number=(page_number + 1), # Count page numbers from 1, not 0
            contents = page_contents,
        )
        new_page.save()
        # Detect possible instances of incorporation by reference on this page
        generate_incorporations(new_page)

def generate_incorporations(page):
    '''Detect possible instances of incorporation by reference and store
    them as Incorporation objects.
    
    The is_incorporation attribute of Incorporation objects indicates whether
    or not they are, in fact, instance of incorporation by reference. This
    script uses loose search parameters and is bound to generate quite a few
    false positives. When these instances are reviewed by hand, the reviewer
    will mark them as "yes" (is_incorporation=True) or "no"
    (is_incorporation=False).
    '''
    pattern = re.compile(r'(?i)standard|(?i)incorporat')
    for match in re.finditer(pattern, page.contents):
        context_start_position = match.start() - 200
        context_end_position = match.end() + 200
        context = page.contents[context_start_position:context_end_position]
    
        new_incorporation = Incorporation(
            page=page,
            context=context,
            context_start_position=context_start_position,
            context_end_position=context_end_position
        )
        new_incorporation.save()
