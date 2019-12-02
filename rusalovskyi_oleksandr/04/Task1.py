'''
Implement Text Analyzer program.
Features:

    Calculate words quantity;
    Extract text dictionary - unique words;
    Find keywords - top 3 most frequent words;
    Calculate frequency for each word - word quantity / all words quantity * 100.

Do not analyze such words as a, an, to, is, are, was, were, will, would, could,
and, or, if, he, she, it, this, my, etc.

Add docstring.

Example:
input: This is my favourite text. Let's try to analyze it. I love this text. I love Python.
output:

    words quantity: 9
    text dictionary: favourite, text, let's, try, analyze, love, python
    keywords: text - 2, love - 2, favourite - 1
    frequency: favourite - 11%, text - 22%, let's - 11%, try - 11%, analyze - 11%, love - 22%, python - 11%

author Oleksandr Rusalovskyi
2019-12-02
'''


def _count_words_(input_str, not_analizable_set):

    words = []
    # Making two steps for split, cause smbd don't make space after dot
    for first_split in input_str.split('.'):
        words += first_split.split(' ')

    # lower and strip words 
    lowered_stripped_words = list(map(lambda w: w.strip('.').strip().lower(), words))

    # filter words with not_analizable_set
    filtered_words = list(filter(lambda w: w not in not_analizable_set, lowered_stripped_words))

    # Initiate dict from keys of list with value 0
    words_counts = dict.fromkeys(filtered_words, 0)

    # count words in filtered_words using predefined dict with zeros
    for word in filtered_words:
        words_counts[word] += 1

    return words_counts


def _top_n_words_(dict_words_cnt, top_n):

    # make list from inputed dict
    list_to_sort = list(dict_words_cnt.items())
    # sort by count(*) desc
    list_to_sort.sort(key=lambda item: item[1], reverse=True)

    # return slice of top_n
    return list_to_sort[:top_n]


def _word_frequency_(dict_words_cnt):

    # try not modify incoming object:)
    result = dict_words_cnt.copy()

    # count words
    all_words_count = sum(list(result.values()))

    for k,v in result.items():
        result[k] = int(100 * v / all_words_count)

    return result
    
    
def text_analizer(input_str):
    """
    Function text_analizer() analizes input text for words count, dictionary, frequency and top 3 words. Prints result to output.
    :param input_str: text string to analize words
    :type input_str: str
    :return: None
    :rtype: None
    """

    DONT_ANALIZE = {'a', 'an', 'to', 'is', 'are', 'was', 'were', 'will',
                    'would', 'could', 'and', 'or', 'if', 'i', 'he', 'she',
                    'it', 'this', 'my', 'his', 'her', ''}
    
    words_counts = _count_words_(input_str, DONT_ANALIZE)

    top_3_words = _top_n_words_(words_counts, 3)

    word_freq = _word_frequency_(words_counts)

    # results formatting and output
    words_quantity = sum(list(words_counts.values()))
    text_dictionary = ', '.join(list(words_counts.keys()))
    keywords = ', '.join(['{0} - {1}'.format(w, c) for w, c in top_3_words])
    frequency = ', '.join(['{0} - {1}%'.format(w, f) for w, f in word_freq.items()])

    output = f' words quantity: {words_quantity}\n text dictionary: {text_dictionary}\n keywords: {keywords}\n frequency: {frequency}'

    print(output)

    return None


text_analizer(input('Please insert text to analize: '))
