from django.shortcuts import render,redirect
from django.http import HttpResponse 
from .models import LongToShort

# def hello_world(request):
#     return HttpResponse("hello world")

def home_page(request):
    context={
        'submitted':False,
        'error':False
        }
        
    if request.method == 'POST':
        data=request.POST
        long_url=data['longurl']
        customer_name=data['custom_name']

        try:
            # print('long_url: ',long_url)
            # print('customer_name: ',customer_name)
            # object created
            obj=LongToShort(long_url=long_url,short_url=customer_name)
            obj.save()
            context['long_url']=long_url
            context['short_url']=request.build_absolute_uri() + customer_name
            context['date']=obj.date
            context['click']=obj.click
            context['submitted']=True
        except:
            context['error']=True

    return render(request,'index.html',context)

def redirect_url(request,short_url):
    row = LongToShort.objects.filter(short_url=short_url)
    print(row)
    if len(row) == 0:
        return HttpResponse("no such short url exist")
        
    obj=row[0]
    long_url=obj.long_url

    obj.click=obj.click+1
    obj.save()

    return redirect(long_url)

def all_analytics(request):
    row=LongToShort.objects.all()
    context={
        'rows':row,
    }
    return render(request,"all-analytics.html",context)