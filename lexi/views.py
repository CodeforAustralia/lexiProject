import os
#ToDo: Move all Business logic to another python file / folder.
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Message_Analysis, Business_Word, Common_Word

def splitByWholeSentences(paragraph):
    return paragraph

def splitByParagraphs(text):
    checked_message = ""
    paragraphs = text.split("\n\r\n")
    print(len(paragraphs))
    for p in paragraphs:
        checked_paragraph = splitByWholeSentences(p)
        checked_message += checked_paragraph
    return checked_message

def index(request):
    inputText = ""
    if('threshold' in request.POST):
        inputText = request.POST.__getitem__('inputText')
        threshold = request.POST.__getitem__('threshold')
        #ToDo: Change the way I read the file
        txtFilepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/20k.txt")
        txtFile = open(txtFilepath, "r")
        mostCommonWords = txtFile.read().split(",")
        txtFile.close()
        print(len(mostCommonWords[:int(threshold)]))
        print(splitByParagraphs(inputText))
    else:
        print("No threshold")
    return render(request, 'lexi/index.html', {
        'checked_message': splitByParagraphs(inputText)
    })

def commonWords(request):
    common_words = Common_Word.objects.order_by('-times')
    return render(request, 'lexi/commonwords.html', {
        'common_words': common_words
    })

def businessWords(request):
    business_words = Business_Word.objects.order_by('-times')
    return render(request, 'lexi/businesswords.html', {
        'business_words': business_words
    })

def messageAnalysis(request):
    message_analysis = Message_Analysis.objects.order_by('-total_words')
    return render(request, 'lexi/messageanalysis.html', {
        'message_analysis': message_analysis
    })

def detail(request, analysis_id):
    analysis = get_object_or_404(Message_Analysis, pk=analysis_id)
    return render(request, 'lexi/detail.html', {
        'analysis': analysis
    })