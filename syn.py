import io
import re

f = io.open("17000+words.txt", 'r', encoding='utf8')
f_out = io.open("17000+words_syn.txt", 'w', encoding='utf8')
lines = f.readlines()
f.close()

i = 0
for line in lines:
	i = i + 1
	print i
	words = line.split("	")
	transl = words[4].split("; ")
	syns = None
	syns = []
	for l in lines:
		if len(syns) > 9:
			break
		w = l.split("	")
		if w[1] == words[1]:
			continue
		tr = w[4].split("; ")
		if len(set(transl) & set(tr)) > 1:
			syns.append(w[1])
	if len(syns) < 10:
		for l in lines:
			if len(syns) > 9:
				break
			w = l.split("	")
			if w[1] == words[1]:
				continue
			tr = w[4].split("; ")
			if len(set(transl) & set(tr)) > 0:
				if w[1] not in syns:
					syns.append(w[1])	
	text = ""
	for syn in syns:
		text = text + syn + ", "
	
	f_out.write(words[0] + u"	" + words[1] + u"	" + words[2] + u"	" + words[3] + u"	" + words[4] + u"	" + text[:-2] + u"	" + words[6] + u"	" + words[7])
	
f_out.close()