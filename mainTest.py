# get count of tokens,
# Returns a Dictionary
def freq(fileName):
    counts = {}
    with open(fileName, 'r') as f:
        words = f.read().split()  # split the file at every whitespace
        for w in words:
            if w in counts:
                counts[w] += 1
            else:
                counts[w] = 1
    # prints list in a ordered manner
    for key, val in sorted(counts.items()):
        print("%s --> %r" % (key, val))
    return counts


# Add <s> and </s> to ever sentence, lowercase, writes newfile
def pre_process(fileName, newFile):
    with open(fileName, 'r+') as f:
        with open(newFile, 'w+') as w:
            for line in f.readlines():
                w.write(" <s> " + line.lower().strip() + " </s> \n")


# takes a txt file, and gives a unigram model with prob, output into a file
def unigramModel(fileName):
    counts = {}  # a map that holds the count of the word
    total_count = 0  # num of words in the file

    # reads training file, gets count of words and total count of words in file
    with open(fileName, 'r') as f:
        words = f.read().split()  # split the file at every whitespace
        total_count = len(words)  # gets count of words in the file
        for w in words:
            if w in counts:
                counts[w] += 1
            else:
                counts[w] = 1

    with open('unigramMLE.txt', 'w+') as f:
        for word, count in sorted(counts.items()):
            prob = float(counts[word]) / total_count
            f.write(word + ' ------> ' + str(prob) + "\n")


# gets count of lines,Returns an int
def count_lines(fileName):
    bigram_list = []
    bigram_map = {}
    with open(fileName, 'r') as f:
        lines = f.readlines()  # list of all the lines
        for line in lines:
            words = line.split()  # list of words in current line


            # loop thru the current list of words
            for i in range(len(words) - 1):
                bigram = words[i] + ' ' + words[i + 1]
                if bigram in bigram_map:
                    bigram_map[bigram] += 1
                else:
                    bigram_map[bigram] = 1
                bigram_list.append((words[i], words[i + 1]))

                # prints list in a ordered manner
    for key, val in sorted(bigram_map.items()):
        print("[ %s ]--> %r" % (key, val))
    print()
    return bigram_list


# takes a txt file, and gives a bigram model with prob, output into a file for i in range(len(words) - 1):
def bigramModel(fileName):
    counts = {};
    context_counts = {}
    bigram_list = []

    with open(fileName, 'r') as f:
        lines = f.readlines()  # a list of all the lines in file
        for line in lines:
            words = line.split()  # list of words in the current line
            bigram_list += zip(words, words[1:])
    return bigram_list


# print(len(freq('tempTexy.txt').keys()))
# unigramModel('tempTexy.txt')

print(count_lines('tempTexy.txt'))
print(bigramModel('tempTexy.txt'))


# dict1 = {'Jack': 15, 'Bob': 22}
# dict1['Bob'] += 1 # increase counter by 1
# dict1['Joe'] = 1 # assign a new key with value
# print(dict1.get('Bob')) # gets value in dict
# print("ack" in dict1) # checks if it is in dictionary T/F
# print(dict1)
# dict2 = {'a': {'count': 2, 'prob': .666}, 'b': {'count': 1, 'prob': .0345}}
# print(dict2)
