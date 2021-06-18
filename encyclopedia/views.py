from logging import PlaceHolder
from django.forms import widgets
from django.forms.widgets import Textarea
from django.http.response import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django import forms
from django.urls import reverse

markdowner = Markdown()

class Search(forms.Form):
    stitle = forms.CharField(label="",widget=forms.TextInput(attrs={'class' : 'search', 'placeholder': 'Search'}))

class Create(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control col-sm-10', 
        'placeholder' : 'Title'
        }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control col-sm-10',
        'placeholder' : 'Type you content with markdown'
        }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": Search()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "content": markdowner.convert(util.get_entry(title)),
        "title": title
    })

def search(request):
    form = Search(request.POST)

    if form.is_valid():
        title = form.cleaned_data["stitle"]
        for entry in util.list_entries():
            if entry.lower().find(title) >= 0:
                return HttpResponseRedirect(reverse("encyclopedia:entry",args=[entry]))
        return HttpResponseNotFound('<h1>404 Page not found</h1>')     

def CreatePage(request):
    if request.method == "POST":
        form = Create(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title,content)

            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))

    return render(request,"encyclopedia/create.html", {
        "contentbox" : Create()
    })
