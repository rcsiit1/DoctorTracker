from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, timedelta

def sendmail(subject,template,to,context):
    subject = 'Subject'
    template_str = 'doctorfinder/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'rcsiit1@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def availableTimeSlots():
    appointments = [(datetime(2012, 5, 22, 10), datetime(2012, 5, 22, 10, 30)),
                (datetime(2012, 5, 22, 12), datetime(2012, 5, 22, 13)),
                (datetime(2012, 5, 22, 15, 30), datetime(2012, 5, 22, 17, 10))]
    
    hours = (datetime(2012, 5, 22, 9), datetime(2012, 5, 22, 18))
    
    duration=timedelta(minutes=30)
    
    slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
    
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        while start + duration <= end:
            print("{:%H:%M} - {:%H:%M}".format(start, start + duration))
            start += duration
