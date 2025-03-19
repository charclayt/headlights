from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

import logging

from myapp.models import Claim, UploadedRecord
from myapp.utility.SimpleResults import SimpleResult

# Configure logging
logger = logging.getLogger(__name__)

@method_decorator(login_required, name="dispatch")
class CustomerDashboardView(View):
    """
    This class handles the rendering and proccessing of the end-user dashboard page.
    """

    template_name = "customer.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles the GET request for the customer dashboard.

        Args:
            request: the GET request object.
            message: 

        Returns:
            render: the customer.html template.
        """

        num_claims = Claim.objects.all().count()
        
        context = {
            'num_claims': num_claims,
        }

        logger.info(f"{request.user} accessed the customer dashboard.")
        return render(request, self.template_name, context=context)

@method_decorator(login_required, name="dispatch")
class ClaimUploadView(View):
    """
    This class handles the proccessing of uploaded claims data.
    """
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        return redirect("customer_dashboard")
    
    def post(self, request: HttpRequest, ignore_validation: int = 0) -> JsonResponse:
        result = SimpleResult()
        file = request.FILES['claims_file']
        
        if not file.name.endswith(".csv"):
            result.add_error_message_and_mark_unsuccessful("Invalid file type")
        
        if result.success:
            uploadResult = UploadedRecord.upload_claims_from_file(file, None, True if ignore_validation == 1 else False)  
            result.add_messages_from_result_and_mark_unsuccessful_if_error_found(uploadResult)
            
        status = "success"
        if not result.success:
            status = "error"
            for message in result.get_error_messages():
                if message.text == "Column Name Error":
                    status = "confirmationRequired"
                    result.messages.remove(message)
        
        return JsonResponse({
                'status': status,
                'message': '\n\n'.join([message.text for message in result.messages])
            })
        