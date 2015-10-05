from django.template import RequestContext
from django.shortcuts import render_to_response
from .forms import ReceptionForm
from .models import Schedule


def add_reception(request):
    if request.method == 'POST':
        form = ReceptionForm(request.POST)
        if form.is_valid():
            if Schedule.objects.reception_is_possibly(
                    form.cleaned_data['doctor'],
                    form.cleaned_data['reception_date'],
                    form.cleaned_data['reception_time']):
                form.save()
                return render_to_response('HospitalShed/index.html',
                                          RequestContext(request,
                                                         {'form': ReceptionForm(),
                                                          'success': True}))
            else:
                message = 'Прием в данное время невозможен'
                return render_to_response('HospitalShed/index.html',
                                          RequestContext(request,
                                                         {'form': form,
                                                          'success': False,
                                                          'message': message}))
        else:
            message = 'Обнаружены ошибки в заполнении полей формы'
            return render_to_response('HospitalShed/index.html',
                                      RequestContext(request, {'form': form,
                                                               'success': False,
                                                               'message': message}))
    else:
        return render_to_response('HospitalShed/index.html',
                                  RequestContext(request, {'form': ReceptionForm()}))
