import requests
import xml.etree.ElementTree as ET
import argparse
import re

# gather trips extractions from an entire pubmed paper(xml) or body of raw text
# extraction output are text files named ID+paragraphNum+subSectionNum
# example is "1403772P2-1.txt"
def interface(filename, pStart, extension):
	pNum=0

	if 'xml' in filename:
		# read in NXML file
		tree = ET.parse(filename)
		root = tree.getroot()
		paperID = root.find(".//*[@pub-id-type='pmc']")
		paperID = str(paperID.text)
		
		body = root.find('body')
		for paragraph in body.iter('p'):
			pNum+=1
			# retrieving next paragraph's text
			thisString = str("".join(paragraph.itertext()))
			print(thisString)
			# paragraph offset for where to begin reading
			if pNum >= pStart:
				# breaking up large paragraphs into smaller chunks
				paragraphChunk=""
				chunkCount = 0
				sentenceList = re.split(r"\.\s|\?\s|\!\s", thisString)
				try:
					sentenceList.remove("")
				except ValueError:
					pass
				# growing paragraph chunk sentence by sentence
				for thisSentence in sentenceList:
					paragraphChunk+= thisSentence+"."
					# if paragraph chunk is large enough, submit it
					if len(paragraphChunk) > 500:
						print("chunk "+str(chunkCount)+" is:\n"+paragraphChunk)
						sendRequest(paragraphChunk, paperID, pNum, chunkCount, extension)
						# reset paragraph chunk after response recieved
						paragraphChunk = ""
						chunkCount+=1
				# if last paragraph chunk is small
				if len(paragraphChunk) < 500 and len(paragraphChunk)>1:
					print("chunk "+str(chunkCount)+" is:\n"+paragraphChunk)
					sendRequest(paragraphChunk, paperID, pNum, chunkCount, extension)

			print()

	elif 'txt' in filename:
		# read in raw text
		paperID = filename.replace('.txt','')
		with open(filename, 'r') as infile:
			thisString = infile.read()
		# breaking up large paragraphs into smaller chunks
		paragraphChunk=""
		chunkCount = 0
		sentenceList = re.split(r"\.\s|\?\s|\!\s", thisString)
		try:
			sentenceList.remove("")
		except ValueError:
			pass
		# growing paragraph chunk sentence by sentence
		for thisSentence in sentenceList:
			paragraphChunk+= thisSentence+"."
			# if paragraph chunk is large enough, submit it
			if len(paragraphChunk) > 500:
				print("chunk "+str(chunkCount)+" is:\n"+paragraphChunk)
				if chunkCount >= pStart:
					sendRequest(paragraphChunk, paperID, pNum, chunkCount, extension)
				# reset paragraph chunk after response recieved
				paragraphChunk = ""
				chunkCount+=1
		# if last paragraph chunk is small
		if len(paragraphChunk) < 500 and len(paragraphChunk)>1:
			print("chunk "+str(chunkCount)+" is:\n"+paragraphChunk)
			sendRequest(paragraphChunk, paperID, pNum, chunkCount, extension)		


def sendRequest(paragraphChunk, paperID, pNum, chunkCount, extension):
	# send chunk to api
	data = {'input': paragraphChunk}
	if extension == 'DRUM':
		response = requests.post('http://trips.ihmc.us/parser/cgi/drum', data=data)
	elif extension == 'CWMS':
		response = requests.post('http://trips.ihmc.us/parser/cgi/cwmsreader', data=data)
	else:
		assert False

	# check for whether the server crashed lol
	if len(response.text) > 1000:
		# write out to a text file for each
		with open(str(paperID)+"P"+str(pNum)+str("" if chunkCount==0 else "-"+str(chunkCount))+".txt","w") as text_file:
			text_file.write(response.text)
		print("RESPONSE RECIEVED")

def main():
	# Parse command line arguments
	parser = argparse.ArgumentParser(
		description='Process PMC articles (in nmxl format or plain text) through TRIPS/DRUM api and store to xml output files',
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('input_file', type=str, 
						help='PMC .nmxl file')
	parser.add_argument('pStart', type=int, 
						help='starting paragraph')
	parser.add_argument('extension', type=str,
						help='DRUM or CWMS')

	args = parser.parse_args()
	assert 'xml' in args.input_file or 'txt' in args.input_file
	print(args.extension == 'CWMS')
	if args.extension == 'DRUM':
		interface(args.input_file, args.pStart, args.extension)
	elif args.extension == 'CWMS':
		interface(args.input_file, args.pStart, args.extension)
	else:
		print('other extensions not supported at this time')


if __name__ == '__main__':
	main()