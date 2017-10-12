# prints a map ina certain way, sorted
def printMap(map):
    for key, val in sorted(map.items()):
        print("%s --> %r" % (key, val))


# get count of tokens,
# Returns a Dictionary of the word type counts, aslo prints it
def word_type_count(fileName):
    counts = {}
    with open(fileName, 'r') as f:
        words = f.read().split()  # split the file at every whitespace
        for w in words:
            if w in counts:
                counts[w] += 1
            else:
                counts[w] = 1

    return counts


# Add <s> and </s> to ever sentence, lowercase,
# replace words occuring once with <unk>, write it to outputfile
def pre_process(fileName, newFile):
    word_count = word_type_count(fileName)
    with open(fileName, 'r+') as f:
        with open(newFile, 'w+') as w:
            for line in f.readlines():
                w.write("<s>")
                words = line.split()
                for word in words:
                    if word_count[word] != 1:
                        w.write(" " + word.lower())
                    else:
                        w.write(" <unk>")
                w.write(" </s>\n")
    return newFile

def pad_lower(fileName,newFile):
    word_count = word_type_count(fileName)
    with open(fileName, 'r+') as f:
        with open(newFile, 'w+') as w:
            for line in f.readlines():
                w.write(" " + line.lower() + " </s>\n")
    return newFile

# prints the number of word types
def unique_words(fileName):
    count = word_type_count(fileName)
    print(len(count))
    uniq_num = len(count)
    print("After including padding symbols and unknown tokens also lowercase the text,\n"
          "the word types(unique words) is :  " + str(uniq_num))


# prints the number of tokens,
def word_tokens(fileName):
    count = 0
    with open(fileName, 'r') as f:
        words = f.read().split()  # split the file at every whitespace
        count = len(words)
        print("Number of tokens in the training corpus without including padding and  <unk>: " + str(count))
        return count


def percent_tokens(trainFile, testFile):
    print()
    padded_file= pad_lower(trainFile, "new1.txt")
    print()



word_tokens('brown-train.txt')
unique_words(pre_process('brown-train.txt', 'new.txt'))


# takes a txt file, and gives a unigram model with prob, output into a file
def unigramModel(fileName):
    print('Count of word types: ')
    word_type_count(fileName)
    print()
    counts = {}  # a map that holds the count of the word
    total_count = 0  # num of words Tokens
    unigrammap = {}
    # reads training file, gets count of words and total count of words in file
    with open(fileName, 'r') as f:
        words = f.read().split()  # split the file at every whitespace
        total_count = len(words)  # gets count of words in the file
        print('Number of tokens: ' + str(total_count))
        for w in words:
            if w in counts:
                counts[w] += 1
            else:
                counts[w] = 1
        # loop thru
        for word, count in sorted(counts.items()):
            prob = float(counts[word]) / total_count
            unigrammap[word] = prob

    # this writes the prob into a file
    # with open('unigramMLE.txt', 'w+') as f:
    #     for word, count in sorted(counts.items()):
    #         prob = float(counts[word]) / total_count
    #         unigrammap[word] = prob
    #         f.write(word + ' ------> ' + str(prob) + "\n")
    return unigrammap


# printMap(unigramModel('Test.txt'))


# Returns a dictionary with the bigrams and its probablity
def bigram_model(fileName):
    print('Count of Word Types: ')
    word_type_count(fileName)
    print()
    bigram_prob = {}
    bigram_count = {}  # map tht holds the bigram counts
    word_count = {}  # count of the word types
    with open(fileName, 'r') as f:
        lines = f.readlines()  # list of all the lines
        for line in lines:
            words = line.split()  # list of words in current line

            if words[-1] in word_count:
                word_count[words[-1]] += 1
            else:
                word_count[words[-1]] = 1

            # loop thru the current list of words
            for i in range(len(words) - 1):
                bigram = words[i] + ' ' + words[i + 1]
                if bigram in bigram_count:
                    bigram_count[bigram] += 1
                else:
                    bigram_count[bigram] = 1

                # Add word into count of words
                if words[i] in word_count:
                    word_count[words[i]] += 1
                else:
                    word_count[words[i]] = 1

    # loop thru bigram_count
    for key, count in sorted(bigram_count.items()):
        # st = '' + key
        word = ('' + key).split()
        context_word = word[0]
        prob = float(bigram_count[key]) / word_count[context_word]
        bigram_prob[key] = prob

    # prob = float(counts[word]) / total_count
    # unigrammap[word] = prob

    print('Count of bigrams: ')
    # #prints list in a ordered manner
    for key, val in sorted(bigram_count.items()):
        print("[ %s ]--> %r" % (key, val))
    print()
    return bigram_prob


def bigram_smooth_model(fileName):
    bigram_prob = {}
    bigram_count = {}  # map tht holds the bigram counts
    word_count = {}  # count of the word types
    V = 0  # number of word types
    with open(fileName, 'r') as f:
        lines = f.readlines()  # list of all the lines
        for line in lines:
            words = line.split()  # list of words in current line

            if words[-1] in word_count:
                word_count[words[-1]] += 1
            else:
                word_count[words[-1]] = 1

            # loop thru the current list of words
            for i in range(len(words) - 1):
                bigram = words[i] + ' ' + words[i + 1]
                if bigram in bigram_count:
                    bigram_count[bigram] += 1
                else:
                    bigram_count[bigram] = 1

                # Add word into count of words
                if words[i] in word_count:
                    word_count[words[i]] += 1
                else:
                    word_count[words[i]] = 1

    V = len(word_count)
    print('3/18 = ' + str(float(3 / 18)))
    print('V= ' + str(V))
    print('Count of tokens: ')
    # prints list in a ordered manner
    for key, val in sorted(bigram_count.items()):
        print("[ %s ]--> %r" % (key, val))

    print()
    # loop thru bigram_count
    for key, count in sorted(bigram_count.items()):
        # st = '' + key
        word = ('' + key).split()
        context_word = word[0]
        prob = (float(bigram_count[key] + 1)) / (word_count[context_word] + V)
        bigram_prob[key] = prob

    return bigram_prob

# printMap(bigram_model('Test.txt'))
# printMap(unigramModel('Test.txt'))

# count_lines('tempTexy.txt')


# takes a txt file, and gives a bigram model with prob, output into a file for i in range(len(words) - 1):


# print(len(freq('tempTexy.txt').keys()))
# unigramModel('tempTexy.txt')

# print(count_lines('tempTexy.txt'))
# print(bigramModel('tempTexy.txt'))


# dict1 = {'Jack': 15.000000000, 'Bob': 22.9900877}
# print(dict1)
# prob = float(5)/27
#
# # dict1['Bob'] += 1 # increase counter by 1
# dict1['Joe'] = prob # assign a new key with valu
#
# print(dict1)


# print(dict1.get('Bob')) # gets value in dict
# print("ack" in dict1) # checks if it is in dictionary T/F
# print(dict1)
# dict2 = {'a': {'count': 2, 'prob': .666}, 'b': {'count': 1, 'prob': .0345}}
# print(dict2)
