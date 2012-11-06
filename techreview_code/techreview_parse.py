import numpy as N
import pylab as P
import nltk
import re
from textutils_nltk import *


def rankorder(x):
	x1 = list(N.sort(x))
	x1.reverse()
	y1 = range(1,len(x1)+1)
	return x1,y1

def clean(html):
	try:
		start = re.search('<p>',html)
		dummy = start.start()
	except AttributeError:
		start = re.search('<p style="text-indent: 2em;">',html)
		print start
	end = re.search('<a name="comments"></a>',html)
	html=html[start.start():end.start()]
	#html=re.findall('<P>.*</P>',html)
	html =re.sub('<.*?>',' ',html)
	#html =re.sub('>Story continues .*?"afteradbody"></a>',' ',html)
	return html

#branches = ["computing/","web/"]
branches = ["computing/","web/","communications/","/energy"]

folder = "data2/" #%s" %branches[0]

cw = open("words/cwords2",'r')
cwords = cw.read()
cwords = nltk.word_tokenize(cwords)




q=[-2.,-1.,0.,1.,2.]
#files=N.arange(20000,25000)


files = os.listdir("data2")

H = N.zeros([len(files),len(q)])
#H=[]

num_keywords = 100
w = N.zeros([len(files),num_keywords])
f = N.zeros([len(files),num_keywords])

w=N.array([])
fq=N.array([])
d=[]
id=[]
len_txt=[]
len_unique_words=[]
a=0

for i,ix in enumerate(files[2416:]):


	if ix=='14826' or ix=='17475' or ix=='21905' or ix=='21970' or ix=='22054':
		continue

	file = folder + ix.__str__()
	print i,ix,file
	if not os.path.isfile(file):
		print "no file"
		continue
	

	
	
	f= open(file,'r')
	html = f.read()
	
	if len(html)==0:
		print "empty file"
		continue


	#Test for abo:	
	abo = re.findall('TO READ THIS STORY',html)
		
	
	if 	len(abo)>0:
		print abo, "continue..."
		abo=[]
		continue

	#search date:
	date = re.findall('<p id="date" .*>(.*)</p>',html)			
	if len(date)==0:
		date='0'
	else:
		date=date[0]


#	raw=''
	
	#two pages or only one?:
	twopages = re.findall('\n\n2pages\n\n',html)
	if len(twopages)==0:

#		body = re.findall('<div id="articlebody" class="article">.*<div style="overflow: hidden; margin-left:8px;">',html)
		raw=clean(html)

	else:

		twopages = re.search('\n\n2pages\n\n',html)
		r1 = clean(html[0:twopages.end()])	
		r2 = clean(html[twopages.start():-1])	
		raw = r1+r2


	#print raw

		
	#tokens= nltk.word_tokenize(raw)
	
	
	#vocab = make_corpus_vocab_from_tokens(docs, ignorewords='', N=1,stem=False,verbose=False)
	#freq = compute_word_freq_rawtext(raw,vocab,stem=False)
	
	#words = raw.split()
	
	print len(raw)
	
	#Nick's Method:
	words = make_token_list(raw)
	
	
	
	
	voc = nltk.FreqDist(words)
	
	
	#remove common words:	
	for k,kx in enumerate(cwords):
		if voc.has_key(kx):
			voc.pop(kx)

	print "length text: ",len(words)
	print "length unique words: ",len(voc)
	
	#remove small words:
	#for k,kx in enumerate(words):
	#	if voc.has_key(kx):
	#		voc.pop(kx)
	

	#implement edit distance:



	
	#print voc[tokens[0]]
	
	kwds = N.array(voc.keys()[0:num_keywords])
	freqs = N.array(voc.values()[0:num_keywords])


		
	
	if len(kwds)==num_keywords:
		#print freqs,kwds
		#print i,ix,date,kwds
		w=N.append(w,kwds)
		fq=N.append(fq,freqs)
		d=N.append(d,date)	
		id=N.append(id,int(ix))
		len_txt=N.append(len_txt,len(words))
		len_unique_words = N.append(len_unique_words,len(voc))
#		w[i,:] = kwds
#		f[i:] = N.array(voc.keys()[0:num_keywords])
	else:
		print "problem"
		print kwds,freqs
		print len(kwds),len(freqs)
		a+=1
	
	x,y = rankorder(voc.values())
	
	
	#Entropy:
	

	#print "q","H"
	for k,kx in enumerate(q):
	
		
		if kx==1:
			log_p = N.log(x)
			S= -sum(N.array(x)*log_p)
	
		else:
			sum_pq = N.sum(N.array(x)**kx)
			S = 1/(kx-1)*(1-sum_pq)
			#print N.array(x)**jx
		
		#print jx,S
		
		#H.append(S)
		H[i,k]=S
		
	#P.close("all")
	#P.loglog(x,y)


w=N.reshape(w,[len(w)/num_keywords,num_keywords])
fq=N.reshape(fq,[len(fq)/num_keywords,num_keywords])



#P.close(2)
#P.figure(2)
#for i,ix in enumerate(q):
#	print N.mean(H[:,i]), N.std(H[:,i])
#	P.plot(H[:,i])

#P.legend(q,loc=0)


