import time, re, urllib.request, os, json
from bs4 import BeautifulSoup

from .models import Word, Configuration

# Import Lexi functions
from .tools import openFile, setElapsedTime

mostCommonWords = []
threshold = 0
url = ''
uncommonWordsCounter = 0
commonWordsCounter = 0
suggestions = ''
elapsed_time = ''
words_looked_for = []

def lookForSynonyms(word):
    try:
        how_many_synonyms = 0
        synonyms = []
        content = urllib.request.urlopen( url + word)
        data = content.read().decode('utf-8')
        content.close()
        soup = BeautifulSoup(data, 'html.parser')
        results = soup.find_all("script")
        result = results[22].string #ToDo: Fix or improve this!
        json_txt = result.replace("window.INITIAL_STATE = ","").replace("};","}")
        structure = json.loads(json_txt)
        synonyms.clear()
        global mostCommonWords
        for synonym in structure['searchData']['tunaApiData']['posTabs']:
            for term in synonym['synonyms']:
                if int(term['similarity']) == 100 and word in mostCommonWords:  #ToDo: Validate the in validation
                    #synonyms.append(term['term'] + '<span class="badge badge-light">' + term['similarity'] + '</span>')
                    synonyms.append(term['term'])
                    how_many_synonyms += 1
        if how_many_synonyms == 0:
            synonyms.append("Not common synonyms.")
        return synonyms
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print(word + " was not found.")
            synonyms.append(word + " was not found at Thesaurus.")
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
                global uncommonWordsCounter
                uncommonWordsCounter += 1
                print(w + " - (" + whereIs + ")")
                if w.lower() not in words_looked_for:
                    words_looked_for.append(w.lower())
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
            else:
                global commonWordsCounter
                commonWordsCounter += 1
            checked_simple_sentence += '<span class=\''+ whereIs +'\'>' + w + '</span> '
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

def set_results(global_variables):
    global suggestions
    global_variables['suggestions'] = suggestions
    global commonWordsCounter, uncommonWordsCounter
    commonWordsPercentage = (commonWordsCounter/(commonWordsCounter + uncommonWordsCounter)) * 100
    global_variables['commonWordsPercentage'] = commonWordsPercentage
    print(commonWordsPercentage)
    if commonWordsPercentage >= 80:
        global_variables['result'] = 'Passed!'
        global_variables['result_class'] = 'pass'
    else:
        global_variables['result'] = 'Check the message'
        global_variables['result_class'] = 'bad'
    global_variables['uncommonWordsPercentage'] = (uncommonWordsCounter/(commonWordsCounter + uncommonWordsCounter)) * 100
    global elapsed_time
    global_variables['elapsed_time'] = elapsed_time

def makeAnalysis(text, global_variables):
    #start = time.time()
    #global mostCommonWords
    #mostCommonWords = openFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/20k.txt"))
    #global threshold
    #threshold = global_variables['threshold']
    #print(len(mostCommonWords[:int(threshold)]))
    #global url
    #url = global_variables['url']
    #print(global_variables)
    #global commonWordsCounter, uncommonWordsCounter
    #commonWordsCounter = uncommonWordsCounter = 0
    #global words_looked_for
    #words_looked_for = []
    #global suggestions
    #suggestions = ''
    #checked_message = splitByParagraphs(text)
    #global elapsed_time
    #elapsed_time = setElapsedTime(time.time() - start)
    #set_results(global_variables)
    checked_message = text
    configuration = Configuration.objects.all().first()
    print(configuration.source, configuration.threshold, configuration)
    words = Word.objects.all()[:10]
    if words.exists():
        print([word.word for word in words.iterator()])
    return checked_message

def import_common_words():
    count = 0
    #common_words = openFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/20k.txt"))[:2000]
    #for word in common_words:
    #    w = Word(word = word, is_common = True)
    #    w.save()
    #    count += 1
    #    if(count%400 == 0):
    #        print(str(count) + ' words saved!')
    print('2000 most common words imported successfully!')
