from logging import PlaceHolder
from django.http.response import HttpResponse,HttpResponseNotFound
from django.shortcuts import render
from django.http import Http404
from . import util
from markdown2 import Markdown
from django import forms

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(util.get_entry(title)),
            "title": title
        })
    else:
        return HttpResponseNotFound('<h1>404 Page not found</h1>')