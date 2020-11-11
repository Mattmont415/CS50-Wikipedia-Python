from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

import random

markdowner = Markdown()

from . import util


def index(request):
  return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
  })


def edit(request, entrytitle):
  #Who knew that get_entry loaded the contents of the file *FACEPALM*
  loadpage = util.get_entry(entrytitle)    
  if request.method == "POST":
    util.delete_entry(entrytitle)
    entrytitle = request.POST["title"]
    entryarea = request.POST["entryarea"]

    util.save_entry(entrytitle, entryarea)
    return HttpResponseRedirect(reverse("entry", kwargs={'title': entrytitle}))
  else:
    return render(request, "encyclopedia/edit.html", {
      "entrytitle": entrytitle,
      "entryarea": loadpage
    })

def entry(request, title):
  entrylist = util.list_entries()
  if title in entrylist:
    entryname = util.get_entry(title)
    conventry = markdowner.convert(entryname)
    return render(request, "encyclopedia/entry.html", {
      #Pass the new page both so you can edit the TITLE and display BODY
      "entry": markdowner.convert(entryname),
      "entrytitle": title
    })
  else:
    return render(request, "encyclopedia/entryfail.html", {
      "entrytitle": title
    })

def search(request):
  searchitem = request.GET.get("q")
  if (util.get_entry(searchitem) is not None):
    return HttpResponseRedirect(reverse("entry", kwargs={'title': searchitem}))
  else:
    subString = []
    for entry in util.list_entries():
      if searchitem.upper() in entry.upper():
        subString.append(entry)
    if len(subString) == 0:
      return render(request, "encyclopedia/entryfail.html", {
        "entrytitle": searchitem
      })

    return render(request, "encyclopedia/index.html", {
      "entries": subString,
      "search": True,
      "searchitem": searchitem
    })


def create(request):
  if request.method == "POST":
    entrytitle = request.POST["title"]
    entryarea = request.POST["entryarea"]
    #If it doesn't exist, 
    if (util.get_entry(entrytitle) is None):
      util.save_entry(entrytitle, entryarea)
      return HttpResponseRedirect(reverse("entry", kwargs={'title': entrytitle}))
    else:
      strstr = "The entry " + entrytitle + " already exists, edit name or choose another."
      return render(request, "encyclopedia/create.html", {
        "message": strstr,
        "entrytitle": entrytitle,
        "entryarea": entryarea
      })
  else:
    return render(request, "encyclopedia/create.html",)

def rando(request):
  #Load the list entries
  #Find random number between 0 and len(list)
  #Go to the link of that pages entrytitle
  listentry = util.list_entries()
  length = len(listentry)
  rand = random.randint(0,length-1)
  entry = listentry[rand]
  return HttpResponseRedirect(reverse("entry", kwargs={'title': entry}))
