from django.shortcuts import render, get_object_or_404
from django.utils import html

# Import Lexi functions
from .business_rules import makeAnalysis

# Create your views here.
from .models import Message_Analysis, Business_Word, Common_Word

global_variables = {
    'url': 'http://www.thesaurus.com/browse/',
    'threshold': 0,
    'suggestions': '',
    'count': 0,
    'commonWordsPercentage': 0.0,
    'uncommonWordsPercentage': 0.0
}

def index(request):
    return render(request, 'lexi/index.html')

def analysis(request):
    inputText = request.POST.__getitem__('inputText')
    if('threshold' in request.POST and inputText != ""):
        global_variables['threshold'] = request.POST.__getitem__('threshold')
        checked_message = makeAnalysis(inputText, global_variables),
        return render(request, 'lexi/analysis.html', {
            'checked_message': checked_message,
            'suggestions': global_variables['suggestions'],
            'commonWords': global_variables['commonWordsPercentage'],
            'uncommonWords': global_variables['uncommonWordsPercentage']
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