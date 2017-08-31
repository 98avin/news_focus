from nltk.tokenize import RegexpTokenizer

def build_dict():
	file = open("application/master_count.txt");
	stringFile = file.read()
	tokenizer = RegexpTokenizer(r'[A-Za-z.]+')
	stringArray = tokenizer.tokenize(stringFile) #remove non alpha-numeric

	currentPaper = ""
	wordDict = {}

	for x in stringArray:
		if(x == '.'):
			continue
		if(x[len(x)-4:] == '.txt'):
			currentPaper = x[0:len(x)-4]
			wordDict[currentPaper] = []
		else:
			wordDict[currentPaper].append(x)

	return wordDict