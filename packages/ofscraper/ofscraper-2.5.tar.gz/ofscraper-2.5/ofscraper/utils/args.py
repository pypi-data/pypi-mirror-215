import argparse
import logging
import sys
import re
import arrow
import pathlib
from ofscraper.__version__ import __version__ 

args=None
log=logging.getLogger(__package__)
def getargs(input=None):
    global args
    if args and input==None:
        return args
    if "pytest" in sys.modules and input==None:
        input=[]
    elif input==None:
        input=sys.argv[1:]
    parent_parser=argparse.ArgumentParser(add_help=False)
    general=parent_parser.add_argument_group("General",description="General Args")  
    general.add_argument('-v', '--version', action='version', version=__version__ ,default=__version__)
    output=parent_parser.add_argument_group("Logging",description="Arguments for output controls")  

    output.add_argument(
        '-l', '--log', help = 'set log file level', type=str.upper,default="OFF",choices=["OFF","STATS","LOW","NORMAL","DEBUG"]
    ),
    output.add_argument(
        '-dc', '--discord', help = 'set discord log level', type=str.upper,default="OFF",choices=["OFF","STATS","LOW","NORMAL","DEBUG"]
    )

    output.add_argument(
        '-p', '--output', help = 'set console output log level', type=str.upper,default="NORMAL",choices=["PROMPT","STATS","LOW","NORMAL","DEBUG"]
    )
    output.add_argument(
        '-cg', '--config', help="Change location of config folder/file",default=None
    )
    output.add_argument(
        '-au', '--auth', help="Change location of auth file",default=None
    )


    parser = argparse.ArgumentParser(add_help=False,parents=[parent_parser])  
    parser.add_argument( '-h', '--help', action='help')
    scraper=parser.add_argument_group("scraper",description="General Arguments for scraper")                                
    scraper.add_argument(
        '-u', '--username', help="select which username to process (name,name2)\nSet to ALL for all users",type=username_helper,action="extend"
    )
    scraper.add_argument(
        '-eu', '--excluded-username', help="select which usernames to exclude  (name,name2)\nThis has preference over --username",type=username_helper,action="extend"
    )
  
    scraper.add_argument(
        '-d', '--daemon', help='run script in the background\nSet value to minimum minutes between script runs\nOverdue runs will run as soon as previous run finishes', type=int,default=None
    )

    scraper.add_argument(
        '-g', '--original', help = 'don\'t trunicate long paths', default=False,action="store_true"
    )


    post=parser.add_argument_group("Post",description="What type of post to scrape")                                      

    post.add_argument("-e","--dupe",action="store_true",default=False,help="Bypass the dupe check and redownload all files")
    post.add_argument(
        '-o', '--posts', help = 'Download content from a model',default=[],required=False,type = posttype_helper,action='extend'
    )
    post.add_argument("-c","--letter-count",action="store_true",default=False,help="intrepret config 'textlength' as max length by letter")

    post.add_argument("-a","--action",default=None,help="perform like or unlike action on each post",choices=["like","unlike"])
    post.add_argument("-sk","--skip-timed",default=None,help="skip promotional or tempory post",action="store_true")
    post.add_argument(
        '-ft', '--filter', help = 'Filter post by provide regex\nNote if you include any uppercase characters the search will be case-sensitive',default=".*",required=False,type = str
    )
    post.add_argument(
        '-sp', '--scrape-paid', help = 'scrape the entire paid page for content. This can take a very long time',default=False,required=False,action="store_true"
    )
    post.add_argument(
        '-nc', '--no-cache', help = 'disable cache',default=False,required=False,action="store_true"
    )

     #Filters for accounts
    filters=parser.add_argument_group("filters",description="Filters out usernames based on selected parameters")
    
    filters.add_argument(
        '-at', '--account-type', help = 'Filter Free or paid accounts\npaid and free correspond to your original price, and not the renewal price',default=None,required=False,type = str.lower,choices=["paid","free"]
    )
    filters.add_argument(
        '-rw', '--renewal', help = 'Filter by whether renewal is on or off for account',default=None,required=False,type = str.lower,choices=["active","disabled"]
    )
    filters.add_argument(
        '-ss', '--sub-status', help = 'Filter by whether or not your subscription has expired or not',default=None,required=False,type = str.lower,choices=["active","expired"]
    )
    filters.add_argument(
        '-be', '--before', help = 'Process post at or before the given date general synax is Month/Day/Year\nWorks for like,unlike, and downloading posts',type=arrow_helper)
 
    filters.add_argument(
        '-af', '--after', help = 'Process post at or after the given date Month/Day/Year\nnWorks for like,unlike, and downloading posts',type=arrow_helper)
    
    
    sort=parser.add_argument_group("sort",description="Options on how to sort list")
    sort.add_argument(
        '-st', '--sort', help = 'What to sort the model list by',default="Name",choices=["Name","Subscribed","Expiring","Price"],type=str.lower)
    sort.add_argument(
        '-ds', '--desc', help = 'Sort the model list in descending order',action="store_true",default=False) 
    
    advanced=parser.add_argument_group("Advanced",description="Advanced Args")  
    advanced.add_argument(
        '-uf', '--users-first', help = 'Scrape all users first rather then one at a time. This only effects downloading posts',default=False,required=False,action="store_true"
    )

    subparser=parser.add_subparsers(help="commands",dest="command")
    post_check=subparser.add_parser("post_check",help="Check if data from a post\nCache lasts for 24 hours",parents=[parent_parser])


    post_check.add_argument("-u","--url",
    help = 'Check if media is in library via url',default=None,required=False,type = check_strhelper,action='extend'
    )


    post_check.add_argument("-f","--file",
    help = 'Check if media is in library via file',default=None,required=False,type = check_filehelper
    )
    
    post_check.add_argument(
        '-fo', '--force', help = 'force retrival of new posts info from API', default=False,action="store_true"
    )

    message_check=subparser.add_parser("msg_check",help="Parse a user's messages and view status of missing media\nCache lasts for 24 hours",parents=[parent_parser])
    message_check.add_argument(
        '-fo', '--force', help = 'force retrival of new posts info from API', default=False,action="store_true"
    )
    message_check.add_argument("-f","--file",
    help = 'Check if media is in library via file',default=None,required=False,type = check_filehelper
    )
    

    message_check.add_argument("-u","--url",
    help = 'link to conversation',type = check_strhelper,action="extend")
    message_check.add_argument("-un","--username",
    help = 'link to conversation',type = check_strhelper,action="extend")

    paid_check=subparser.add_parser("paid_check",help="Parse Purchases sent from a user\nCache last for 24 hours",parents=[parent_parser])
    paid_check.add_argument(
        '-fo', '--force', help = 'force retrival of new posts info from API', default=False,action="store_true"
    )
    paid_check.add_argument("-f","--file",
    help = 'Check if media is in library via file',default=None,required=False,type = check_filehelper
    )
    

    paid_check.add_argument("-us","--username",
    help = 'link to conversation',type = check_strhelper,action="extend")




    story_check=subparser.add_parser("story_check",help="Parse Stories/Highlights sent from a user\nCache last for 24 hours",parents=[parent_parser])
    story_check.add_argument(
        '-fo', '--force', help = 'force retrival of new posts info from API', default=False,action="store_true"
    )
    story_check.add_argument("-f","--file",
    help = 'Check if media is in library via file',default=None,required=False,type = check_filehelper
    )
    

    story_check.add_argument("-us","--username",
    help = 'link to conversation',type = check_strhelper,action="extend")

    manual=subparser.add_parser("manual",help="Manually download content via url or ID",parents=[parent_parser])
    manual.add_argument("-f","--file",
    help = 'Pass links/IDs to download via file',default=None,required=False,type = check_filehelper
    )
    manual.add_argument("-us","--url",
    help = 'pass links to download via url',type = check_strhelper,action="extend")


    args=parser.parse_args(input)
    #deduplicate posts
    args.posts=list(set(args.posts or []))
    args.username=set(args.username or [])
    args.excluded_username=set( args.excluded_username or [])

    if args.command=="post_check" and not (args.url or args.file):
        raise argparse.ArgumentTypeError("error: argument missing --url or --file must be specified )")

    return args



def check_strhelper(x):
    temp=None
    if isinstance(x,list):
        temp=x
    elif isinstance(x,str):
        temp=x.split(",")
    return temp

def check_filehelper(x):
    if isinstance(x,str) and pathlib.Path(x).exists():
        with open(x,"r") as _:
           return _.readlines()

   
    
def posttype_helper(x):
    choices=set(["Highlights","All","Archived","Messages","Timeline","Pinned","Stories","Purchased","Profile","None"])
    if isinstance(x,str):
        x=x.split(',')
        x=list(map(lambda x:x.capitalize() ,x))
    if len(list(filter(lambda y: y not in choices,x)))>0:
        raise argparse.ArgumentTypeError("error: argument -o/--posts: invalid choice: (choose from 'highlights', 'all', 'archived', 'messages', 'timeline', 'pinned', 'stories', 'purchased','profile')")
    return x

def changeargs(newargs):
    global args
    args=newargs


def username_helper(x):
    temp=None
    if isinstance(x,list):
        temp=x
    elif isinstance(x,str):
        temp=x.split(",")
    return temp

def arrow_helper(x):
    print(x)
    try:
        return arrow.get(x)
    except arrow.parser.ParserError as E:
        try:
            x=re.sub("\\byear\\b","years",x)
            x=re.sub("\\bday\\b","days",x)
            x=re.sub("\\bmonth\\b","months",x)
            x=re.sub("\\bweek\\b","weeks",x)
            print(x)
            arw=arrow.utcnow()
            return arw.dehumanize(x)
        except ValueError as E:
             raise E


