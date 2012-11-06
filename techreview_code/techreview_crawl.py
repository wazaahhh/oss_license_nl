from urllib2 import Request,urlopen,HTTPError,URLError
import numpy as N
import os
import re

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)



#http://www.technologyreview.com/computing/25537/

branches = ["computing/","web/","communications/","energy/"]

folder = "data2/" #%s" %branches[3]


ensure_dir(folder)


for k,kx in enumerate(branches[1:]):

	r = 'http://www.technologyreview.com/%s' %kx
	
	i = 25550
	#i = 13000
	
	
	while i>5000:
		i=i-1
		print i
		url1 = r+i.__str__()+"/page1"
		url2 = r+i.__str__()+"/page2"
	
		file_path= folder+i.__str__()
		
		twopages=[]
		
		if not os.path.isfile(file_path):

			req1 = Request(url1)
			print url1
	
			try:
				f = open(file_path,'w')
				response = urlopen(req1)
				html= response.read()
				twopages=re.findall('page2/">2</a>',html)
				f.write(html)
				#print "done"
	
			except URLError:
				print "This Page 1 does not exists"
				continue
				
			req2 = Request(url2)

			
			if len(twopages)>0:
				print url2
				try:
					response = urlopen(req2)
					f.write("\n\n2pages\n\n")
					html= response.read()
					f.write(html)
					print "2 pages...done"

	
				except URLError:
					print "This Page 2 does not exists"

			else:
				print "only 1 page...done"


			f.close()

			
		else:
			print "file already downloaded"