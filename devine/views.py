from django.shortcuts import render, redirect
from django.http import JsonResponse
from .element_flow import process_flow  # Import the function to process the flow

def home(request):
    return render(request, 'index.html')

def process_form(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        email = request.POST.get('email')
        hr_data = '''email: hr1@techcorp.com, name: Vishvas, company: Google
                     email: hr2@datavision.com, name:Rahul, company: DataVision
                     email: hr3@startuplab.com, name: Priti, company: StartupLab'''
        input_dict = {"role": role, "email": email, "hr_data": hr_data}
        result = process_flow(input_dict)  # Call the function to process the flow
        return JsonResponse({'result': result})
    return redirect('home')