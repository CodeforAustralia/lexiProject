import os
#ToDo: Move all Business logic to another python file / folder.
from django.shortcuts import render, get_object_or_404
from django.utils import html

# Create your views here.
from .models import Message_Analysis, Business_Word, Common_Word

mostCommonWords = []
threshold = 0

def lookForWord(word):
    #ToDo: Include Keras text preprocessing for words with an character stick (i.e. ?)
    #ToDo: Look for the index if the word is within the 20k most common words, to avoid check multiple times
    global threshold
    global mostCommonWords
    if word in mostCommonWords[10000:]:
        return "twentyK"
    if word in mostCommonWords[5000:10000]:
        return "tenK"
    if word in mostCommonWords[2000:5000]:
        return "fiveK"
    if word in mostCommonWords[1000:2000]:
        return "twoK"
    if word in mostCommonWords[:1000]:
        return "oneK"
    return "uncommon"

def splitByWords(simpleSentence):
    checked_simple_sentence = ""
    words = simpleSentence.split(" ")
    for w in words:
        if (w != ""):
            #global mostCommonWords
            #global threshold
            whereIs = lookForWord(w.lower())
            print(w + " - " + whereIs)
            #if w.lower() in mostCommonWords[:int(threshold)]:
            checked_simple_sentence += '<span class=\'badge word '+ whereIs +'\'>' + w + '</span> '
            #else:
            #    checked_simple_sentence += '<span class=\'uncommon\'>' + w + '</span> '
    return checked_simple_sentence

def splitBySimpleSentences(wholeSentence):
    #print(wholeSentence)
    checked_whole_sentence = ""
    simpleSentences = wholeSentence.split(",")
    for ss in simpleSentences:
        checked_whole_sentence += splitByWords(ss)
    return checked_whole_sentence

def splitByWholeSentences(paragraph):
    checked_paragraph = ""
    wholeSentences = paragraph.split(".")
    for ws in wholeSentences:
        checked_paragraph += splitBySimpleSentences(ws)
    return checked_paragraph

def splitByParagraphs(text):
    checked_message = ""
    paragraphs = text.split("\n\r\n")
    for p in paragraphs:
        checked_message += splitByWholeSentences(p)
    return checked_message

def index(request):
    inputText = ""
    if('threshold' in request.POST):
        inputText = request.POST.__getitem__('inputText')
        global threshold
        threshold = request.POST.__getitem__('threshold')
        #ToDo: Change the way I read the file
        txtFilepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/20k.txt")
        txtFile = open(txtFilepath, "r")
        global mostCommonWords
        mostCommonWords = txtFile.read().split(",")
        txtFile.close()
        print(len(mostCommonWords[:int(threshold)]))
        return render(request, 'lexi/index.html', {
            'original_message': inputText,
            'checked_message': splitByParagraphs(inputText)
        })
    else:
        print("No threshold")
        return render(request, 'lexi/index.html')

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

#ToDo: Use generic views (https://docs.djangoproject.com/en/2.2/intro/tutorial04/)