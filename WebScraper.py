# Import necessary libraries
from urllib import request
import certifi
import ssl
import pycountry

'''
Session: Lab 1X01
Group Members: Hans, Abizer & Yingwei
Due Date: December 10, 2023
Assignment #4: Interfacing with the Web in Python
Summary: Opens up the following Canada’s major news sources: CBC News, CBC World and Windspeaker (Indigenous 
News) news, to find which Province/Territory is the most talked about in CBC News and Windspeaker and which 
country is the most talked about in CBC World?
Resources Used : 
    Perkovic, Ljubomir. Introduction to Computing Using Python, 2nd ed, Chapter 11
    https://www.w3schools.com/tags/default.asp
    https://www.w3schools.com/python/python_strings_methods.asp
    https://www12.statcan.gc.ca/census-recensement/2021/ref/dict/tab/index-eng.cfm?ID=t1_8
    https://www.cbc.ca/news
    https://www.cbc.ca/news/world
    https://windspeaker.com/news
'''


# Primary Contributor: Hans
# Secondary Contributor: Abizer
# Function gaining access to the url and cleaning up the string html file
def getContent(url):
    # Makes the request and saves the html to a string
    myRequest = request.Request(url)
    context = ssl.create_default_context(cafile=certifi.where())
    connect = request.urlopen(myRequest, context=context)
    html = connect.read()
    content = html.decode()

    # Cleans Code of unnecesary characters
    unnecessary = '''~!@#$%^&*()_+`-={}|[]\\:";'?,<>/"0123456789'''  # A string of unneeded characters
    for character in content:  # Iterates every character of the sting content
        if character in unnecessary:
            content = content.replace(character, " ")  # Replaces the unwanted character to a space
        if "\n" in content:  # Gets rid of the \n that the if statement above does not get rid of
            content = content.replace("\n", " ")
    content = [item for item in content.split(" ") if len(item) > 1]
    # Splits the content to individual words that are seperatd by a space and filters out words not greater than 1
    return content


# Primary Contributor: Hans
# Secondary Contributor: Yingwei
# Returns the occurence value of the indexed province
def countProvince(index, content):
    counter = 0  # Variable for the value of the counted province
    # List for the capital sensitive words and "-" allows iteration at a certain index of the list for each province
    sensitiveList = [("NL", "-"), ("PE", "PEI"), ("NS", "-"), ("NB", "-"), ("QC", "-"), ("ON", "-"), ("MB", "-"),
                     ("SK", "-"), ("AB", "-"), ("BC", "-"), ("YT", "-"), ("NT", "-"), ("NU", "-")]
    for word in sensitiveList[index]:  # Loops for every word in the specific province
        if word in content:  # Checks if the word in the list content
            counter = counter + content.count(word)  # Counts occurence and saves value

    # Turns content into a string, replaces "', '" inside the string to a space and lower cases all characters
    content = str([item.lower() for item in content]).replace("', '", " ")
    # A list for the non character sensitive words
    nonSensitiveList = [("Newfoundland", "N.L."), ("Prince Edward Island", "P.E.I."), ("Nova Scotia", "N.S."),
                        ("New Brunswick", "N.B."), ("Quebec", "Que.", "QC"), ("Ontario", "Ont."), ("Manitoba", "Man."),
                        ("Saskatchewan", "Sask.", "Saskatoon"), ("Alberta", "Alta."), ("British Columbia", "B.C."),
                        ("Yukon", "Y.T."), ("Northwest Territories", "N.W.T."), ("Nunavut", "Nvt.")]
    for word in nonSensitiveList[index]:
        if word.lower() in content:  # Checks if the lowercase of the word is inside the string of content
            counter = counter + content.count(word.lower())  # Counts occurence of lowercase word
    return counter


# Primary Contributor: Hans
# Secondary Contributor: Abizer
# Returns a dictionary of each province with the amount of times they occur
def getProvince(url):
    content = getContent(url)  # Saves the content into a variable
    index = 0
    # Dictionary of provinces each with a value of zero
    provinceDictionary = {"Newfoundland and Labrador": 0, "Prince Edward Island": 0, "Nova Scotia": 0,
                          "New Brunswick": 0, "Quebec": 0, "Ontario": 0, "Manitoba": 0, "Saskatchewan": 0, "Alberta": 0,
                          "British Columbia": 0, "Yukon": 0, "Northwest Territories": 0, "Nunavut": 0}
    for province in provinceDictionary:  # Loops for every province
        provinceDictionary[province] = countProvince(index, content)  # Saves the value of occurence to dictionary
        index += 1
    return provinceDictionary


# Primary Contributor: Hans
# Retuns the total of the two dictionary sources
def getTotal(source1, source2):
    total = {"Newfoundland and Labrador": 0, "Prince Edward Island": 0, "Nova Scotia": 0, "New Brunswick": 0,
             "Quebec": 0, "Ontario": 0, "Manitoba": 0, "Saskatchewan": 0, "Alberta": 0, "British Columbia": 0,
             "Yukon": 0, "Northwest Territories": 0, "Nunavut": 0}  # A dictionary with a zero value for each province
    for province in total:
        total[province] = source1[province] + source2[province]  # Adds both the province value of each dictionary
    return total


# Primary Contributor: Hans
# Secondary Contributor: Abizer
# Prints out the answer to the question of which province/territory has the most news
def displayProvinces(dictionary1, dictionary2, dictionary3):
    dictionary = dictionary1 | dictionary2 | dictionary3  # Joins all three dictionary values into a single dictionary
    # Sorts the dictionary according to the highest value in total
    sortedDictionary = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    print("{:30}{:8}{:8}{:8}".format("Province/Territory", "CBC", "WindS.", "Total"))  # Prints the titles
    for provinceName in sortedDictionary:
        print("{:30}{:<8}{:<8}{:<8}".format(provinceName, dictionary1[provinceName], dictionary2[provinceName],
                                            dictionary3[provinceName]))  # Prints the values of each dictionary values
    print("The province/territory most in the news is: " + max(sortedDictionary, key=sortedDictionary.get) + "\n")
    # Prints the answer of which province/territory has the most news about it


# Primary Contributor: Hans
# Secondary Contributor: Yingwei
# Returns the occurence value of the indexed country
def countCountry(index, content):
    counter = 0
    # List for the capital sensitive words including the values of abbreviations of each country without the periods
    sensitiveList = [(str(country.alpha_2), str(country.alpha_3)) for country in pycountry.countries]
    for word in sensitiveList[index]:
        if word in content:  # Checks if the word is in the list content
            counter = counter + content.count(word)  # Counts occurence and saves value

    # Turns content into a string, replaces "', '" inside the string to a space and lower cases all characters
    content = str([item.lower() for item in content]).replace("', '", " ")
    # List for the non character sensitive words including abbreviations with periods and the country name
    nonSensitiveList = [list(('.'.join(country.alpha_2) + '.', '.'.join(country.alpha_3) + '.', str(country.name))) for
                        country in pycountry.countries]
    listIndex = 0  # Sepertate index for adding the common and official names
    for country in list(pycountry.countries):  # Itterates for each country in the list of countries
        # Creates a variable for the value in country for the official and common name using getattr if the value exists
        officialName, commonName = getattr(country, 'official_name', None), getattr(country, 'common_name', None)
        if officialName is not None:  # Checks if there is a value for the official name
            nonSensitiveList[listIndex].append(country.official_name)  # Adds the offical name to the list at an index
        if commonName is not None:  # Checks if there is a value for the common name
            nonSensitiveList[listIndex].append(country.common_name)  # Adds the common name to the list at an index
        listIndex += 1
    for word in nonSensitiveList[index]:
        if word.lower() in content:  # Checks if the lowercase of the word is inside the string of content
            counter = counter + content.count(word.lower())  # Counts occurence of lowercase word
    return counter


# Primary Contributor: Hans
# Secondary Contributor: Abizer
# Returns a dictionary of each country with the amount of times they occur
def getCountry(url):
    content = getContent(url)  # Saves the content into a variable
    # Dictionary of countries each with a value of zero
    countryDictionary = {country.name: 0 for country in list(pycountry.countries)}
    index = 0  # Index value
    for country in countryDictionary:  # Loops for every country
        countryDictionary[country] = countCountry(index, content)  # Saves the value of occurence to dictionary
        index += 1  # Increases index value
    return countryDictionary


# Primary Contributor: Hans
# Secondary Contributor: Abizer
# Main program that calls other functions
def main():
    cbcProvices = getProvince("https://www.cbc.ca/news")  # Gets dictionary for provinces in CBC News
    windSpeakerProvinces = getProvince("https://windspeaker.com/news")  # Gets dictionary for provinces in wind speaker
    total = getTotal(cbcProvices, windSpeakerProvinces)  # Gets total value dictionary from both sources
    displayProvinces(cbcProvices, windSpeakerProvinces, total)  # Prints text

    cbcWorldCountries = getCountry("https://www.cbc.ca/news/world")  # Gets dictionary for countries in CBC World
    print("The country most in CBC World is: " + max(cbcWorldCountries, key=cbcWorldCountries.get) + " with " + str(max(
        cbcWorldCountries.values())) + " mentions")  # Prints the answer to the question from the cbcWorld Dictionary


# Calls the main program
main()
