from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from jplag_catcher import forms
from zipfile import ZipFile
from copy_catcher import settings

import os
import shutil
import zipfile
import subprocess

def main_page(request):
    if request.method == 'POST':
        form = forms.SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save(commit=False)
            model.ip_address = get_client_ip(request)
            model.save()
            return run_jplag(model)
    else:
        form = forms.SubmissionForm()

    return render(request, 'jplag_catcher/index.html', {'form': form})

def details_page(request):
    download_url = reverse('download')
    print(download_url)

    if os.path.isfile(settings.BASE_DIR / 'jplag_results' / 'index.html'):
        with open(settings.BASE_DIR / 'jplag_results' / 'index.html', 'r') as jplag_index_html_f:
            contents = jplag_index_html_f.readlines()
        
        contents.insert(5, f'<a href="{download_url}"><big><strong>Download Report</strong></big></a>\n')

        with open(settings.BASE_DIR / 'jplag_results' / 'index.html', 'w') as jplag_index_html_f:
            contents = "".join(contents)
            jplag_index_html_f.write(contents)

        with open(settings.BASE_DIR / 'jplag_results' / 'index.html', 'r') as jplag_index_html_f:
            response = HttpResponse(jplag_index_html_f.read())
        return response
    else:
        with open(settings.BASE_DIR / 'jplag_results' / 'jplag-log.txt', 'r') as jplag_output_f:
            response = HttpResponse("JPLAG ERROR\n" + 11 * "#" + "\n" + jplag_output_f.read(), content_type="text/plain")
        return response

def download_page(request):
    jplag_results_dir = settings.BASE_DIR / 'jplag_results'

    shutil.make_archive(jplag_results_dir, 'zip', jplag_results_dir)

    if os.path.isdir(jplag_results_dir):
        shutil.rmtree(jplag_results_dir)

    with open(os.path.join(settings.BASE_DIR, 'jplag_results.zip'), 'rb') as zip_file:
        response = HttpResponse(zip_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="jplag_results.zip"'
    
    return response

def run_jplag(submission_data):
    output_dir = os.path.join(settings.MEDIA_ROOT, os.path.splitext(str(submission_data.submissions))[0])
    jplag_results_dir = settings.BASE_DIR / 'jplag_results'

    if os.path.exists(jplag_results_dir):
        shutil.rmtree(jplag_results_dir)

    os.makedirs(jplag_results_dir)

    with ZipFile(os.path.join(settings.MEDIA_ROOT, str(submission_data.submissions)), 'r') as zipObj:
        zipObj.extractall(output_dir)
    
    # java -jar jplag-yourVersion.jar -l java19 -r /tmp/jplag_results_exercise1/ -s /path/to/exercise1
    with open(os.path.join(jplag_results_dir, 'jplag-log.txt'), 'w') as jplag_log_f:
        subprocess.run(
            ['java', '-jar', 'jplag.jar', '-l', submission_data.prog_language, '-r', jplag_results_dir, '-s', output_dir],
            stdout=jplag_log_f,
            stderr=jplag_log_f
        )
    
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    return redirect('details')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip