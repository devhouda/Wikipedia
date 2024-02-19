from django.shortcuts import render, redirect
from .forms import CreateNewEntry, EditEntry
from random import choice
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": util.get_entry(title)
        })

def search(request):
    query = request.GET.get('q')
    filtered_byquery = list(filter(lambda entry: query in entry, util.list_entries()))
    if len(filtered_byquery) > 0:
        return render(request, 'encyclopedia/search.html', {
            "query": query,
            "entries": filtered_byquery
        })
    else:
        return render(request, "encyclopedia/error.html", {
        "query": query
    })

def create(request):
    form = CreateNewEntry
    # if request is not post, initialize an empty form
    form = CreateNewEntry(request.POST or None)
    if request.method == "POST":
        form = CreateNewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                #error
                return render(request, "encyclopedia/error.html", {
                    "message": "ERROR! Entry already exist"
                })
            else:
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": util.get_entry(title)
                })
        else:
            form = CreateNewEntry()
    return render(request, "encyclopedia/create.html", {
                "form": form
            })


def edit(request, title):
    form = EditEntry
    # if request is not post, initialize an empty form
    Entry = EditEntry(util.get_entry(title))
    if request.method == "POST":
        form = EditEntry(request.POST, Entry)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": util.get_entry(title)
            })
        else:
            form = EditEntry(util.get_entry(title))

    return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form
            })

def random(request):
    all_entries = util.list_entries()
    title = choice(all_entries)
    return render(request, "encyclopedia/random.html", {
        "title": title,
        "content": util.get_entry(title)
    })