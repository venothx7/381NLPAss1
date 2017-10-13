import math


# reads in a file, Adds padding <s> and </s> , and lowercase
# then writes out the result to a newFile, Returns the newFile name
def pad_lower(fileName, newFile):
    word_count = wordCountDict(fileName)
    with open(fileName, 'r+') as f:
        with open(newFile, 'w+') as w:
            for line in f.readlines():
                w.write("<s> " + line.lower().strip() + " </s>\n")
    return newFile


# Add <s> and </s> to every sentence, and lowercase,
# replace words that occur once with <unk>, write it to outputfile
def unk_train(fileName, newFile):
    word_count = wordCountDict(fileName)
    with open(fileName, 'r+') as f:
        with open(newFile, 'w+') as w:
            for line in f.readlines():
                w.write("<s>")
                words = line.split()
                for word in words:
                    if word_count[word] != 1:
                        w.write(" " + word.lower().strip())
                    else:
                        w.write(" <unk>")
                w.write(" </s>\n")
    return newFile


# pad <s>, </s> and lowercase
# every word in test data and not in Train data needs to be replaced with <unk>
# writes it to a newFile, returns the newFile name
def unk_test(trainFile, testFile, newFile1):
    wordCountTrain = wordCountDict(trainFile)  # gets a dictionary of word count
    with open(testFile, 'r+') as f:  # open and read test file
        with open(newFile1, 'w+') as w:  # open a newfile to start writin
            for line in f.readlines():  # loop thru each line
                w.write("<s>")
                words = line.split()
                for word in words:
                    if word in wordCountTrain:
                        w.write(" " + word.lower().strip())
                    else:
                        w.write(" <unk>")
                w.write(" </s>\n")
    return newFile1


# prints a Dictionary  in a sorted and clear manner
def dictPrint(map):
    for key, val in sorted(map.items()):
        print("%s -->  %r" % (key, val))


# reads in a file, and creates a dictionary, Key=word type, Value= count of word type
# Returns a Dictionary of the word type counts,
def wordCountDict(fileName):
    counts = {}
    with open(fileName, 'r') as f:
        words = f.read().split()  # split the file at every whitespace
        for w in words:
            if w in counts:
                counts[w] += 1
            else:
                counts[w] = 1
    return counts


# reads a txt file, and gives a unigram model with prob
# Returns a Dictionary, Key= unigram word , Value= probability of that unigram word
def unigramModel(fileName):
    # print('Count of word types: ')
    # word_type_count(fileName)  # function gets a dictionary of the word type counts
    counts = {}  # a map that holds the count of the word
    total_count = 0  # num of words Tokens
    unigrammap = {}
    # reads training file, gets count of words and total count of words in file
    with open(fileName, 'r') as f:
        words = f.read().split()  # split the file at every whitespace
        total_count = len(words)  # gets count of words in the file
        # print('Number of Tokens in Unigram : ' + str(total_count))
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


# reads a file, gives the bigram words and its count, Ex. {'the dog' : 3}
# Returns a Dictionary: Key= bigram word , Value = count of the bigram word
def bigram_count(fileName):
    bigramCountDict = {}  # map tht holds the bigram counts
    with open(fileName, 'r') as f:
        lines = f.readlines()  # list of all the lines
        for line in lines:
            words = line.split()  # list of words in current line

            # loop thru the current list of words
            for i in range(len(words) - 1):
                bigram = words[i] + ' ' + words[i + 1]
                if bigram in bigramCountDict:
                    bigramCountDict[bigram] += 1
                else:
                    bigramCountDict[bigram] = 1

        return bigramCountDict


# reads a text file, gives the proability of bigram words
# returns a Dictionary: key = bigram Word,  value= probability of that bigram
def bigram_model_prob(fileName):
    # print('Count of Word Types: ')
    # word_type_count(fileName)
    print()
    bigram_prob = {}
    bigramCount = {}  # map tht holds the bigram counts
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
                if bigram in bigramCount:
                    bigramCount[bigram] += 1
                else:
                    bigramCount[bigram] = 1

                # Add word into count of words
                if words[i] in word_count:
                    word_count[words[i]] += 1
                else:
                    word_count[words[i]] = 1

    # loop thru bigram_count
    for key, count in sorted(bigramCount.items()):
        # st = '' + key
        word = ('' + key).split()
        context_word = word[0]
        prob = float(bigramCount[key]) / word_count[context_word]
        bigram_prob[key] = prob

    return bigram_prob


# reads a text file, gives probability of bigram words with Add-One Smoothing
# returns a Dictionary: key = bigram Word,  value= probability of that bigram
def bigram_smooth_model(fileName):
    bigram_prob = {}
    bigramCount = {}  # map tht holds the bigram counts
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
                if bigram in bigramCount:
                    bigramCount[bigram] += 1
                else:
                    bigramCount[bigram] = 1

                # Add word into count of words
                if words[i] in word_count:
                    word_count[words[i]] += 1
                else:
                    word_count[words[i]] = 1

    V = len(word_count)
    print()
    # loop thru bigramCount
    for key, count in sorted(bigramCount.items()):
        word = ('' + key).split()
        context_word = word[0]
        prob = (float(bigramCount[key] + 1)) / (word_count[context_word] + V)
        bigram_prob[key] = prob

    return bigram_prob


# returns a string,   P( sent )
def probPrint(str):
    return 'P(' + str + ')'


# ====================================================================================================================
# ====================================================================================================================
# Number 1
print('---------------------------------------------------------------------------------------------')
print('                 #1: word types in Training')


# prints the number of word types
def unique_words(fileName):
    processed_text = unk_train(fileName, 'modText.txt')
    count = wordCountDict(processed_text)  # gets diction of the word type counts
    return len(count)


wordTypeCount = unique_words('brown-train.txt')
print("After including padding symbols and unknown tokens also lowercase the text,\n"
      "the word types(unique words) is :  " + str(wordTypeCount))
print('---------------------------------------------------------------------------------------------')

# ====================================================================================================================
# ====================================================================================================================
# Number 2
print('---------------------------------------------------------------------------------------------')
print('                 #2: word tokens')


# returns the number of tokens in the text file
def word_tokens(fileName):
    with open(fileName, 'r') as f:
        words = f.read().split()  # split the file at every whitespace
        return len(words)


tokenCount = word_tokens('brown-train.txt')
print('Number of word tokens in Training corpus: ' + str(tokenCount))
print('---------------------------------------------------------------------------------------------')

# ***************************************************************************************************************
# ***************************************************************************************************************
# Number 3
print('---------------------------------------------------------------------------------------------')
print('                 #3: Percentage')


# Percentage = numTokens in Test but not in Train / # of Tokens in Test
# Percentage = numWord types in Test but not in Train / # of Word types in Test
# before mapping <unk>, but lowercased and padded <s> and </s>
def percent_type(trainFile, testFile1, testFile2):
    # pad <s> , </s> and lowercase both train and test file.
    processed_train = pad_lower(trainFile, 'modTrain.txt')
    processed_test1 = pad_lower(testFile1, 'modTest1.txt')
    processed_test2 = pad_lower(testFile2, 'modTest2.txt')

    # Get number of Tokens for both test files
    test1_tokenCount = word_tokens(processed_test1)
    test2_tokenCount = word_tokens(processed_test2)

    # Dictionaries that hold the word type and its count
    wordcount_train = wordCountDict(processed_train)
    wordcount_test1 = wordCountDict(processed_test1)
    wordcount_test2 = wordCountDict(processed_test2)

    # Number of word types in both Train and Test File
    train_WordCount = len(wordcount_train)
    test1_WordCount = len(wordcount_test1)
    test2_WordCount = len(wordcount_test2)

    test1_NotTokens = 0  # keeps count of tokens in test that did not occur in train
    test1_NotWords = 0  # keeps count of words in test that did not occur in train

    test2_NotTokens = 0  # keeps count of tokens in test that did not occur in train
    test2_NotWords = 0  # keeps count of words in test that did not occur in train
    for w, count in sorted(wordcount_test1.items()):  # loops thru testWordTypes
        if w not in wordcount_train:
            test1_NotWords += 1
            test1_NotTokens += count  # adds num of tokens of tht word

    for w, count in sorted(wordcount_test2.items()):  # loops thru testWordTypes
        if w not in wordcount_train:
            test2_NotWords += 1
            test2_NotTokens += count  # adds num of tokens of tht word

    print('Train: ' + ' WordType: ' + str(train_WordCount))
    print('Test1:  Tokens: ' + str(test1_tokenCount) + '  WordType: ' + str(
        test1_WordCount) + '    TokensInTest&NotTrain: ' + str(test1_NotTokens))
    print('Test2:  Tokens: ' + str(test2_tokenCount) + '  WordType: ' + str(
        test2_WordCount) + '    WordTypesInTest&NotTrain: ' + str(test1_NotWords))

    print()

    percTokens1 = round(100 * test1_NotTokens / test1_tokenCount, 2)
    percWord1 = round(100 * test1_NotWords / test1_WordCount, 2)
    percTokens2 = round(100 * test2_NotTokens / test2_tokenCount, 2)
    percWord2 = round(100 * test2_NotWords / test2_WordCount, 2)

    print('Number Tokens in Test but not in Train / total # of Tokens in Test :')
    print(testFile1 + ':   ' + str(percTokens1) + '%')
    print(testFile2 + ':   ' + str(percTokens2) + '%')

    print('Number word Types in Test but not in Train / total # of word types in Test :')
    print(testFile1 + ':   ' + str(percWord1) + '%')
    print(testFile2 + ':   ' + str(percWord2) + '%')


percent_type('brown-train.txt', 'brown-test.txt', 'learner-test.txt')
print('---------------------------------------------------------------------------------------------')

# ***************************************************************************************************************
# ***************************************************************************************************************
# Number 4
print('---------------------------------------------------------------------------------------------')
print('                 #4: Bigram Percentage')


# #4
def percent_bigram(trainFile, testFile1, testFile2):
    # pad <s> , </s> and lowercase both train and test file.
    # replace words with <unk> that occurred once in training
    # replaced words with <unk> in Test, if the word is not in train
    processed_train = unk_train(trainFile, 'modTrain.txt')
    processed_test1 = unk_test(trainFile, testFile1, 'modTest1.txt')
    processed_test2 = unk_test(trainFile, testFile2, 'modTest2.txt')

    # Get number of Tokens for both test files
    test1_tokenCount = word_tokens(processed_test1)
    test2_tokenCount = word_tokens(processed_test2)

    # Dictionary of bigram models for both train and test
    wordcount_train = bigram_count(processed_train)
    wordcount_test1 = bigram_count(processed_test1)
    wordcount_test2 = bigram_count(processed_test2)

    # number of word types in both Train and test file
    train_WordCount = len(wordcount_train)
    test1_WordCount = len(wordcount_test1)
    test2_WordCount = len(wordcount_test2)

    test1_NotTokens = 0  # keeps count of tokens in test that did not occur in train
    test1_NotWords = 0  # keeps count of words in test that did not occur in train

    test2_NotTokens = 0  # keeps count of tokens in test that did not occur in train
    test2_NotWords = 0  # keeps count of words in test that did not occur in train

    for w, count in sorted(wordcount_test1.items()):  # loops thru testWordTypes
        if w not in wordcount_train:
            test1_NotWords += 1
            test1_NotTokens += count  # adds num of tokens of tht word

    for w, count in sorted(wordcount_test2.items()):  # loops thru testWordTypes
        if w not in wordcount_train:
            test2_NotWords += 1
            test2_NotTokens += count  # adds num of tokens of tht word
    print('Train: ' + ' WordType: ' + str(train_WordCount))
    print('Test1:  Tokens: ' + str(test1_tokenCount) + '  WordType: ' + str(
        test1_WordCount) + '    TokensInTest&NotTrain: ' + str(test1_NotTokens))
    print('Test2:  Tokens: ' + str(test2_tokenCount) + '  WordType: ' + str(
        test2_WordCount) + '    WordTypesInTest&NotTrain: ' + str(test1_NotWords))

    print()

    percTokens1 = round(100 * test1_NotTokens / test1_tokenCount, 2)
    percWord1 = round(100 * test1_NotWords / test1_WordCount, 2)
    percTokens2 = round(100 * test2_NotTokens / test2_tokenCount, 2)
    percWord2 = round(100 * test2_NotWords / test2_WordCount, 2)

    print('Number Tokens in Test but not in Train / total # of Tokens in Test :')
    print(testFile1 + ':   ' + str(percTokens1) + '%')
    print(testFile2 + ':   ' + str(percTokens2) + '%')

    print('Number word Types in Test but not in Train / total # of word types in Test :')
    print(testFile1 + ':   ' + str(percWord1) + '%')
    print(testFile2 + ':   ' + str(percWord2) + '%')


percent_bigram('brown-train.txt', 'brown-test.txt', 'learner-test.txt')
print('---------------------------------------------------------------------------------------------')

# ***************************************************************************************************************
# ***************************************************************************************************************
# Number 5
print('---------------------------------------------------------------------------------------------')
print('                 #5: Log Probability')

sentence1 = 'He was laughed off the screen .'
sentence2 = 'There was no compulsion behind them .'
sentence3 = 'I look forward to hearing your reply .'


# ignoring lowercase, and padding, getting the log probabilities
def log_unigram(trainFile, sent1, sent2, sent3):
    print()
    print('#5: Log Probabilities of the sentences under the Unigram Model')
    uniProbDict = unigramModel(trainFile)

    # input the sentence that needs to compute probability a log probability
    # prints the probability and the log of that probability
    def probSent(sent):
        s1 = sent.split()
        print(probPrint(sent) + ' = ')
        temp = ''
        for w in s1:
            if w == s1[-1]:
                temp += (probPrint(w) + ' = ')
            else:
                temp += (probPrint(w) + ' * ')
        print(temp)
        temp = ''
        prob = 1
        for w in s1:
            if w in uniProbDict:
                temp += (probPrint(w) + '= ' + str(uniProbDict[w]) + ',  ')
                prob *= uniProbDict[w]
            else:
                temp += (probPrint(w) + '= 0, ')
                # prob *= 0

        print(temp)
        print(probPrint(sent) + ' = ' + str(float(prob)))
        logProb = math.log(prob, 2)
        print('Log of ' + probPrint(sent) + ' = ' + str(logProb))

    probSent(sent1)
    print()
    probSent(sent2)
    print()
    probSent(sent3)


log_unigram('brown-train.txt', sentence1, sentence2, sentence3)


# ignoring lowercase, and padding, getting the log probabilities
def log_bigram(trainFile, sent1, sent2, sent3):
    print('\n\n')
    print('#5: Log Probabilities of the sentences under the Bigram Model')
    biProbDict = bigram_model_prob(trainFile)
    biProbDict.update(unigramModel(trainFile))  # adds the prob of the single words

    def probSent(sent):
        print(probPrint(sent) + ' = ')
        s1 = sent.split()
        temp = str(probPrint(s1[0])) + ' '
        for i in range(len(s1) - 1):
            temp += '* ' + probPrint(s1[i + 1] + '|' + s1[i]) + ' '
        print(temp)
        prob = 1
        if s1[0] in biProbDict:
            temp = str(probPrint(s1[0])) + '=' + str(biProbDict[s1[0]])
            prob *= biProbDict[s1[0]]
        else:
            temp = str(probPrint(s1[0])) + '= 0'
            prob *= 0

        for i in range(len(s1) - 1):
            bigram = s1[i] + ' ' + s1[i + 1]
            if bigram in biProbDict:
                temp += '  ' + probPrint(s1[i + 1] + '|' + s1[i]) + '=' + str(biProbDict[bigram]) + ' '
                prob *= biProbDict[bigram]
            else:
                temp += '  ' + probPrint(s1[i + 1] + '|' + s1[i]) + '= 0'
                prob *= 0
        print(temp)
        print(probPrint(sent) + ' = ' + str(float(prob)))
        if prob != 0:
            logProb = math.log(prob, 2)
            print('Log of ' + probPrint(sent) + ' = ' + str(logProb))
        else:
            print('Log of ' + probPrint(sent) + ' = undefined')

    probSent(sent1)
    print()
    probSent(sent2)
    print()
    probSent(sent3)


log_bigram('brown-train.txt', sentence1, sentence2, sentence3)


# ignoring lowercase, and padding, getting the log probabilities
def log_smoothBigram(trainFile, sent1, sent2, sent3):
    print('\n\n')
    print('#5: Log Probabilities of the sentences under the Bigram Model with Add-One Smoothing')

    biProbDict = bigram_smooth_model(trainFile)
    biProbDict.update(unigramModel(trainFile))  # adds the prob of the single words

    def probSent(sent):
        print(probPrint(sent) + ' = ')
        s1 = sent.split()
        temp = str(probPrint(s1[0])) + ' '
        for i in range(len(s1) - 1):
            temp += '* ' + probPrint(s1[i + 1] + '|' + s1[i]) + ' '
        print(temp)
        prob = 1
        if s1[0] in biProbDict:
            temp = str(probPrint(s1[0])) + '=' + str(biProbDict[s1[0]])
            prob *= biProbDict[s1[0]]
        else:
            temp = str(probPrint(s1[0])) + '= 0'
            prob *= 0

        for i in range(len(s1) - 1):
            bigram = s1[i] + ' ' + s1[i + 1]
            if bigram in biProbDict:
                temp += '  ' + probPrint(s1[i + 1] + '|' + s1[i]) + '=' + str(biProbDict[bigram]) + ' '
                prob *= biProbDict[bigram]
            else:
                temp += '  ' + probPrint(s1[i + 1] + '|' + s1[i]) + '= 0'
                prob *= 0
        print(temp)
        print(probPrint(sent) + ' = ' + str(float(prob)))
        if prob != 0:
            logProb = math.log(prob, 2)
            print('Log of ' + probPrint(sent) + ' = ' + str(logProb))
        else:
            print('Log of ' + probPrint(sent) + ' = undefined')

    probSent(sent1)
    print()
    probSent(sent2)
    print()
    probSent(sent3)


log_smoothBigram('brown-train.txt', sentence1, sentence2, sentence3)

# log_bigram('brown-train.txt')
# log_smoothBigram('brown-train.txt')


# printMap(bigram_model('Test.txt'))
# unk_test('Test.txt', 'new.txt', 'temp1.txt')
# percent_bigram('Test.txt', 'new.txt', 'temp1.txt')
# log_unigram('Test.txt')
print()
# printMap(word_type_count('Test.txt'))
# printMap(unigramModel('Test.txt'))
