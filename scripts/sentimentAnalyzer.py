#Import necessary libraries
import nltk
import os
#Uncomment and run the following lines if this the first time running the code
#nltk.download('all')
#specify custom download directory for NLTK data
#nltk.download('all', download_dir='/project/redditsa/')

#Add custom download directory for NLTK data
nltk.data.path.append("/project/redditsa/nltk_Data");
#^Add custom path the NLTK data
#nltk.download('vader_lexicon')

#Import speicific modules from the NLTK library 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#initialize the VADER sentiment analyzer
vader = SentimentIntensityAnalyzer()

#Define a function to preprocess text 
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    
    #Define list of words not to be removed during tokenization
    dontDelete=["no", "nor", "aren't", "couldn't", "didn't", "doesn't", "don't", "hasn't", "hadn't", "haven't", "isn't", "shouldn't", "wasn't", "weren't", "won't", "wouldn't"]
    
    #Filter out stopwards and words specified in dontDelete
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english') or token in dontDelete]
   #Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    #Join the lemmatized tokens into a processed text
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text

#Join the lemmatized tokens into a procssed text
fileDirectory=""
writeToFile=""
tempFile=""
trueFile=""

#Specify the directory for input files
directory = '/project/redditsa/reddit-scraping/api-results/'
for fileName in os.listdir(directory):
    #^Loop through each file in the specified directory 
    fileDirectory= os.path.join(directory, fileName) 
    #construct the file paths for input and output
    writeToFile=os.path.join('/project/redditsa/reddit-scraping/sentiment-results', fileName)
    tempFile='/project/redditsa/reddit-scraping/sentiment-results/temp-results'
#fileDirectory="/project/redditsa/reddit-scraping/api-results/WEN DFV?.md"
    #Create dictionaries to store user comments, replies, and related info
    userComments={}
    userReplies={}
    whoRepliedToWho={}
    mostRepliedToUsers={}

    #intialize variable for processing comments and replies
    firstComment=True
    firstReply=True
    replyIsMostRecent=False
    currentComment=[]
    currentReply=[]
    user=""
    commentScore=0
    postTime=""
    repliedUser=""
    personRepliedTo=""
    replyPostTime=""

    replyScore=0
    totalPositives=0
    totalPositiveScore=0
    totalNegatives=0
    totalNegativeScore=0
    totalNeutrals=0
    totalCount=0
    totalScore=0
    tempScore=0

    #open temporary file for writing
    f = open(tempFile, "w")

    #open the current file for reading
    with open(fileDirectory) as file_object:
        #iterate through each line in the file
        for currentLine in file_object:
            #split through each line in the file
            line=currentLine.split();
            #split the current line into a list of words

            #Check if the line has more than 2 words
            if (len(line) > 2):
                #Check if the line is a comment 
                if (line[1]=="commented" or line[2]=="commented"):
                    #Process the first comment
                    if (firstComment==True):
                        firstComment=False
                        user=line[0]
                        #Handle the case of a deleted user
                        if (user=="[deleted"):
                            user="[deleted user]"
                            postTime=line[4:6]
                            commentScore=line[6]
                            currentComment=line[8:]
                            replyIsMostRecent=False
                        else:
                            postTime=line[3:5]
                            commentScore=line[5]
                            currentComment=line[7:]
                            replyIsMostRecent=False
                            #Update userComments dictioary
                        if (user not in userComments):
                            userComments[user]=1
                        else:
                            userComments[user]=userComments[user]+1
                    else:
                        #Write sentiment analysis for the previous comment
                        f.write(user + " commented on " + postTime[0] + " at " + postTime[1] + " with a score of " + replyScore + ":\n") 
                        f.write(' '.join(currentComment))
                        f.write("\n----------------------------------------------\n")
                        f.write("Sentiment analysis is as follows: \n")
                        f.write(str(vader.polarity_scores(preprocess_text(' '.join(currentComment)))) + "\n \n \n")
                        #update total scores and counts 
                        tempScore=vader.polarity_scores(preprocess_text(' '.join(currentComment)))["compound"]
                        totalScore=tempScore+totalScore
                        totalCount=totalCount+1
                        #update postiive, negative, and netural counts and scores
                        if (tempScore > 0):
                            totalPositives=totalPositives+1
                            totalPositiveScore=totalPositiveScore+tempScore
                        elif (tempScore < 0):
                            totalNegatives=totalNegatives+1
                            totalNegativeScore=totalNegativeScore+tempScore
                        else:
                            totalNeutrals=totalNeutrals+1
                        #Reset vaaible for the next comment
                        f.write("\n")
                        f.write("\n")
                        user=line[0]
                        #handle the case of a deleted user
                        if (user=="[deleted"):
                            user="[deleted user]"
                            postTime=line[4:6]
                            commentScore=line[6]
                            currentComment=line[8:]
                            replyIsMostRecent=False
                        else:
                            currentComment=line[7:]
                            commentScore=line[5]
                            postTime=line[3:5]
                            replyIsMostRecent=False
                        if (user not in userComments):
                            userComments[user]=1
                        else:
                            userComments[user]=userComments[user]+1
             #Check if line is a reply
                elif (line[1]=="replied" or line[2]=="replied"):
                    if (firstReply==False):
                        f.write(repliedUser + " replied to " + personRepliedTo + " on " + replyPostTime[0] + " at " + replyPostTime[1] + " with a score of " + replyScore + ":\n")
                        f.write(' '.join(currentReply))
                        f.write("\n----------------------------------------------\n")
                        f.write("Sentiment analysis is as follows: \n")
                        f.write(str(vader.polarity_scores(preprocess_text(' '.join(currentReply)))) + "\n \n \n")
                        tempScore=vader.polarity_scores(preprocess_text(' '.join(currentReply)))["compound"]
                        totalScore=tempScore+totalScore
                        #update total scores and counts
                        totalCount=totalCount+1
                        #^update total scores and counts
                        #Update postivie, neg and netural scores and counts 
                        if (tempScore > 0):
                            totalPositives=totalPositives+1
                            totalPositiveScore=totalPositiveScore+tempScore
                        elif (tempScore < 0):
                            totalNegatives=totalNegatives+1
                            totalNegativeScore=totalNegativeScore+tempScore
                        else:
                            totalNeutrals=totalNeutrals+1
                    else:
                        firstReply=False
                    repliedUser=line[0]
                    #update variable for the current reply
                    incrementer=0
                    if (repliedUser=="[deleted"):
                        repliedUser="[deleted user]"
                        personRepliedTo=line[4]
                        if (personRepliedTo=="[deleted"):
                            personRepliedTo="[deleted user]"
                            incrementer=1
                        replyPostTime=line[6+incrementer:8+incrementer]
                        currentReply=line[10+incrementer:]
                        replyScore=line[8+incrementer]
                        replyIsMostRecent=True
                    else:
                        personRepliedTo=line[3]
                        if (personRepliedTo=="[deleted"):
                            personRepliedTo="[deleted user]"
                            incrementer=1
                        replyPostTime=line[5+incrementer:7+incrementer]
                        currentReply=line[9+incrementer:]
                        replyScore=line[7+incrementer]
                        replyIsMostRecent=True
                    if (repliedUser not in userReplies):
                        userReplies[repliedUser]=1
                    else:
                        userReplies[repliedUser]=userReplies[repliedUser]+1
                    if (repliedUser not in whoRepliedToWho):
                        whoRepliedToWho[repliedUser]=[]
                        whoRepliedToWho[repliedUser].append(personRepliedTo)
                    else:
                        whoRepliedToWho[repliedUser].append(personRepliedTo)
                else:
                    if (replyIsMostRecent == False):
                        currentComment = currentComment + line
                    else:
                        currentReply = currentReply + line
            elif (len(line)<=2 and firstComment==False):
                if (replyIsMostRecent == False):
                    currentComment = currentComment + line
                else:
                    currentReply = currentReply + line
    f.write(user + " commented on " + postTime[0] + " at " + postTime[1] + " with a score of " + replyScore + ":\n")
    f.write(' '.join(currentComment))
    f.write("\n----------------------------------------------\n")
    f.write("Sentiment analysis is as follows: \n")
    f.write(str(vader.polarity_scores(preprocess_text(' '.join(currentComment)))) + "\n \n \n")
    tempScore=vader.polarity_scores(preprocess_text(' '.join(currentComment)))["compound"]
    totalScore=tempScore+totalScore
    totalCount=totalCount+1
    if (tempScore > 0):
        totalPositives=totalPositives+1
        totalPositiveScore=totalPositiveScore+tempScore
    elif (tempScore < 0):
        totalNegatives=totalNegatives+1
        totalNegativeScore=totalNegativeScore+tempScore
    else:
        totalNeutrals=totalNeutrals+1
    f.write(repliedUser + " replied to " + personRepliedTo + " on " + replyPostTime[0] + " at " + replyPostTime[1] + " with a score of " + replyScore + ":\n")
    f.write(' '.join(currentReply))
    f.write("\n----------------------------------------------\n")
    f.write("Sentiment analysis is as follows: \n")
    f.write(str(vader.polarity_scores(preprocess_text(' '.join(currentReply)))) + "\n \n \n")
    tempScore=vader.polarity_scores(preprocess_text(' '.join(currentReply)))["compound"]
    totalScore=tempScore+totalScore
    totalCount=totalCount+1
    if (tempScore > 0):
        totalPositives=totalPositives+1
        totalPositiveScore=totalPositiveScore+tempScore
    elif (tempScore < 0):
        totalNegatives=totalNegatives+1
        totalNegativeScore=totalNegativeScore+tempScore
    else:
        totalNeutrals=totalNeutrals+1

    f.close()
#writeToFile=os.path.join('/project/redditsa/reddit-scraping/sentiment-results', fileName)
    f2 = open(writeToFile, "w")
    f2.write("Info for post titled: " + fileName + "\n\n\n")
    f2.write("FINAL SCORE: \n" )
    f2.write("----------------------------\n")
    f2.write("TOTAL NUMBER OF POSITIVE COMMENTS/REPLIES: " + str(totalPositives) + " out of " + str(totalCount) + "\n")
    f2.write("TOTAL NUMBER OF NEGATIVE COMMENTS/REPLIES: " + str(totalNegatives) + " out of " + str(totalCount) + "\n")
    f2.write("TOTAL NUMBER OF NEUTRAL COMMENTS/REPLIES: " + str(totalNeutrals) + " out of " + str(totalCount) + "\n")
    f2.write("TOTAL AVERAGE COMMENT/REPLY SENTIMENT: " + str(totalScore/totalCount) + "\n")
    f2.write("AVERAGE POSITIVE COMMENT/REPLY SENTIMENT: " + str(totalPositiveScore/totalPositives) + "\n")
    f2.write("AVERAGE NEGATIVE COMMENT/REPLY SENTIMENT: " + str(totalNegativeScore/totalNegatives) + "\n \n \n")
    
    f2.write("People who commented: \n------------------------------------------\n")
    for key in userComments:
        f2.write(key + ": " + str(userComments[key]) + "\n")
    f2.write("\n\n\n")

    f2.write("Number of replies per person: \n------------------------------------------\n")
    for key in userReplies:
        f2.write(key + " replied to " + str(userReplies[key]) + " person(s)\n")
    f2.write("\n\n\n")

    f2.write("Who replied to who: \n------------------------------------------\n")
    for key in whoRepliedToWho:
        f2.write(key + ": " + str(whoRepliedToWho[key]) + "\n")
    f2.write("\n\n\n")

    for key in whoRepliedToWho:
        for entry in whoRepliedToWho[key]:
            if (entry not in mostRepliedToUsers):
                mostRepliedToUsers[entry]=1
            else:
                mostRepliedToUsers[entry]=mostRepliedToUsers[entry]+1

    f2.write("The most replied to users: \n------------------------------------------\n")
    #{k: v for k, v in sorted(x.items(), key=lambda item: item[1])
    #dict(sorted(x.items(), key=lambda item: item[1]))
    mostRepliedToUsersNew = dict(sorted(mostRepliedToUsers.items(), key=lambda x: x[1], reverse=True))
    for key in mostRepliedToUsersNew:
        f2.write(key + ": " + str(mostRepliedToUsersNew[key]) + "\n")
    f2.write("\n")
    f2.close()

    with open(tempFile) as afile_object:
        f3=open(writeToFile, "a")
        f3.write("\n                                                     SPECIFIC DATA:                                                                        \n")
        f3.write("\n_______________________________________________________________________________________________________________________________\n \n \n")
        for currentLine in afile_object:
            f3.write(currentLine)
        f3.close()
#print(sorted(mostRepliedToUsers))
