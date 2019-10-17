import os, urllib.request, json, warnings, re
#ToDo: Move all Business logic to another python file / folder.
from django.shortcuts import render, get_object_or_404
from django.utils import html
from pprint import pprint
from bs4 import BeautifulSoup

# Create your views here.
from .models import Message_Analysis, Business_Word, Common_Word

mostCommonWords = []
threshold = 0
url = 'http://www.thesaurus.com/browse/'
suggestions = ''
allSynonyms = []
count = 0

def lookForSynonyms(word):
    try:
        how_many_synonyms = 0
        synonyms = []
        content = urllib.request.urlopen(url + word)
        data = content.read().decode('utf-8')
        content.close()
        soup = BeautifulSoup(data, 'html.parser')
        results = soup.find_all("script")
        result = results[22].string #ToDo: Fix or improve this!
        json_txt = result.replace("window.INITIAL_STATE = ","").replace("};","}")
        structure = json.loads(json_txt)
        synonyms.clear()
        for synonym in structure['searchData']['tunaApiData']['posTabs']:
            for term in synonym['synonyms']:
                if int(term['similarity']) >= 60 and word in mostCommonWords:
                    #allSynonyms[word].append(term['term'])
                    synonyms.append(term['term'] + '<span class="badge badge-light">' + term['similarity'] + '</span>')
                    how_many_synonyms += 1
                    global count
                    count += 1
                    #print(allSynonyms)
        if how_many_synonyms == 0:
            synonyms.append("Not common synonyms.")
            #allSynonyms[word] = []
            #print(allSynonyms)
        return synonyms
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print(word + " was not found.")
            synonyms.append(word + " was not found at Thesaurus.")
            #allSynonyms[word] = []
            return synonyms
        else:
            raise
    except Exception as e1:
        print(f"There is an error in lookForSynonyms for {word}: {str(e1)}")
        synonyms.append(word + " was not found at Thesaurus.")
        return synonyms
        
def lookForWord(word):
    #ToDo: Include Keras text preprocessing for words with an character stick (i.e. ?)
    #ToDo: Look for the index if the word is within the 20k most common words, to avoid check multiple times
    global threshold
    global mostCommonWords
    if word in mostCommonWords[:int(threshold)] or re.findall("[0-9]", word):
        return "common"
    return "uncommon"

def splitByWords(simpleSentence):
    checked_simple_sentence = ""
    words = simpleSentence.split(" ")
    for w in words:
        if (w not in ("", " ", "\n", "\r")):
            whereIs = lookForWord(w.lower())
            if whereIs != "common":
                print(w + " - (" + whereIs + ")")
                synonyms = lookForSynonyms(w.lower())
                if synonyms:    #ToDo: Check Generator Expressions (https://www.python.org/dev/peps/pep-0289/)
                    global suggestions
                    suggestions += '<section>'
                    suggestions += '<h3>' + w + '</h3>'
                    suggestions += '<ul>'
                    for synonym in synonyms:
                        #print(synonym)
                        suggestions += '<li>' + synonym + '</li>'
                    suggestions += '</ul>'
                    suggestions += '</section>'
            #if w.lower() in mostCommonWords[:int(threshold)]:
            checked_simple_sentence += '<span class=\'badge word '+ whereIs +'\'>' + w + '</span> '
            #checked_simple_sentence += '<span class=\''+ whereIs +'\'>' + w + '</span> '
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
    return render(request, 'lexi/index.html')

def analysis(request):
    inputText = ""
    #print(request.POST.__getitem__('inputText'))
    inputText = request.POST.__getitem__('inputText')
    if('threshold' in request.POST and inputText != ""):
        global threshold
        threshold = request.POST.__getitem__('threshold')
        #ToDo: Change the way I read the file
        txtFilepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/20k.txt")
        txtFile = open(txtFilepath, "r")
        global mostCommonWords
        mostCommonWords = txtFile.read().split(",")
        txtFile.close()
        global suggestions
        suggestions = ''
        print(len(mostCommonWords[:int(threshold)]))
        return render(request, 'lexi/analysis.html', {
            'original_message': inputText,
            'checked_message': splitByParagraphs(inputText),
            'suggestions': suggestions,
            'allSynonyms': allSynonyms,
            'count': count
        })
    else:
        print("There is not a text to analyze")
        return render(request, 'lexi/index.html', {
            "error_message": "There is not a text to analyze."
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

#ToDo: Use generic views (https://docs.djangoproject.com/en/2.2/intro/tutorial04/)