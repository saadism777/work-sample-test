from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import re
import pyrebase
x = []
form_fields = []
in_value = []

data_dictionary = {

}

firebaseConfig={"apiKey": "AIzaSyBSaNWZH_N9fb-1ExTxET4bqfGGEmbjjhw",
  "authDomain": "work-sample-test.firebaseapp.com",
  "databaseURL": "https://work-sample-test-default-rtdb.firebaseio.com",
  "projectId": "work-sample-test",
  "storageBucket": "work-sample-test.appspot.com",
  "messagingSenderId": "776126785760",
  "appId": "1:776126785760:web:59d986efc982eb7e1c0885",
  "measurementId": "G-Q5SNEE822W"}

firebase=pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def homepage(request):
    if x:
        form_name = []
        for i in x:
            form_name.append(i[0])
        data = {
            'field_type': form_name
        }
        return render(request, 'project1/homepage.html', data)
    else:
        return render(request, 'project1/homepage.html')

def responses(request):
    dat=db.child('Forms').child().get()
    keydata=[]
    for key in dat.val():
         #keydata = [ key for i in range(len(db.child('NameOfForms').get().val())) ]
         keydata.append(key[0:])
    data = {
            'field_type': keydata
           }
    return render(request, 'project1/responses.html', data)


def gen_form(request):
    return render(request, 'project1/g_form.html')


def data(request):
    field_type = request.GET.getlist('data[]', None)
    field_data = request.GET.getlist('data1[]', None)
    x.append(field_data)
    form_fields.append(field_type)
    return HttpResponse("Done")


def form(request, name):
    flag = 0
    form_data = []
    for i in x:
        if name in i:
            flag = x.index(i)
            form_data = i

    print(form_fields[flag])
    print(form_data[1:])
    length = len(form_data)-1
    mylist = zip(form_data[1:], form_fields[flag])
    data = {
        'f_name': name,
        'mylist': mylist,
        'length': length,
        'form_label': form_data[1:],

    }
    
    #db.child("NameOfForms").child().update(namedata)
    return render(request, 'project1/form_view.html', data)


def formSubmit(request, no):



    k = 0
    fname = request.POST.get('fname')
    flabels = request.POST.get('flabel')
    flabels = re.sub("['']", "", flabels)

    flabels = flabels[1:len(flabels)-1]
    flabels = list(flabels.split(","))

    in_data = []
    for i in range(no):
        k = k + 1
        j = f'{k}'
        in_data.append(request.POST.get(j))

    in_value.append(in_data)

    if data_dictionary:
        key = data_dictionary.keys()
        if fname in key:
            data_dictionary[fname].append(in_data)
        else:
            data_dictionary.update({fname: [flabels, in_data]})
    else:
        data_dictionary.update({fname: [flabels, in_data]})

    n_data = []

    for name, model in data_dictionary.items():
        if name == fname:
            n_data = model
    length = len(n_data[0])
    n_dist = {
        'fname': fname,
        'h_data': n_data[0],
        'in_value': n_data[1:],
        'length': length+1,

    }
    #firebase push
    
    db.child("Forms").child(fname).update(n_dist)
    return render(request, 'project1/individual_table.html', n_dist)


def reports(request, name):

    try:
        n_data = []
        for namee, model in data_dictionary.items():
            if namee == name:
                n_data = model
        length = len(n_data[0])
        dat = db.child(name).get()
        n_dist = {
            'fname': name,
            'h_data': n_data[0],
            'in_value': n_data[1:],
            'length': length,

        }
        

        return render(request, 'project1/individual_table.html', n_dist)
    except IndexError:
        return render(request, 'project1/nodata.html')


def check(request, name):
    dat = db.child().get()
    #fname = dat.to_dict()
    fname = db.child('Forms').child(name).child('fname').get()
    h_data = db.child('Forms').child(name).child('h_data').get()
    in_value = db.child('Forms').child(name).child('in_value').get()
    length = db.child('Forms').child(name).child('length').get()
    
    n_dist = {
            'fname': fname.val(),
            'h_data': h_data.val()[0:],
            'in_value': in_value.val()[0:][0:],
            'length': length.val(),

        }
    return render(request,"project1/check.html",n_dist)