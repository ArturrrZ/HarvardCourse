from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import random
import markdown2
from . import util
from django.contrib import messages

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_entry(request,title):


    entry=util.get_entry(title)
    if entry:

        entry=markdown2.markdown(f"{entry}")
        return render(request,"encyclopedia/get_entry.html",{
            "title": title,
            "entry": entry,
        })
    else:
        return render(request,"encyclopedia/error.html")


def random_entry(request):
    all_entries=util.list_entries()
    random_title=random.choice(all_entries)
    return HttpResponseRedirect(reverse("wiki:get_entry",args=(random_title,)))


def search(request):
    if request.method == 'GET':
        query=request.GET['q']
        if query.lower() in [old.lower() for old in util.list_entries()]:
            return HttpResponseRedirect(reverse("wiki:get_entry", args=(query,)))
        else:
            list_of_entries = []
            for entry in util.list_entries():
                if query.lower() in entry.lower():
                    list_of_entries.append(entry)

            return render(request,"encyclopedia/search.html",{
                "list": list_of_entries,
            })


def create_new_page(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        content = request.POST.get('content')
        if not title.lower() in [old.lower() for old in util.list_entries()]:
            with open(f"entries/{title}.md","w") as new_entry:
                new_entry.write(content)
            return HttpResponseRedirect(reverse("wiki:get_entry", args=(title,)))
        else:
            # messages.add_message(request, messages.error, "Hello world.")
            messages.error(request, "Entry already exist")
    return render(request,"encyclopedia/new_page.html")


def edit_page(request,title):
    if request.method == 'POST':
        new_body=request.POST.get("body")
        util.save_entry(title,new_body)
        return HttpResponseRedirect(reverse("wiki:get_entry",args=(title,)))
    body = util.get_entry(title)
    return render(request,"encyclopedia/edit_page.html",{
        "title": title,
        "body": body,
    })