from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

import logging

from myapp.models import Claim, UploadedRecord
from myapp.forms import RecordUploadForm

# Configure logging
logger = logging.getLogger(__name__)


class IndexView(View):
    """
    This class handles the rendering and proccessing of the index page.
    """

    template_name = "index.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles the GET request for the index page.

        Args:
            request: the GET request object.

        Returns:
            render: the index.html template.
        """

        num_claims = Claim.objects.all().count()
        upload_form = RecordUploadForm()
        
        context = {
            'num_claims': num_claims,
            'upload_form': upload_form,
        }

        logger.info(f"{request.user} accessed the index page.")
        return render(request, self.template_name, context=context)

    @login_required
    @require_http_methods(["POST"])
    def record_upload(request):
        form = RecordUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            result = UploadedRecord.upload_claims_from_file(file, None)
                
        return HttpResponseRedirect("/")