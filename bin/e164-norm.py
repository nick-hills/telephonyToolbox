#!/usr/bin/python
import sys, re, csv

def main():
	#originalNum = sys.argv[1]

	infile = sys.stdin
	outfile = sys.stdout

	r = csv.DictReader(infile)
	#header = r.fieldnames
	header = ["number","countryCode","areaCode","normalisedNumber","length","nationalNumber"] #

	w = csv.DictWriter(outfile, fieldnames=header)
	w.writeheader()

	for result in r:
		if result['number']:
			#print result
			result['number'],result['countryCode'],result['areaCode'],result['normalisedNumber'],result['length'],result['nationalNumber'] = processNumber(result['number'])
			#print result
			w.writerow(result)

	



def processNumber(originalNum):
	originalNumLen = len(originalNum)
	#if 8 <= originalNumLen <= 15: 
	#	print "Valid"
	#else:
	#	print "InValid"

	originalNumInitial = originalNum[0]
	
	if originalNumInitial == "+":
		numType="e164Int"
		normNum = originalNum[-(originalNumLen-1):]	
	elif  originalNumInitial == "0":
		if originalNum[1] == "0":
			numType = "prefixInt"
			normNum = originalNum[-(originalNumLen-2):]
		else:
			numType = "prefixUKGeo"
			normNum = "44"+str(originalNum[-(originalNumLen-1):])			
	else:
		numType = "unprefixed"
		normNum = originalNum
	
	countryCode, ccLen = getCountry(normNum)
	if countryCode > 0:
		nationalNum = normNum[-(len(normNum)-ccLen):]
		#Take specific country action
		if countryCode == "1":
			area = str(nationalNum[0])+str(nationalNum[1])+str(nationalNum[2])
		elif countryCode == "7":
                        area = str(nationalNum[0])+str(nationalNum[1])+str(nationalNum[2])
		elif countryCode == "33":
                        area = str(nationalNum[0])
		elif countryCode == "34":
			area = str(nationalNum[0])+str(nationalNum[1])+str(nationalNum[2])
		elif countryCode == "39":
                        area = str(nationalNum[0])+str(nationalNum[1])
                elif countryCode == "41":
                        area = str(nationalNum[0])+str(nationalNum[1])
                elif countryCode == "48":
                        area = str(nationalNum[0])+str(nationalNum[1])
		elif countryCode == "44":
			area = getUKArea(nationalNum)
		else:
			area = None

	else:
		#something went wrong :(
		countryCode = None
		nationalNum = None
		area = None
		
	return originalNum, countryCode, area, normNum, len(normNum), nationalNum


def getCountry(normNum):
	oneDigitCC = re.match( r'(?P<country>^[1,7])\d*', normNum, re.M|re.I)
	twoDigitCC = re.match( r'(?P<country>^(20|27|30|31|32|33|34|36|39|40|41|43|44|45|46|47|48|49|51|52|53|54|55|56|57|58|60|61|62|63|64|65|66|81|82|84|86|90|91|92|93|94|95|98))\d*', normNum, re.M|re.I)
	threeDigitCC = re.match( r'(?P<country>^[2-9]\d\d)\d*', normNum, re.M|re.I)

	if oneDigitCC:
			country = oneDigitCC.group('country')
			ccLen = 1
	elif twoDigitCC:
			country = twoDigitCC.group('country')
			ccLen = 2
	elif threeDigitCC: 
			country = threeDigitCC.group('country')
			ccLen = 3
	else:
			country = 0
			ccLen = 0	
	return country, ccLen

def getUKArea(nationalNum):
	ukOne = re.match( r'(?P<area>^1\d\d\d)\d*', nationalNum, re.M|re.I)
	ukTwo = re.match( r'(?P<area>^20(3|7|8))\d*', nationalNum, re.M|re.I)
	ukThree = re.match( r'(?P<area>^3\d\d)\d*', nationalNum, re.M|re.I)
	ukSeven = re.match( r'(?P<area>^7)\d*', nationalNum, re.M|re.I)
	ukEight = re.match( r'(?P<area>^8)\d*', nationalNum, re.M|re.I)
        ukNine = re.match( r'(?P<area>^9)\d*', nationalNum, re.M|re.I)
	if ukOne:
		area = ukOne.group('area')
	elif ukTwo:
		area = ukTwo.group('area')
	elif ukThree:
		area = ukThree.group('area')
	elif ukSeven:
		area = ukSeven.group('area')
        elif ukEight:
                area = ukEight.group('area')
        elif ukNine:
                area = ukNine.group('area')
	return area



main()
