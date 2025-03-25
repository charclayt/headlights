from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

import logging
import json

from myapp.models import UserProfile, Company
from myapp.utility.SimpleResults import SimpleResult, Message

# Configure logging
logger = logging.getLogger(__name__)

@method_decorator([login_required, permission_required("myapp.view_financereport")], name="dispatch")
class FinanceDashboardView(View):
    """
    This class handles the rendering and processing of the finance dashboard.
    """

    template_name = "finance.html"

    def get(self, request: HttpRequest) -> HttpResponse: 
        user_profile = UserProfile.objects.get(auth_id=request.user.id)
        
        context={
            "is_company_owner": user_profile.is_company_owner
        }
        
        return render(request, self.template_name, context)
    
    
@method_decorator([login_required, permission_required("myapp.view_financereport")], name="dispatch")   
class CompanyDetailsView(View):
    """
    This class handles the rendering and processing of the company details page.
    """
    
    template_name = "company_details.html"
    
    def get(self, request: HttpRequest) -> HttpResponse:
        return self.__render_company_details_page(request, SimpleResult())
    
    def post(self, request: HttpRequest) -> HttpResponse:
        result = SimpleResult()
        
        company_name = request.POST.get('companyName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        user_profile = UserProfile.objects.get(auth_id=request.user.id)
        company = user_profile.company_id
        contact_info = company.contact_info_id
        
        # Update info if it was provided
        company.name = company_name if company_name else company.name
        contact_info.email = email if email else contact_info.email
        contact_info.phone = phone if phone else contact_info.phone
        contact_info.address = address if address else contact_info.address
        
        company.save()
        contact_info.save()
        
        result.add_info_message("Contact details saved successfully")
        
        return self.__render_company_details_page(request, result)
    
    def __render_company_details_page(self, request, result: SimpleResult) -> HttpResponse:    
        user_profile = UserProfile.objects.get(auth_id=request.user.id)
        
        # Page only available for the company owner
        if not user_profile.is_company_owner:
            return redirect("index")
        
        company = user_profile.company_id
        company_contact_info = company.contact_info_id
        
        context = {
            "company_name": company.name,
            "current_email": company_contact_info.email,
            "current_phone": company_contact_info.phone,
            "current_address": company_contact_info.address,
            'info_messages': result.get_info_messages(),
            'error_messages': result.get_error_messages()
        }
        
        return render(request, self.template_name, context=context)


@method_decorator([login_required, permission_required("myapp.view_financereport")], name="dispatch")
class CompanyManageEmployeesView(View):
    """
    This class handles the rendering and processing of the add employees page.
    """
    
    template_name = "company_manage_users.html"
    
    def get(self, request: HttpRequest) -> HttpResponse:
        return self.__render_company_details_page(request, SimpleResult())
    
    def post(self, request: HttpRequest) -> JsonResponse:
        requestUser = UserProfile.objects.get(auth_id=request.user.id)
        
        data = json.loads(request.body.decode('utf-8'))
        user_id = data['user']
        action = data['action']
        
        user = UserProfile.objects.get(user_profile_id=user_id)
        
        if action == "remove":
            user.company_id = None
        
        elif action == "add":
            user.company_id = requestUser.company_id
            
        user.save()
        
        return JsonResponse({
                'status': 'success',
            })
        
    
    def __render_company_details_page(self, request, result: SimpleResult) -> HttpResponse:    
        user_profile = UserProfile.objects.get(auth_id=request.user.id)
        
        # Page only available for the company owner
        if not user_profile.is_company_owner:
            return redirect("index")
        
        company = user_profile.company_id
        users_in_company = UserProfile.objects.filter(~Q(user_profile_id=user_profile.pk), company_id=company)
        users_without_company = UserProfile.objects.filter(company_id=None)

        context = {
            'users_in_company': users_in_company,
            'users_without_company': users_without_company,
            'info_messages': result.get_info_messages(),
            'error_messages': result.get_error_messages()
        }
        
        return render(request, self.template_name, context=context)
    
    