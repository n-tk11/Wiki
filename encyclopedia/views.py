from logging import PlaceHolder
from django.http.response import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django import forms
from django.urls import reverse
import re

markdowner = Markdown()


class Search(forms.Form):
    stitle = forms.CharField(label="",widget=forms.TextInput(attrs={'class' : 'search', 'placeholder': 'Search'}))

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
