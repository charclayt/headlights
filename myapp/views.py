from django.shortcuts import render
from .models import Claim

# Create your views here.
def index(request):
    """ View function for site home page (placeholder)"""

    num_claims = Claim.objects.all().count()

    context = {
        'num_claims': num_claims
    }

    return render(request, 'index.html', context=context)
