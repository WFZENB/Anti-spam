import analyzer

filename = 'dict.txt'


def read():
    analyzer.unique_words = {}
    f = open(filename, 'r')
    for i, line in enumerate(f):
        if i == 0:
            analyzer.spam_words_count  = int(line.split()[1])
        elif i == 1:
            analyzer.other_words_count = int(line.split()[1])
        elif i == 2:
            analyzer.spam_texts_count  = int(line.split()[1])
        elif i == 3:
            analyzer.other_texts_count = int(line.split()[1])
        else:
            line = line.split()
            analyzer.unique_words[line[0]] = [int(line[1]), int(line[2])]
    f.close()


def write():
    f = open(filename, 'w')
    f.write('spam_words_count '  + str(analyzer.spam_words_count)  + '\n')
    f.write('other_words_count ' + str(analyzer.other_words_count) + '\n')
    f.write('spam_texts_count '  + str(analyzer.spam_texts_count)  + '\n')
    f.write('other_texts_count ' + str(analyzer.other_texts_count) + '\n')
    for word_line in analyzer.unique_words:
        f.write(word_line + ' ' + str(analyzer.unique_words[word_line][0]) + ' ' + str(analyzer.unique_words[word_line][1]) + '\n')
    f.close()
