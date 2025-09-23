from django.shortcuts import render
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile, Contact

# Create your views here.
def home(request):

    # Fetch the first user profile. In a multi-user scenario, you might select
    # the user based on the request or a specific ID.
    # We use prefetch_related to efficiently load all related objects
    # (experiences, skills, tools, and projects with their technologies)
    # in a minimal number of database queries.
    # profile = UserProfile.objects.first()

    profile = UserProfile.objects.prefetch_related(
        'experiences',
        'skills',
        'tools',
        'projects__projecttechnology_set__technology'
    ).first()

    if request.method == 'POST':
        # Handle the contact form submission
        if profile:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # Create and save the contact message
            Contact.objects.create(
                user_profile=profile, name=name, email=email, subject=subject, message=message
            )
            messages.success(request, 'Your message has been sent successfully! I will get back to you soon.')
        else:
            messages.error(request, 'Could not submit form, no user profile found.')
        return redirect('home')
    
    context = {
        'profile': profile,
    }
    return render(request, 'index.html', context)
