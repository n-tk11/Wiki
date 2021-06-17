from logging import PlaceHolder
from django.http.response import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django import forms
from django.urls import reverse

markdowner = Markdown()


class Search(forms.Form):
    stitle = forms.CharField(widget=forms.TextInput(attrs={'class' : 'search', 'placeholder': 'Search'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": Search()
    })

def entry(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(util.get_entry(title)),
            "title": title
        })
    else:
        return HttpResponseNotFound('<h1>404 Page not found</h1>')

def search(request):
    form = Search(request.POST)

    if form.is_valid():
        title = form.cleaned_data["stitle"]
        return HttpResponseRedirect(reverse("encyclopedia:entry",args=[title]))
