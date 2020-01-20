import time, re, urllib.request, os, json
from bs4 import BeautifulSoup

from .models import Word, Configuration

# Import Lexi functions
from .tools import openFile, setElapsedTime

mostCommonWords = []
amount_common_words = 2000 #ToDo: Add to DB model and query it
threshold = 0
source = ''
url = ''
uncommonWordsCounter = 0
commonWordsCounter = 0
suggestions = ''
words_looked_for = []

def lookForSynonyms(word):
    synonyms = []
    global source
    if(source == 'Thesaurus'):
        try:
            how_many_synonyms = 0
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
    else:
        synonyms.append(word + " has no synonyms that are common words.")
        return synonyms
        
def lookForWord(word):
    #ToDo: Include Keras text preprocessing for words with an character stick (i.e. ?)
    #ToDo: Look for the index if the word is within the 20k most common words, to avoid check multiple times
    global mostCommonWords
    if word in mostCommonWords or re.findall("[0-9]", word):
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
                checked_simple_sentence += '<span class=\''+ whereIs +'\'>' + w + '</span> '
            else:
                global commonWordsCounter
                commonWordsCounter += 1
                checked_simple_sentence += (w + ' ')
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

def set_results(global_variables, start):
    global suggestions
    global_variables['suggestions'] = suggestions
    global commonWordsCounter, uncommonWordsCounter
    commonWordsPercentage = (commonWordsCounter/(commonWordsCounter + uncommonWordsCounter))
    global_variables['commonWordsPercentage'] = commonWordsPercentage * 100
    print(commonWordsPercentage)
    global threshold
    global_variables['threshold'] = threshold * 100
    if commonWordsPercentage >= threshold:
        global_variables['result'] = 'Passed!'
        global_variables['result_class'] = 'text-success'
    else:
        global_variables['result'] = 'Check the message'
        global_variables['result_class'] = 'text-danger'
    global_variables['uncommonWordsPercentage'] = (uncommonWordsCounter/(commonWordsCounter + uncommonWordsCounter)) * 100
    global amount_common_words
    global_variables['amount_common_words'] = amount_common_words
    global source
    global_variables['source'] = source
    global_variables['elapsed_time'] = setElapsedTime(time.time() - start)
    print(global_variables)

def getCommonWords():
    configuration = Configuration.objects.all().first()
    global threshold, source
    threshold = configuration.threshold
    source = configuration.get_source_description(configuration.source)
    # print(test_source, type(test_source))
    if(configuration.source == configuration.THESAURUS):
        print('TH')
        global amount_common_words
        common_words = openFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/20k.txt"))[:amount_common_words]
        # print(common_words[:50])
        return common_words
    elif(configuration.source in (configuration.DATABASE, configuration.AI_MODEL)):
        print('DB', 'AI')
        common_words = []
        db_words = Word.objects.all()
        if db_words.exists():
            for word in db_words.iterator():
                common_words.append(word.word)
        # print(list(common_words))
        return list(common_words)
    else:
        return None

def get_global_variables(global_variables):
    global mostCommonWords
    mostCommonWords = getCommonWords()
    global url
    url = global_variables['url']
    print(global_variables)
    global commonWordsCounter, uncommonWordsCounter
    commonWordsCounter = uncommonWordsCounter = 0
    global words_looked_for
    words_looked_for = []
    global suggestions
    suggestions = ''

def makeAnalysis(text, global_variables):
    start = time.time()
    get_global_variables(global_variables)
    checked_message = splitByParagraphs(text)
    set_results(global_variables, start)
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
