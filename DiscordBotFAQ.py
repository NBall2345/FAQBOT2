import discord
import re
import spacy
###I Nathan Ball, 000881332 certify that this material is my original work. No other person's work has been used without due acknowledgement. I have not made my work available to anyone else.
###DOCUMENTED ON THE PYTHON SHELL VERSION, ONLY CHANGES HERE ARE ADDING MESSAGE, SELF params and changing print() to await message.channel.send()
class MyClient(discord.Client):
    """Class to represent the Client (bot user)"""
    Questions_array = []
    Answers_array = []
    regex_array = []
    double_question = []
    greet = False
    def __init__(self):
        """Constructor for python and discord kinda thing"""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)
        with open('questions.txt', 'r') as file:
            for line in file:
                elements = line.split()
                sentence = ' '.join(elements)
                self.Questions_array.append(sentence)
        with open('answers.txt', 'r') as file:
            for line in file:
                elements = line.split()
                sentence = ' '.join(elements)
                self.Answers_array.append(sentence)
        with open('Regex.txt', 'r') as file:
            for line in file:
                elements = line.split('\n')
                self.regex_array.append(elements)
        self.greet = True

    async def greetings(self, message):
        await message.channel.send("Hello, This is DolphinsAI. Please ask anything regarding to dolphins and I will do my best to respond")
        await message.channel.send("Type Quit to End at anytime")
        #await self.basicMatchQuestions(message)
    async def SpacyTime(self, message, user_input):
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
            await message.channel.send("Im sorry I could not find anything on your question")
            return
        if theGreeting == True:#if its true respond with this
            await message.channel.send("Hello! Please feel free to ask anything")
        if theQuestion == True:#same logic
            await message.channel.send("Please Rephrase a question about dolphins")
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
                await message.channel.send("Im sorry i cant help you " + verb + " "+ det +" " + noun)
                await message.channel.send("Please ask me anything about Dolphins")
            elif noun and verb:#only the 2
                await message.channel.send("Im sorry i cant help you " + verb + " the " + noun)
            elif noun:#only the noun
                await message.channel.send("Im sorry i cant help you with the" + noun)
                await message.channel.send("Please ask me anything about Dolphins")
            else:#something else
                await message.channel.send("Im sorry i cant help you with that")
                await message.channel.send("Please ask me anything about Dolphins")
        return#regarldess call the questioning and first logic function
    async def fuzzyMatchQuestions(self, message, user_input):
        iteration = 0#loop throughs

        for i in self.regex_array:#go through all the regex's i made in the file

            theregex = self.regex_array[iteration][0].strip()#at the iteration its on, and then grab it so the brackets arent there and strip extra space

            match = re.match('(.*)?' + theregex, user_input, re.IGNORECASE)#match the regex and userinput and ignore the cases and the '(.*)?' to see if anything is infront
            if match:#if there was a match
                await message.channel.send(self.Answers_array[iteration])#print the answers array
                return#go back to the first logic function
            iteration +=1#increment iteration
        await self.SpacyTime(message, user_input)
        #SpacyTime(userinput)#Go to the spacy time as it never found it

    async def basicMatchQuestions(self, message, user_input):
        thesequence = 0
        found = False
        count = 0
        if user_input.lower() == 'quit':
            await message.channel.send('Closing the bot...')
            await self.close()
        cleaned_text = re.sub(r'\W', '', user_input).lower()

        for i in self.Questions_array:
            self.double_question = self.Questions_array[count].split('|')[:2]
            for sub_question in self.double_question:
                cleaned_response = re.sub(r'\W', '', sub_question).lower()
                if cleaned_text == cleaned_response:
                    found = True
                    await message.channel.send(self.Answers_array[count])
                    return
            count += 1
        if not found:
            await self.fuzzyMatchQuestions(message, user_input)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if self.greet == True:
            await self.greetings(message)
            self.greet= False
        user_input = message.content
        await self.basicMatchQuestions(message, user_input)
# Set up and log in
client = MyClient()
with open("bot_token.txt") as file:
    token = file.read()

client.run(token)
