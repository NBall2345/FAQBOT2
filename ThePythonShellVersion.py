import re
import sys
import spacy
from openai import OpenAI
###I Nathan Ball, 000881332 certify that this material is my original work. No other person's work has been used without due acknowledgement. I have not made my work available to anyone else.
Questions_array = []#define the array to put all the questions inside
Answers_array = []#define the answers array to put all the answers inside
regex_array = []#regex array of all the regexes
double_question = []#logic to store and keep
client=OpenAI(api_key ="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")
with open('questions.txt', 'r') as file:#read the questions.txt file
        for line in file:
            elements = line.split()#split it up
            sentence = ' '.join(elements)#and then join all the sentences together to give big arrays of sentences
            Questions_array.append(sentence)#add the sentence to the question array
with open('answers.txt', 'r') as file:#same concept with answers
        for line in file:
            elements = line.split()
            sentence = ' '.join(elements)
            Answers_array.append(sentence)
with open('Regex.txt', 'r') as file:
        for line in file:
            elements = line.split('\n')#split it by each line
            regex_array.append(elements)
#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
def thechatgptpart():

#print(f"LIST OF QUESTIONS: {Questions_array}")#SHOW ALL QUESTIONS
#Basic Match Questions used to match spots with the questions and answers  with 2 questions per line
#No params
#No arguments
def basicMatchQuestions():
    thesequence = 0#how many times it runs through
    while True:#keep itterating through
        found = False#if it found one, start this at false
        count = 0#count at 0
        user_input = input("Enter a Question: ")#user input
        if user_input == 'quit':#if they type quit exit out of the whole thing
            sys.exit()
        cleaned_text = re.sub(r'\W', '', user_input).lower()#put it lower and get rid of any weird symbols


        for i in Questions_array:#loop through questions

            double_question = Questions_array[count].split('|')[:2]#only holds 2, split it with the | as there is 2 questions for each line
            for sub_question in double_question:#itterate trhough both the questions
                cleaned_response = re.sub(r'\W', '', sub_question).lower()#make them clean
                if cleaned_text == cleaned_response:#match and see if any do match
                    found = True
                    print(Answers_array[count])#print result
                    break
            count +=1
        if not found:#if its not found
            break
    fuzzyMatchQuestions(user_input)#go to fuzzy input
##SpacyTime
##Param User_Input
##3rd function with purpose called and used to understand whatt the user is asking for and reply with human response,
def SpacyTime(user_input):
    noun = None  # Initialize noun
    verb = None
    det = None
    theGreeting = False#Checks for if there is a greeting, question or Command
    theQuestion = False
    theCommand = False
    from spacy.matcher import Matcher#Import the matcher
    nlp = spacy.load("en_core_web_sm")#load this thing
    matcher = Matcher(nlp.vocab)#let the matcher connect these
    greeting_pattern = [{"LOWER": {"IN": ["hi", "hello", "hey", "greetings", "howdy"]}}]#if there is any of these, its a greeting
    question_pattern = [{"LOWER": {"IN": ["what", "where", "when", "how", "why", "who"]}}]#any of these and its a question
    command_pattern = [#In order if something goes kinda in this order, It has a chance to not be used with the OP:?
                    {"POS": "ADV", "OP": "?"},  # Match "ADV"
                    {"POS": "VERB"},    # Match"VERB"
                    {"POS": "PRON"}, #Match "PRON" Pronoun
                    {"POS": "DET", "OP": "?"},   # Match "DET"
                    {"POS": "NOUN", "OP": "?"}   # Match "NOUN"
]
    matcher.add("GREETING", [greeting_pattern])#add these all regardless and see if it populates
    matcher.add("QUESTION", [question_pattern])
    matcher.add("COMMAND", [command_pattern])
    doc = nlp(user_input.lower())#make it all lower to check as everything is in lower
    matches = matcher(doc)#new name and variable for it
    if matches:
        for match_id, start, end in matches:#go from all the matches and check from the start to the end
            matched_span = doc[start:end]
            if matcher.vocab.strings[match_id] == "GREETING":#if the match_id is greeting
                theGreeting = True#set true
            elif matcher.vocab.strings[match_id] == "QUESTION":#same logic
                theQuestion = True
            else:
                theCommand = True#same logic

    else:#couldnt find any at all
        print ("Im sorry I could not find anything on your question")
        basicMatchQuestions()
    if theGreeting == True:#if its true respond with this
        print("Hello! Please feel free to ask anything")
    if theQuestion == True:#same logic
        print ("Please Rephrase a question about dolphins")
    elif theCommand == True:#for command its different, checking for any verb, det or noun spoken and putting it into the variable I initialized at the start
        for token in matched_span:
            if token.pos_ == "VERB":
                verb = token.text
            if token.pos_ == "DET":
                det = token.text
            if token.pos_ == "NOUN":
                noun = token.text
                break
        if noun and verb and det:#if it had all 3 use them in a sentence to respond
            print("Im sorry i cant help you " + verb + " "+ det +" " + noun)
            print("Please ask me anything about Dolphins")
        elif noun and verb:#only the 2
            print("Im sorry i cant help you " + verb + " the " + noun)
        elif noun:#only the noun
            print ("Im sorry i cant help you with the" + noun)
            print("Please ask me anything about Dolphins")
        else:#something else
            print("Im sorry i cant help you with that")
            print("Please ask me anything about Dolphins")
    basicMatchQuestions()#regarldess call the questioning and first logic function
##fuzzyMatchQuestions
##Param: UserInput
##if the question isnt exactly the same as the notes, we go to the fuzzy matches and check for something similar
def fuzzyMatchQuestions(userinput):
    iteration = 0#loop throughs

    for i in regex_array:#go through all the regex's i made in the file

        theregex = regex_array[iteration][0].strip()#at the iteration its on, and then grab it so the brackets arent there and strip extra space

        match = re.match('(.*)?' + theregex, userinput, re.IGNORECASE)#match the regex and userinput and ignore the cases and the '(.*)?' to see if anything is infront
        if match:#if there was a match
            print(Answers_array[iteration])#print the answers array
            basicMatchQuestions()#go back to the first logic function
        iteration +=1#increment iteration
    SpacyTime(userinput)#Go to the spacy time as it never found it

##Greetings, First function overall with no logic besides greeting the user and calling the first logical function
def greetings():
    print("Hello, This is DolphinsAI. Please ask anything regarding to dolphins and i will do my best to respond")
    print("Type Quit to End at anytime")
    basicMatchQuestions()#the start of it all





greetings()






