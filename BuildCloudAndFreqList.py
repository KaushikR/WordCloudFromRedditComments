# Builds word cloud from submission

import time
import praw
import datetime
from wordcloud import WordCloud, STOPWORDS

WIDTH = 1280
HEIGHT = 720
NUM_OF_WORDS = 500

def getCommentsAsSingleString(comments):
    """    
    Get all comments as a single string    
    """

    text = ''

    for comment in comments:                            
        text += comment.body
        text += ' '

    return text

def makeCloud(text, imgFile, words):
    """
    Makes a word cloud and stores it in a jpeg file
    """
    excludewords = STOPWORDS.copy()
    
    for word in words:
        excludewords.add(word)
    
    wordcloud = WordCloud(max_words=NUM_OF_WORDS, width=WIDTH, height=HEIGHT, stopwords=excludewords).generate(text)
    image = wordcloud.to_image()
    image.show()
    image.save(imgFile + '.jpeg')      

def writeFreq(text, outFile, words):
    """
    Writes frequencies of words into the specified file
    """

    excludewords = STOPWORDS.copy()
    
    for word in words:
        excludewords.add(word)
    
    wordcloud = WordCloud(max_words=NUM_OF_WORDS, stopwords=excludewords)
    freqList  = wordcloud.process_text(text)

    for item in freqList:
        outFile.write(item[0] + ',' + str(item[1]) + '\n')


def fetchAndProcessComments(subid):
    """
    Function to process comments from a submission
    """
    
    r = praw.Reddit('/r/IAmA scraping by /u/kashre001')    
    
    try: 
        new_submission = r.get_submission(submission_id = subid)
        new_submission.replace_more_comments(limit=None, threshold=0)
        all_flat_comments = praw.helpers.flatten_tree(new_submission.comments)
    

    except Exception as e:
        print ('Something went wrong...\n Sleeping for 60 seconds...\n')
        return

    print(len(all_flat_comments))
    return all_flat_comments
            

def main():

    subid = '3mq1wl'
    freqFile = open('RandiaFreq.csv','w',encoding='utf-8')
    submissionId = '3mq1wl'
    imgFile  = 'AMAcloud2'    
    words_to_be_excluded = ['p','np','r','s','thread','say','will','need','india\'','t','u','modi\'','k','e','go',\
                            'see','x','still','vs','says','may','.',',',';']
    

    comments = fetchAndProcessComments()
    text = getCommentsAsSingleString(comments)
    makeCloud(text, imgFile, words_to_be_excluded)
    writeFreq(text, freqFile, words_to_be_excluded)
    freqFile.close()
    
# Call Main 
main()
