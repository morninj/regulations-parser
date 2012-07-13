from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from parser_tools.forms import ScrapeForm, IncorporationForm, \
    StandardsOrganizationForm, RegulationForm
from parser_tools.models import Regulation, Page, Incorporation, \
    StandardsOrganization
import os
import re
from regulations_parser.settings import DATA_PATH
import collections
from parser_tools.helper import generate_regulation_pages
from django.forms.models import model_to_dict
import forms
from django.shortcuts import redirect
import csv

def index(request):
    matched_incorporations = Incorporation.objects.filter(is_incorporation=True)
    return render_to_response('parser_tools/index.html', {'matched_incorporations': \
        matched_incorporations})

def flush(request):
    do_flush = False
    if request.GET.get('do_flush') == 'yes':
        do_flush = True
        if 'regulations_parser' in DATA_PATH:
            os.system('rm -rf ' + DATA_PATH + '*')
        Regulation.objects.all().delete()
        Page.objects.all().delete()
        Incorporation.objects.all().delete()
    return render_to_response('parser_tools/flush.html',
        {'do_flush': do_flush})

def review(request):
    regulations_list = Regulation.objects.all().order_by('parent_title', 'title')
    return render_to_response('parser_tools/review.html',
                              {
                                'regulations_list': regulations_list
                              })

def edit_incorporation(request, pk=None):
    '''Edit an Incorporation object.
    
    This is the primary interface for reviewing possible instances
    of incorporation by reference. If no primary key is specified,
    the form will display the next unreviewed instance.
    '''
    
    if pk is None:
        incorporation = Incorporation.objects.filter(is_incorporation=None)[0]
    else:
        incorporation = get_object_or_404(Incorporation, pk=pk)
    form = IncorporationForm(instance=incorporation)
    # Ignore if context matches known key phrases
    ignore = False
    if 'standards of assistance' in incorporation.context.lower(): ignore = True
    if 'timeliness standards' in incorporation.context.lower(): ignore = True
    if 'evidence standard' in incorporation.context.lower(): ignore = True
    if 'budget standard' in incorporation.context.lower(): ignore = True
    if 'standard adjudicatory' in incorporation.context.lower(): ignore = True
    if 'evidentiary standards' in incorporation.context.lower(): ignore = True
    if 'standard payment' in incorporation.context.lower(): ignore = True
    if 'standard deviation' in incorporation.context.lower(): ignore = True
    if 'efficiency standard' in incorporation.context.lower(): ignore = True
    if 'cost standard' in incorporation.context.lower(): ignore = True
    if 'standard of review' in incorporation.context.lower(): ignore = True
    if 'standard mattress length' in incorporation.context.lower(): ignore = True
    if 'standard seat' in incorporation.context.lower(): ignore = True
    if 'standard remote joystick' in incorporation.context.lower(): ignore = True
    if 'non-standard' in incorporation.context.lower(): ignore = True
    if 'backbench standard preparation' in incorporation.context.lower(): ignore = True
    if 'masshealth standard' in incorporation.context.lower(): ignore = True
    if 'standard of assistance' in incorporation.context.lower(): ignore = True
    if 'standard hemi' in incorporation.context.lower(): ignore = True
    if 'director of standards' in incorporation.context.lower(): ignore = True
    if 'standard benefits plan' in incorporation.context.lower(): ignore = True
    if ': Standard' in incorporation.context: ignore = True
    if 'loss ratio standard' in incorporation.context.lower(): ignore = True
    if 'pre-standardized plans' in incorporation.context.lower(): ignore = True
    if 'incorporated org' in incorporation.context.lower(): ignore = True
    if 'articles of incorp' in incorporation.context.lower(): ignore = True
    if 'standard offer generation' in incorporation.context.lower(): ignore = True
    if 'standard operating proce' in incorporation.context.lower(): ignore = True
    if 'mfs standards' in incorporation.context.lower(): ignore = True
    if 'carve-out minimum standard' in incorporation.context.lower(): ignore = True
    if incorporation.page.regulation.parent_title == '248 CMR': ignore = True
    if 'standard industrial classification' in incorporation.context.lower(): ignore = True
    if 'standards set forth in 3' in incorporation.context.lower(): ignore = True
    if 'standards set forth in 4' in incorporation.context.lower(): ignore = True
    if 'standards set forth in 5' in incorporation.context.lower(): ignore = True
    if 'standards set forth in 6' in incorporation.context.lower(): ignore = True
    if 'standards set forth in 7' in incorporation.context.lower(): ignore = True
    if 'standards set forth in 8' in incorporation.context.lower(): ignore = True
    if 'standards set forth in 9' in incorporation.context.lower(): ignore = True
    if 'standard set forth in 6' in incorporation.context.lower(): ignore = True
    if 'standards and procedures of 7' in incorporation.context.lower(): ignore = True
    if 'standard units' in incorporation.context.lower(): ignore = True
    if 'standard written notification' in incorporation.context.lower(): ignore = True
    if 'standard and poor' in incorporation.context.lower(): ignore = True
    if 'standard &amp; poor' in incorporation.context.lower(): ignore = True
    if 'standards can be used to direct conservation' in incorporation.context.lower(): ignore = True
    if 'unincorporated' in incorporation.context.lower(): ignore = True
    if 'substandard' in incorporation.context.lower(): ignore = True
    if 'sub-standard' in incorporation.context.lower(): ignore = True
    if 'standard form' in incorporation.context.lower(): ignore = True
    if 'wage standards' in incorporation.context.lower(): ignore = True
    if 'apprentice standards' in incorporation.context.lower(): ignore = True
    if 'professional standards for admin' in incorporation.context.lower(): ignore = True
    if 'standardized test' in incorporation.context.lower(): ignore = True
    if 'performance standard' in incorporation.context.lower(): ignore = True
    if 'high standards' in incorporation.context.lower(): ignore = True
    if 'standards for vocational' in incorporation.context.lower(): ignore = True
    if 'Standards.' in incorporation.context: ignore = True
    if 'standards of behavior' in incorporation.context.lower(): ignore = True
    if 'standard certificate' in incorporation.context.lower(): ignore = True
    if 'standards for abe' in incorporation.context.lower(): ignore = True
    if 'poverty level standard' in incorporation.context.lower(): ignore = True
    if 'standard contract form' in incorporation.context.lower(): ignore = True
    if 'standards of decorum' in incorporation.context.lower(): ignore = True
    if 'standard contractor eval' in incorporation.context.lower(): ignore = True
    if 'standard soq' in incorporation.context.lower(): ignore = True
    if 'standard prequal' in incorporation.context.lower(): ignore = True
    if 'not incorpor' in incorporation.context.lower(): ignore = True
    if 'standards of conduct' in incorporation.context.lower(): ignore = True
    if 'aesthetic standard' in incorporation.context.lower(): ignore = True
    if 'standards for the protection of' in incorporation.context.lower(): ignore = True
    if 'standard of care' in incorporation.context.lower(): ignore = True
    if 'incorporator' in incorporation.context.lower(): ignore = True
    if 'standard size paper' in incorporation.context.lower(): ignore = True
    if 'standards and guidelines' in incorporation.context.lower(): ignore = True
    if 'standard contract' in incorporation.context.lower(): ignore = True
    # Highlight our keywords
    pattern = re.compile(r'(?i)standard|(?i)incorporat')
    keyword_start = 0
    keyword_end = 0
    for match in re.finditer(pattern, incorporation.context):
        keyword_start = match.start()
        keyword_end = match.end()
    highlighted_context = incorporation.context[:keyword_start]
    highlighted_context = highlighted_context + '<span style="background-color: #fc0;">'
    highlighted_context = highlighted_context + incorporation.context[keyword_start:keyword_end]
    highlighted_context = highlighted_context + '</span>'
    highlighted_context = highlighted_context + incorporation.context[keyword_end:]
    # Print this incorporation's context in bold within the page full text
    page = incorporation.page
    regulation = page.regulation
    rendered_contents = page.contents[:incorporation.context_start_position]
    rendered_contents = rendered_contents + \
        '<strong style="font-size: 1.5em;">'
    rendered_contents = rendered_contents + highlighted_context 
    rendered_contents = rendered_contents + '</strong>'
    rendered_contents = rendered_contents + \
        page.contents[incorporation.context_end_position:]
    # Get contexts from next and previous instances to aid in deduping
    if incorporation.pk > 1:
        previous_incorporation = Incorporation.objects.get(pk=(incorporation.pk - 1))
    else:
        previous_incorporation = incorporation
    try:
        next_incorporation = Incorporation.objects.get(pk=(incorporation.pk + 1))
    except:
        next_incorporation = incorporation
    return render_to_response('parser_tools/edit_incorporation.html',
                              {'form': form,
                              'incorporation': incorporation,
                              'regulation': regulation,
                              'page': page,
                              'previous_incorporation': previous_incorporation,
                              'next_incorporation': next_incorporation,
                              'ignore': ignore,
                              'rendered_contents': rendered_contents},
                              context_instance=RequestContext(request))

def update_incorporation(request, pk):
    '''Make necessary changes to the requested instance and return to
    the edit page.
    '''
    incorporation = get_object_or_404(Incorporation, pk=pk)
    form = IncorporationForm(instance=incorporation)
    if request.method == 'POST':
        form = IncorporationForm(request.POST, instance=incorporation)
        if form.is_valid():
            form.save()
            return redirect('parser_tools.views.edit_incorporation')
        else:
            return HttpResponse('Your submission was invalid.')
    else:
        return HttpResponse('No data was submitted.')

def edit_standards_organization(request, pk=None):
    '''Add or edit a StandardsOrganization object'''
    if pk is not None:
        standards_organization = \
            get_object_or_404(StandardsOrganization, pk=pk)
        message = 'Edit using the form below.'
    else:
        standards_organization = StandardsOrganization()
        message = 'Add a new standards organization using the form below.'
    if request.method == 'POST':
        form = StandardsOrganizationForm(request.POST, \
            instance=standards_organization)
        if form.is_valid():
            form.save()
            message = 'Saved successfully.'
        else:
            message = 'Your submission was invalid.'
    else:
        form = StandardsOrganizationForm(instance=standards_organization)
    standards_organizations_list = StandardsOrganization.objects.order_by('acronym')
    return render_to_response(
        'parser_tools/edit_standards_organization.html',
        {'form': form, 'pk': pk, 'message': message,
        'standards_organizations_list': standards_organizations_list},
        context_instance=RequestContext(request))

def scrape(request):
    if request.method == 'POST':
        form = ScrapeForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            parent_url = form.cleaned_data['url']
            parent_title = form.cleaned_data['title']

            # Initialize output string
            output = ''

            # Create temporary directory to contain downloaded files
            os.system("mkdir " + DATA_PATH + "tmp/")

            # Download PDFs from the specified URL to the temporary directory
            output = output + "<h3>Downloading files</h3>"
            os.system("wget -o " + DATA_PATH + "tmp/wget.log -P " + DATA_PATH + "tmp/ -r -l1 -A.pdf \
            -H -D.gov,.us -nd -np " + parent_url)
            os.system("rm " + DATA_PATH + "tmp/robots.*")
            output = output + "<p>Done.</p>"

            # Create ordered dictionary of url/filename pairs
            # Format: urls_and_filenames['filename.pdf'] = 'http://path/to/file/'
            urls_and_filenames = collections.OrderedDict()
            output = output + '<h3>Generating list of downloaded URLs</h3>'
            with file(DATA_PATH + 'tmp/wget.log') as f:
                log = f.read()
            downloaded_urls = re.findall(r'(https?://\S+)', log)

            for this_url in downloaded_urls:
                # Only keep URLs for PDF files
                if this_url[-4:] == '.pdf':
                    filename = this_url.rsplit('/', 1)[1]
                    urls_and_filenames[filename] = this_url        
                    output = output + 'Kept ' + this_url + '<br />'
                else:
                    output = output + '<em>Not a pdf:' + this_url + '</em><br />'
                    output = output + '<strong>removed</strong><br />'
            output = output + '<h3>Filename/URL pairs</h3>' \
                + str(urls_and_filenames)

            # For each downloaded file: check for naming conflicts, create
            # Regulation object, and move file out of tmp directory
            output = output + '<h3>Processing downloaded files</h3>'
            for this_filename, this_url in urls_and_filenames.items():
                output = output + "Checking " + this_filename + "... "
                current_files = os.listdir(DATA_PATH)
                if this_filename in current_files:
                    # Rename conflicting files
                    output = output + "<strong>conflict</strong><br />"
                    for n in range(1, 100):
                        renamed_file = this_filename[:-4] + '-' + str(n) + '.pdf'
                        if renamed_file not in current_files:
                            # We've found a unique filename; end the loop and
                            # keep the current value in renamed_file
                            output = output + '...renaming to ' + renamed_file \
                                + '<br />'
                            break
                    # Rename file in the filesystem
                    os.system('mv ' + DATA_PATH + 'tmp/' + this_filename + \
                        ' ' + DATA_PATH + 'tmp/' + renamed_file + '<br />')

                    # Rename the file in the current iteration of the loop through downloaded files
                    # This value will be used in creating the new Regulation object
                    this_filename = renamed_file
                else:
                    output = output + "no conflict<br />"

                # Move file out of tmp directory
                os.system('mv ' + DATA_PATH + 'tmp/' + this_filename + ' ' + DATA_PATH)

                # Create new Regulation object
                output = output + '...creating Django objects for ' + \
                    this_filename + ' / ' + this_url + '<br />'
                new_regulation = Regulation(
                    parent_title=parent_title, # from the POST form data
                    parent_url=parent_url, # from the POST form data
                    url=this_url,
                    media='PDF',
                    filename=this_filename,
                )
                new_regulation.save()

                # Create Page objects for each page in the regulation
                # This function lives in helper.py
                generate_regulation_pages(new_regulation)
 
            # Delete wget log, move files out of tmp directory, and delete tmp
            output = output + '<h3>Cleaning up</h3>'
            os.system('rm ' + DATA_PATH + 'tmp/wget.log')
            os.system('rmdir ' + DATA_PATH + 'tmp/')
            output = output + '<p>Done.</p>'
            return render_to_response('parser_tools/scrape.html',
                                      {'output': output},
                                      context_instance=RequestContext(request))

        else:
            return HttpResponse('Your submission is invalid.')
    else:
        form = ScrapeForm
    return render_to_response('parser_tools/scrape.html',
                              {'form': form, 'DATA_PATH': DATA_PATH},
                              context_instance=RequestContext(request))

def add_by_hand(request):
    '''A form to add regulations that can't be scraped.

    Currently, this is only used for HTML files.
    '''
    # add HTML file to folder
    if request.method == 'POST':
        # validate and save form data
        form = RegulationForm(request.POST)
        if form.is_valid():
            regulation = form.save()
            generate_regulation_pages(regulation)
            return redirect('parser_tools.views.add_by_hand')
        else:
            message = 'Your submission was invalid.'
            return render_to_response('parser_tools/add_by_hand.html',
                                      {'message': message},
                                      context_instance=RequestContext(request))
    else:
        form = RegulationForm()
        return render_to_response('parser_tools/add_by_hand.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))

def edit_regulation(request, pk=None):
    '''A form to edit the titles of regulations.
    
    If no primary key is specified, this script will find the next regulation
    where the title is "[Not set]". If a primary key is specified, the
    corresponding regulation will be presented as a form or saved.
    '''

    message = ''

    if pk is None:
        regulation = Regulation.objects.filter(title='[Not set]')[0]
        message = 'Edit the regulation below.'
    else:
        regulation = get_object_or_404(Regulation, pk=pk)
    if request.method == 'POST':
        form = RegulationForm(request.POST, instance=regulation)
        if form.is_valid():
            form.save()
            message = 'Saved.'
            regulation = Regulation.objects.filter(title='[Not set]')[0]
        else:
            message = 'Your submission was invalid.'
    form = RegulationForm(instance=regulation)
    return render_to_response('parser_tools/edit_regulation.html',
                              {'form': form, 'message': message,
                              'regulation': regulation,
                              'DATA_PATH': DATA_PATH},
                              context_instance=RequestContext(request))

def delete_regulation(request, pk):
    regulation = get_object_or_404(Regulation, pk=pk)
    os.system('rm ' + DATA_PATH + regulation.filename)
    regulation.delete()
    return HttpResponse('Deleted.')
