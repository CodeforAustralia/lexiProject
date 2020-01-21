from django.shortcuts import render, get_object_or_404
from django.utils import html

# Import Lexi functions
from .business_rules import makeAnalysis, import_common_words

# Create your views here.
global_variables = {
    'url': 'http://www.thesaurus.com/browse/',
    'suggestions': '',
    'count': 0,
    'commonWordsPercentage': 0.0,
    'uncommonWordsPercentage': 0.0
}

def index(request):
    return render(request, 'lexi/index.html')

def analysis(request):
    inputText = request.POST.__getitem__('inputText')
    if(inputText != ""):
        checked_message = makeAnalysis(inputText, global_variables)
        return render(request, 'lexi/analysis.html', {
            'checked_message': checked_message,
            'global_variables': global_variables
        })
    else:
        print("There is not a text to analyze")
        return render(request, 'lexi/index.html', {
            "error_message": "There is not a text to analyze."
        })

def import_words(request):
    import_common_words()
    return render(request, 'lexi/index.html', {})

#ToDo: Use generic views (https://docs.djangoproject.com/en/2.2/intro/tutorial04/)