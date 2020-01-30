from django.shortcuts import render, get_object_or_404
from django.utils import html

# Import Lexi functions
from .business_rules import make_analysis, import_common_words, validate_word

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
    post = request.POST.copy()
    input_test = post['inputText']
    if(input_test != ""):
        checked_message = make_analysis(input_test, global_variables)
        return render(request, 'lexi/analysis.html', {
            'checked_message': checked_message,
            'global_variables': global_variables
        })
    else:
        print("There is not a text to analyze")
        return render(request, 'lexi/index.html', {
            "error_message": "There is not a text to analyze."
        })

def word_test(request):
    result = {}
    word = ''
    if request.POST.dict():
        post = request.POST.copy()
        word = post['word']
        if word:
            result = validate_word(word, global_variables)
    return render(request, 'lexi/word_test.html', {
        'word': word,
        'result': result,
    })

def import_words(request):
    import_common_words()
    return render(request, 'lexi/index.html', {})

#ToDo: Use generic views (https://docs.djangoproject.com/en/2.2/intro/tutorial04/)