import os
import argparse
import re
import time


def get_lines(fp, line_numbers):
    return (x for i, x in enumerate(fp) if i in line_numbers)

def extract_collection(file_name):
    # Create the 'collection_original' and 'collection_no_stopwords' sub-folder if it doesn't exist
    if not os.path.exists('collection_original'):
        os.makedirs('collection_original', mode=0o777)
    if not os.path.exists('collection_no_stopwords'):
        os.makedirs('collection_no_stopwords', mode=0o777)
    file_names = []
    with open("aesopa10.txt", "r") as f:
        lines = get_lines(f, 307)
        text = f.read()
        formatted_text = text.replace("\n\n\n\n", "\n Chapter")
        split_text = formatted_text.split("Chapter")
        count = 0
        for i in split_text:
            name = i.split("\n\n\n")
            count = count + 1
            form_name = str(count).zfill(2) + '_' + name[0].replace(".", "_").replace("  ", "").replace(" ",
                                                                                                        "_").replace(
                "'", "").replace("?", "").replace("--", "").replace("-", "_").replace(",", "").lower()
            with open(f"./collection_original/{form_name}.txt", "a+") as f:
                f.write(i)
                file_names.append(form_name)
    stop_word_removal(file_names)
    print("Extraction completed.")


def stem_word(word):
   """
   Apply Porter stemming algorithm to a given word.
   """
   stem = word

   # Step 1a
   if stem.endswith("sses"):
       stem = stem[:-4]
   elif stem.endswith("ies"):
       stem = stem[:-3]
   elif stem.endswith("ss"):
       stem = stem
   elif stem.endswith("s"):
       stem = stem[:-1]

   # Step 1b
   if re.search(r"[aeiouy]", stem):
       if stem.endswith("eed"):
           stem = stem[:-1]
       elif stem.endswith(("ed", "ing")):
           stem_candidate = stem[:-2]
           if re.search(r"[aeiouy]", stem_candidate):
               stem = stem_candidate
               if stem.endswith(("at", "bl", "iz")):
                   stem += "e"
               elif stem.endswith((stem[-1], stem[-2])) and not re.search(r"[aeiouy]", stem[:-2]):
                   stem = stem[:-1]
                   if stem.endswith("l") and len(stem) >= 3 and re.search(r"[aeiouy]", stem[:-1]):
                       stem = stem[:-1]

   # Step 1c
   if re.search(r"[aeiouy]", stem):
       if stem.endswith("y"):
           stem_candidate = stem[:-1]
           if re.search(r"[aeiouy]", stem_candidate):
               stem = stem_candidate

   # Step 2
   if re.search(r"[aeiouy]", stem):
       stem_candidate = stem
       if stem_candidate.endswith("ational"):
           stem = stem_candidate[:-5] + "e"
       elif stem_candidate.endswith("tional"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("enci"):
           stem = stem_candidate[:-1] + "e"
       elif stem_candidate.endswith("anci"):
           stem = stem_candidate[:-1] + "e"
       elif stem_candidate.endswith("izer"):
           stem = stem_candidate[:-1]
       elif stem_candidate.endswith("abli"):
           stem = stem_candidate[:-1] + "e"
       elif stem_candidate.endswith("alli"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("entli"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("eli"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("ousli"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("ization"):
           stem = stem_candidate[:-5] + "e"
       elif stem_candidate.endswith("ation"):
           stem = stem_candidate[:-3] + "e"
       elif stem_candidate.endswith("ator"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("alism"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("iveness"):
           stem = stem_candidate[:-4]
       elif stem_candidate.endswith("fulness"):
           stem = stem_candidate[:-4]
       elif stem_candidate.endswith("ousness"):
           stem = stem_candidate[:-4]
       elif stem_candidate.endswith("aliti"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("iviti"):
           stem = stem_candidate[:-3] + "e"
       elif stem_candidate.endswith("biliti"):
           stem = stem_candidate[:-5] + "le"

   # Step 3
   if re.search(r"[aeiouy]", stem):
       stem_candidate = stem
       if stem_candidate.endswith("icate"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("ative"):
           stem = stem_candidate[:-5]
       elif stem_candidate.endswith("alize"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("iciti"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("ical"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("ful"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("ness"):
           stem = stem_candidate[:-4]

   # Step 4
   if re.search(r"[aeiouy]", stem):
       stem_candidate = stem
       if stem_candidate.endswith("al"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("ance"):
           stem = stem_candidate[:-4]
       elif stem_candidate.endswith("ence"):
           stem = stem_candidate[:-4]
       elif stem_candidate.endswith("er"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("ic"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("able"):
           stem = stem_candidate[:-4]
       elif stem_candidate.endswith("ible"):
           stem = stem_candidate[:-4]
       elif stem_candidate.endswith("ant"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("ement"):
           stem = stem_candidate[:-5]
       elif stem_candidate.endswith("ment"):
           stem = stem_candidate[:-4]
       elif stem_candidate.endswith("ent"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith(("ion", "sion", "tion")):
           stem = stem_candidate[:-3]
           if stem.endswith("t") and stem[-2] in "st":
               stem = stem[:-1]
       elif stem_candidate.endswith("ou"):
           stem = stem_candidate[:-2]
       elif stem_candidate.endswith("ism"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("ate"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("iti"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("ous"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("ive"):
           stem = stem_candidate[:-3]
       elif stem_candidate.endswith("ize"):
           stem = stem_candidate[:-3]

   # Step 5a
   if re.search(r"[aeiouy]", stem):
       stem_candidate = stem
       if stem_candidate.endswith("e"):
           stem = stem_candidate[:-1]
           if len(stem) >= 2 and not re.search(r"[aeiouy]", stem):
               stem = stem_candidate

   # Step 5b
   if re.search(r"[aeiouy]", stem):
       stem_candidate = stem
       if len(stem_candidate) >= 2 and stem_candidate[-1] == stem_candidate[-2] and not re.search(r"[aeiouy]", stem_candidate[:-2]):
           stem = stem_candidate[:-1]

   return stem


def inverted_list(query,folder_type):

    # Construct an inverted index
    # here as a Python dictionary for ease of interpretability

    inverted_index = {}
    i = 0
    result = list()
    file_name_list = {}
    search_directory = 'collection_original' if folder_type == 'original' else 'collection_no_stopwords'
    if folder_type == 'original':
        for file_name in os.listdir(search_directory):
            file_path = os.path.join(search_directory, file_name)
            with open(file_path, 'r') as file:
                content = file.read()
                for term in content.split():
                    if term in inverted_index:
                        inverted_index[term].add(i)
                    else:
                        inverted_index[term] = {i}
            file_name_list[i] = file_name
            i = i+1

    print('file_name_list',file_name_list)
    # Splitting the query
    if "-" in query:
        posting_list1 = []
        query_list = query.split('-')
        for key, val in inverted_index.items():

            # checking whether the key value of the iterator is equal to the above-entered key
            if key in query_list[1]:
                posting_list1 = list(inverted_index[key])

        result = not_postings(sorted(posting_list1))
    elif '&' in query:
        posting_list1 = []
        posting_list2 = []
        query_list = query.split('&')
        print('query list',query_list)
        print('query_list[0]',query_list[0])
        print('query_list[1]', query_list[1])
        for key, val in inverted_index.items():

            # checking whether the key value of the iterator is equal to the above-entered key
            if key in query_list[0]:
                #print(val)
                #print(key)
                posting_list1 = list(inverted_index[key])
                #print(posting_list1)
        for key, val in inverted_index.items():
            #print('query_list[1]', query_list[1])
            # checking whether the key value of the iterator is equal to the above-entered key
            if key in query_list[1]:
                #print(val)
                #print(key)
                posting_list2 = list(inverted_index[key])
                #print(posting_list2)

        result = and_postings(sorted(posting_list1), sorted(posting_list2))
    elif '|' in query:
        print(" OR operation ")
        posting_list1 = []
        posting_list2 = []
        query_list = query.split('|')
        # Traversing in the key-value pairs of the dictionary using the items() function
        for key, val in inverted_index.items():

            # checking whether the key value of the iterator is equal to the above-entered key
            if key in query_list[0]:
                print(val)
                posting_list1 = list(inverted_index[key])
                print(posting_list1)
            if key in query_list[1]:
                print(val)
                posting_list2 = list(inverted_index[key])
                print(posting_list2)
        result = or_postings(sorted(posting_list1), sorted(posting_list2))
    else:
        print(" No operator match")
    print('result :', result)
    result_list = []
    for i in result:
        print(file_name_list[i])


def or_postings(posting1, posting2):
    p1 = 0
    p2 = 0
    result = list()
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:
            result.append(posting1[p1])
            p1 += 1
            p2 += 1
        elif posting1[p1] > posting2[p2]:
            result.append(posting2[p2])
            p2 += 1
        else:
            result.append(posting1[p1])
            p1 += 1
    while p1 < len(posting1):
        result.append(posting1[p1])
        p1 += 1
    while p2 < len(posting2):
        result.append(posting2[p2])
        p2 += 1
    return result

def and_postings(posting1, posting2):
    print('posting_list1', posting1)
    print('posting_list2', posting2)
    p1 = 0
    p2 = 0
    result = list()
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:
            result.append(posting1[p1])
            p1 += 1
            p2 += 1
        elif posting1[p1] > posting2[p2]:
            p2 += 1
        else:
            p1 += 1
    return result

def not_postings(posting):
    result = list()
    i = 0
    for item in posting:
        while i < item:
            result.append(i)
            i += 1
        else:
            i += 1
    else:
        while i < 82:
            result.append(i)
            i += 1
    return result

def linearSearch(word,model, operator,folder_type):
    matching_file_names = []
    #print('word :', word)
    search_directory = 'collection_original' if folder_type == 'original' else 'collection_no_stopwords'
    if folder_type == 'original':
        if 'stemming' in operator:
            keywords = word.lower().split()

            stemmed_keywords = [stem_word(keyword) for keyword in keywords]

            # Perform linear search
            matching_files = []
            for file_name in os.listdir(search_directory):
                file_path = os.path.join(search_directory, file_name)
                with open(file_path, 'r') as file:
                    content = file.read().lower()
                    if all(stemmed_keyword in content for stemmed_keyword in stemmed_keywords):
                        matching_files.append((file_name,
                                               stemmed_keywords))  # Include the matching search words

            # Print the matching file names and search words
            for file_name, search_words in matching_files:
                print(f"{file_name}")
        else:
            if 'and' in operator:
                for file_name in os.listdir(search_directory):
                    file_path = os.path.join(search_directory, file_name)
                    with open(file_path, 'r') as file:
                        content = file.read()
                        #print('string search', word[0],word[1])
                        if (re.search(r'\b{}\b'.format(word[0]), content) or re.search(r'\b{}\b'.format(word[0].capitalize()),
                                                                                   content )) and (re.search(r'\b{}\b'.format(word[1]), content) or re.search(r'\b{}\b'.format(word[1]), content)):
                            matching_file_names.append(file_name)
                            print(file_name)
            elif 'or' in operator:
                for file_name in os.listdir(search_directory):
                    file_path = os.path.join(search_directory, file_name)
                    with open(file_path, 'r') as file:
                        content = file.read()
                        if (re.search(r'\b{}\b'.format(word[0]), content) or re.search(r'\b{}\b'.format(word[0].capitalize()),
                                                                                   content)) or (re.search(r'\b{}\b'.format(word[1]), content) or re.search(r'\b{}\b'.format(word[1]), content)):
                            matching_file_names.append(file_name)
                            print(file_name)
            elif 'not' in operator:
                for file_name in os.listdir(search_directory):
                    file_path = os.path.join(search_directory, file_name)
                    with open(file_path, 'r') as file:
                        content = file.read()
                        if not ( re.search(r'\b{}\b'.format(word[1]), content) or re.search(r'\b{}\b'.format(word[1].capitalize()),
                                                                                   content)) :
                            matching_file_names.append(file_name)
                            print(file_name)
    else:
        for file_name in os.listdir(search_directory):
            file_path = os.path.join(search_directory, file_name)
            with open(file_path, 'r') as file:
                content = file.read()
                if re.search(r'\b{}\b'.format(word), content) or re.search(r'\b{}\b'.format(word.capitalize()), content):
                    matching_file_names.append(file_name)
                    print(file_name)
        if len(matching_file_names) == 0:
            print("No documents found")

def stop_word_removal(file_names):
    stop_words_list = set()
    with open("englishST.txt", "r") as fp:
        stop_words = fp.read()
        stop_words_list = stop_words.split("\n")
    for i in file_names:
        with open(f"./collection_original/{i}.txt", "r") as f:
            text = f.read()
            tokenized_words = text.split()
            tokenized_words_without_stop_words = []
            for word in tokenized_words:
                if word not in stop_words_list:
                    tokenized_words_without_stop_words.append(word)
            with open(f"./collection_no_stopwords/{i}.txt", "a+") as f1:
                f1.write(str(tokenized_words_without_stop_words))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--extract-collection', metavar='FILE_NAME', help='Calls document extraction on FILE_NAME')
    parser.add_argument('--query', type=str, help='enter the string to searched')
    parser.add_argument('--model', choices=['bool'], help='Sets the model to Boolean')
    parser.add_argument('--search-mode', choices=['linear','inverted'], help='Sets the search mode to linear')
    parser.add_argument('--documents', choices=['original', 'no_stopwords'], help='Specifies the source documents for the search')
    parser.add_argument('--stemming', action='store_true',help='Specifies whether words in query and documents should be stemmed')
    args = parser.parse_args()
    if args.extract_collection:
        file_name = args.extract_collection
        if os.path.isfile(file_name):
            extract_collection(file_name)
        else:
            print("File not found.")
    elif args.stemming:
        st = time.time()
        linearSearch(args.query, args.model,'stemming',args.documents)
        et = time.time()
    elif args.query:
        st = time.time()
        query = args.query
        model = args.model
        search_mode = args.search_mode
        documents = args.documents
        #linearSearch(query, model, search_mode, documents)
        if 'linear' in search_mode:
            if "-" in query:
                query_list = query.split('-')
                linearSearch(query_list, model, 'not', documents)
            elif '&' in query:
                query_list = query.split('&')
                linearSearch(query_list, model, 'and', documents)
            elif '|' in query:
                query_list = query.split('|')
                linearSearch(query_list, model, 'or', documents)
        else:
            inverted_list(query,documents)
        et = time.time()
    else:
        print("No command-line parameter provided.")
    elapsed_time = et - st
    print('T=', (elapsed_time) / 1000, 2, 'ms')
