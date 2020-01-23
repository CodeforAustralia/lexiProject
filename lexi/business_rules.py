import time, re, urllib.request, os, json
from bs4 import BeautifulSoup

from .models import Word, Configuration

# Import Lexi functions
from .tools import open_file, set_elapsed_time

mostCommonWords = []
subset_common_words = 0
threshold = 0
source = ''
url = ''
uncommonWordsCounter = 0
commonWordsCounter = 0
suggestions = ''
words_looked_for = []

def look_for_synonyms(word):
    synonyms = []
    global source
    if(source == 'Thesaurus'):
        try:
            how_many_synonyms = 0
            content = urllib.request.urlopen( url + word)
            data = content.read()#.decode('utf-8')
            content.close()
            soup = BeautifulSoup(data, 'html.parser')
            results = soup.find_all("script")
            result = results[22].string #ToDo: Fix or improve this!
            json_txt = result.replace("window.INITIAL_STATE = ","").replace("};","}")
            #if word in ['tonight','finish']: # ToDo: IMPORTANT!
            #    print(result)
            #    print(' ')
            #    print(json_txt)
            structure = json.loads(json_txt)
            synonyms.clear()
            global mostCommonWords
            for synonym in structure['searchData']['tunaApiData']['posTabs']:
                word_type = synonym['pos']
                for term in synonym['synonyms']:
                    if int(term['similarity']) == 100 and term['term'] in mostCommonWords:
                        synonyms.append(term['term'] + ' <span class="badge badge-pill badge-warning">' + word_type + '</span>')
                        how_many_synonyms += 1
            if how_many_synonyms == 0:
                synonyms.append("Not common synonyms.")
            synonyms.sort()
            return synonyms
        except urllib.error.HTTPError as err:
            print(f"{word} was not found. (Code: {err.code})")
            if err.code == 404:
                synonyms.append(word + " was not found at Thesaurus.")
                return synonyms
            else:
                raise
        except json.decoder.JSONDecodeError as JSONerr:
            print(f"Response content for '{word}' is not in the JSON format expected. Error: {JSONerr}")
            synonyms.append(word + " was not found* at Thesaurus.")
            return synonyms
        except Exception as e1:
            print(f"There is an error in look_for_synonyms for {word}. Error: {str(e1)}")
            synonyms.append(word + " was not found at Thesaurus.")
            return synonyms
    else:
        synonyms.append(word + " has no synonyms that are common words.")
        return synonyms
        
def look_for_word(word):
    #ToDo: Include Keras text preprocessing for words with an character stick (i.e. ?)
    global mostCommonWords
    if word in mostCommonWords or re.findall("[0-9]", word):
        return "common"
    return "uncommon"

def split_by_words(simpleSentence):
    checked_simple_sentence = ""
    words = simpleSentence.split(" ")
    for w in words:
        if (w not in ("", " ", "\n", "\r")):
            whereIs = look_for_word(w.lower())
            if whereIs != "common":
                global uncommonWordsCounter
                uncommonWordsCounter += 1
                if w.lower() not in words_looked_for:
                    words_looked_for.append(w.lower())
                    synonyms = look_for_synonyms(w.lower())
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

def split_by_simple_sentences(wholeSentence):
    checked_whole_sentence = ""
    simpleSentences = wholeSentence.split(",")
    for ss in simpleSentences:
        checked_whole_sentence += split_by_words(ss)
    return checked_whole_sentence

def split_by_whole_sentences(paragraph):
    checked_paragraph = ""
    wholeSentences = paragraph.split(".")
    for ws in wholeSentences:
        checked_paragraph += split_by_simple_sentences(ws)
    return checked_paragraph

def split_by_paragraphs(text):    # ToDo: Return the same grammar and punctuaction.
    checked_message = ""
    paragraphs = text.split("\n\r\n")
    for p in paragraphs:
        checked_message += split_by_whole_sentences(p)
    return checked_message

def set_results(global_variables, start):
    global suggestions
    global_variables['suggestions'] = suggestions
    global commonWordsCounter, uncommonWordsCounter
    commonWordsPercentage = (commonWordsCounter/(commonWordsCounter + uncommonWordsCounter))
    global_variables['commonWordsPercentage'] = commonWordsPercentage * 100
    global threshold
    global_variables['threshold'] = threshold * 100
    if commonWordsPercentage >= threshold:
        global_variables['result'] = 'Passed!'
        global_variables['result_class'] = 'text-success'
    else:
        global_variables['result'] = 'Check the message'
        global_variables['result_class'] = 'text-danger'
    global_variables['uncommonWordsPercentage'] = (uncommonWordsCounter/(commonWordsCounter + uncommonWordsCounter)) * 100
    global subset_common_words
    global_variables['subset_common_words'] = subset_common_words
    global source
    global_variables['source'] = source
    global_variables['elapsed_time'] = set_elapsed_time(time.time() - start)

def get_common_words():
    configuration = Configuration.objects.all().first()
    global threshold, source, subset_common_words
    threshold = configuration.threshold
    source = configuration.get_source_description(configuration.source)
    subset_common_words = configuration.subset_common_words
    if(configuration.source == configuration.THESAURUS):
        common_words = open_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/20k.txt"))[:subset_common_words]
        return common_words
    elif(configuration.source in (configuration.DATABASE, configuration.AI_MODEL)):
        common_words = []
        db_words = Word.objects.all()
        if db_words.exists():
            for word in db_words.iterator():
                common_words.append(word.word)
        return common_words
    else:
        return None

def get_global_variables(global_variables):
    global mostCommonWords
    mostCommonWords = get_common_words()
    global url
    url = global_variables['url']
    global commonWordsCounter, uncommonWordsCounter
    commonWordsCounter = uncommonWordsCounter = 0
    global words_looked_for
    words_looked_for = []
    global suggestions
    suggestions = ''

def validate_word(word, global_variables):
    get_global_variables(global_variables)
    result = look_for_word(word)
    if result == 'common':
        return {'result': 'Common word', 'result_class': 'text-success'}
    else:
        return {'result': 'Uncommon word', 'result_class': 'text-danger'}

def make_analysis(text, global_variables):
    # ToDo: Set decorator to set Elapsed Time
    start = time.time()
    get_global_variables(global_variables)
    checked_message = split_by_paragraphs(text)
    set_results(global_variables, start)
    return checked_message

def import_common_words():
    count = 0
    #common_words = open_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/20k.txt"))[:2000]
    #for word in common_words:
    #    w = Word(word = word, is_common = True)
    #    w.save()
    #    count += 1
    #    if(count%400 == 0):
    #        print(str(count) + ' words saved!')
    print('2000 most common words imported successfully!')
