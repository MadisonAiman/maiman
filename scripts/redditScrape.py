## Author: Carver Bray
## 
## Date Created: 11/6/2023
##
## Last Modified: 11/20/2023
##
## Script Purpose: Scrapes a group of reddit posts using the PRAW library and
##   outputs certain data into files to then go through sentiment analysis in a
##   separate script later.

import praw
from datetime import datetime

# get Reddit instance, which gives us access to the Reddit API, in general
# NOTE: Do NOT put quotes ("") around items in the praw.ini file
# This command will fail if you do that
reddit = praw.Reddit("bot1")

# create a list of submissions to go through
url_list = [
    "https://www.reddit.com/r/Superstonk/comments/z3mcze/wen_dfv/",
    "https://www.reddit.com/r/Superstonk/comments/yw9g65/dr_susanne_trimbath_on_twitter/",
    "https://www.reddit.com/r/Superstonk/comments/16uc4ve/gamestop_board_elected_ryan_cohen_as_ceo/",
    "https://www.reddit.com/r/Superstonk/comments/12k0fzq/ryan_cohen_on_twitter_i_just_got_off_the_phone/",
    "https://www.reddit.com/r/Superstonk/comments/vszcip/is_the_d_man_speaking_truth/",
    "https://www.reddit.com/r/Superstonk/comments/qge7p8/louder_for_the_people_in_the_back/",
    "https://www.reddit.com/r/Superstonk/comments/msblom/dfv/",
    "https://www.reddit.com/r/Superstonk/comments/14a1yye/drsusanne_trimbath_on_twitter/"
]

for url in url_list:
    submission = reddit.submission(url=url)
    print(submission)

    # clean out submission names for illegal characters
    title = submission.title
    title = title.replace(" ", "_")
    title = "".join(x for x in title if x.isalnum() or x == "_")

    subFile = open("../api-results/"+title+".md", "w")

    # === INITIAL POST SECTION ===
    author = "[deleted user]" if submission.author == None else (
            submission.author.name)
    flair = submission.link_flair_text
    body = submission.selftext
    embed = "![Embed from Reddit post](" + submission.url + ")"
    originalTimePosted = datetime.fromtimestamp(submission.created_utc)
    originalTimePosted = originalTimePosted.strftime("%m/%d/%Y, %H:%M:%S")

    fullContent = (author + " posted " + title + " at " + originalTimePosted)
    if embed != submission.permalink:
        fullContent += "\n with link " + embed
    if flair != None:
        fullContent += "\n with flair " + flair
    
    subFile.write(fullContent+"\n")

    # Delimiter for the sentiment analaysis script, since the initial post
    # is not a part of the analysis
    subFile.write("\nCOMMENTS-BEGIN:")

    # === COMMENTS SECTION ===
    # replace_more gets rid of the "load more comments" thing that pops up on 
    # Reddit so that all comments are loaded into the comments field
    submission.comments.replace_more(limit=None)
    submission.comment_sort = "top"

    # this is for a depth first search algorithm
    commentQueue = submission.comments[:]

    for i in range(0,99):
        comment = commentQueue.pop(0)

        username = "[deleted user]" if comment.author == None else (
            comment.author.name) 
        # skip automod comments
        if username == "Superstonk_QV":
            continue
        timePosted = datetime.fromtimestamp(comment.created_utc)
        timePosted = timePosted.strftime("%m/%d/%Y, %H:%M:%S")

        # Determine if comment is a reply or not
        # reddit.comment(parent_id) will get the parent comment to do stuff with
        # string[:2] is first two letters
        if comment.parent_id[:2] != "t3":
            prevCom = reddit.comment(comment.parent_id)
            previousUser = "[deleted user]" if prevCom.author == None else (
                prevCom.author.name)
            content = username + " replied to " + previousUser
        else:
            content = username + " commented"

        score = comment.score

        content += " at " + timePosted + " " + str(score) + " : " + comment.body

        subFile.write("\n"+content+"\n")

        commentQueue[0:0] = comment.replies
    
    subFile.close()
