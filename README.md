Regulations Parser
==================

Legal documents often incorporate secondary legal material--a practice known as [incorporation by reference](http://en.wikipedia.org/wiki/Incorporation_by_reference). The incorporated material carries the force of law, but it is not always accessible to the reader of the original document.

This app helps define the links between legal texts. It includes tools for:

* Scraping primary legal materials from the web,
* Organizing them sensibly,
* Automatically detecting instances of incorporation by reference, and
* Efficiently reviewing possible matches by hand.

I built this toolkit to parse the Code of Massachusetts Regulations to find incorporations of third-party standards. It could be easily adapted to work on other regulations or similar documents. I'd love help from other developers to make these tools useful for more general purposes.

I worked on this project with the support of a generous fellowship from [Public.Resource.Org](http://public.resource.org/).

Configuration
-------------

Clone this repository.

Install dependencies:

    $ pip install -r requirements.txt

Set DATA_PATH in regulations_parser/regulations_parser/setttings.py.

Create the database:
    
    $ cd regulations_parser
    $ python manage.py syncdb
    $ python manage.py migrate parser_tools

Run the development server:

    $ cd regulations_parser
    $ python manage.py runserver

Navigate to http://127.0.0.1:8000/

pyPdf bugs
---------

### "multiple definitions in dictionary"

Edit the code in `lib/python2.7/site-packages/pyPdf/generic.py`
after line 532 to match: 

    if data.has_key(key):
        # multiple definitions of key not permitted
        pass
        # raise utils.PdfReadError, "multiple definitions in dictionary"
    else:
        data[key] = value

Source: https://bugs.launchpad.net/pypdf/+bug/242755

### "unsupported filter /LZWDecode"

Replace `lib/python2.7/site-packages/pyPdf/filters.py` with http://vaitls.com/treas/pdf/pyPdf/filters.py.

Source: http://stackoverflow.com/a/6572422/593956

### "file has not been decrypted"

I encountered this problem when attempting to parse PDFs scraped from [527 CMR](http://www.lawlib.state.ma.us/source/mass/cmr/527cmr.html).
It can be fixed by decrypting the file with an empty string:

    if pdf.getIsEncrypted():
        pdf.decrypt('')

Source: https://bugs.launchpad.net/pypdf/+bug/355479
