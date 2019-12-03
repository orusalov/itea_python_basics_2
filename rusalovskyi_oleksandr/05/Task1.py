"""
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
"""


DONT_ANALIZE = {'a', 'an', 'to', 'is', 'are', 'was', 'were', 'will',
                'would', 'could', 'and', 'or', 'if', 'i', 'he', 'she',
                'it', 'this', 'my', 'his', 'her', 's', 'the', 'be', 'in',
                'at', 'of', 'they', 'as', 'with', 'for', ''}

SPECIAL_SYMBOLS = ''''!@#$%^&*()[]{};:,./<>?\|`~-=_+"'''

TOP_N_WORDS_OCCURANCE = 10


def count_words(input_str, special_symbols=SPECIAL_SYMBOLS, not_analizable_set=DONT_ANALIZE):
    """
    Function count_words() makes dict of words with its occurance number. It removes
    special_symbols that is given as parameter and removes words from not_analizable_set
    :param input_str: text string to analize words
    :param special_symbols: string with all removable symbols. Those symbols will be split argument for words
    :param not_analizable_set: set of words in lower case that will not be present in returned dict
    :type input_str: str
    :type special_symbols: str
    :type not_analizable_set: set
    :return: dict with words and its occurance number
    :rtype: dict
    """
    
    for sign in special_symbols:
        input_str = input_str.replace(sign, ' ')

    words = input_str.split()

    # lower and strip words 
    lowered_stripped_words = list(map(lambda w: w.strip().lower(), words))

    # filter words with not_analizable_set
    filtered_words = list(filter(lambda w: w not in not_analizable_set, lowered_stripped_words))

    # filter numbers
    filtered_words = list(filter(lambda w: not w.isdigit(), filtered_words))

    # Initiate dict from keys of list with value 0
    words_counts = dict.fromkeys(filtered_words, 0)

    # count words in filtered_words using predefined dict with zeros
    for word in words_counts:
        words_counts[word] = filtered_words.count(word)

    return words_counts


def top_n_dict_occurance(dict_, top_n=65536):
    """
    Function top_n_dict_occurance() makes a list of tuple with top N items of inputed dict sorted by value in reverse
    :param dict_: dictionary to be sorted and sliced
    :param top_n: number of returned top items
    :type dict_: dict
    :type top_n: 
    :return: list of top_n sorted items
    :rtype: list
    """
    try:
        
        # make list from inputed dict
        list_to_sort = list(dict_.items())
        # sort by value desc
        list_to_sort.sort(key=lambda item: item[1], reverse=True)

        # return slice of top_n
        return list_to_sort[:top_n]

    except (TypeError, AttributeError):
        return []

def dict_weight(dict_):
    """
    Function dict_weight() returns a copy of inputed dictionary with values as original values weights in overall sum of values
    :param dict_: dictionary to be sorted and sliced
    :type dict_: dict
    :return: dictionary of key weights of inputed dict
    :rtype: dict
    """
    try:
        # try not modify incoming object:)
        result = dict_.copy()
        
        # sum values
        all_values_sum = sum(result.values())
        
        # calculate weight of each value
        for k,v in result.items():
            try:
                result[k] = int(100 * v / all_values_sum)
            except ZeroDivisionError:
                result[k] = 'NaN'
    
        return result

    except (TypeError, AttributeError):
        #if sum can't be calculated, than return dict with zeros
        return {}
    
    
def text_analizer(input_str):
    """
    Function text_analizer() analizes input text for words count, dictionary, frequency and top 3 words. Prints result to output.
    :param input_str: text string to analize words
    :type input_str: str
    :return: output of analize
    :rtype: str
    """

    try:
        words_counts = count_words(input_str)
        top_words = top_n_dict_occurance(words_counts, TOP_N_WORDS_OCCURANCE)
        word_freq = top_n_dict_occurance(dict_weight(words_counts))
    except Exception as err:
        print(err)
        return None
    
    # results formatting and output
    try:
        words_quantity = sum(words_counts.values())
    except AttributeError:
        words_quantity = 0
        
    text_dictionary = ', '.join(list(words_counts.keys()))
    keywords = ', '.join(['{0} - {1}'.format(w, c) for w, c in top_words])
    frequency = ', '.join(['{0} - {1}%'.format(w, f) for w, f in word_freq])

    output = f' words quantity: {words_quantity}\n text dictionary: {text_dictionary}\n keywords: {keywords}\n frequency: {frequency}'

    return output


def main():
    """
    Task 5 Text Analyzer 2.0

    Use your Task 4 to finish Task 5.

    Additional features:

    Module that provide a possibility to:
    -- Extract a text from text.txt file;
    -- Save results to results.txt file;
    Run your logic only if the main file was executed;
    Try to handle as much exceptions as possible.

    """
    def _load_from_file_(filename):

        try:
            with open(filename,'r') as file:
                text = file.read()

            return text

        except FileNotFoundError:
            print('There is no such file')
        except NameError:
            print('name is not applicable')
        # return nothing if file does not exist


    def _save_file_(filename, text):
        
        try:
            with open(filename,'w') as file:
                file.write(text)
                filename = file.name

            return filename

        except Exception as err:
            print(err)
            return None
        
    #repeats 3 times
    for try_cnt in range(3, 0, -1):

        start = input('Load from file or input manually?(load/input): ').lower().strip()
        
        if start not in {'load', 'input'}:
            # while try_cnt>0 print warning else print Goodbye
            print([f'Wrong answer! Type only options. You have {try_cnt - 1} tries','You didn\'t make choice. Goodbye!'][not bool(try_cnt - 1)])

            # Exit the programm
            if not (try_cnt - 1):
                return False
            
            continue

        elif start == 'input':

            text = input('Please insert text to analize: ')
            break

        else:

            text = _load_from_file_(input('Open filename: '))
            # If text not loaded then give a chance to input text from keyboard
            if text is None:
                continue
            
            break

    try:        

        analized_result = text_analizer(text)
        print(analized_result)

    except Exception as error:
        print(error)
        return False

    # Ask and save file
    while True:

        save_answer = input('Save result?(Y/N): ').lower().strip()

        if save_answer == 'y':
            
            filename = _save_file_(input('Save filename: '), analized_result)
            if filename:
                print(f'File {filename} successfully saved')

            return True

        elif save_answer == 'n':
            return print('Goodbye!')

        # IF ends with Return, so no need to make ELSE
        print(f'Wrong answer! Type only options')


# run program if main
if __name__ == '__main__':
    main()
    
