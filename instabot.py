import matplotlib.pyplot as plt  # Matplotlib is  a Python 2D plotting library which produces figures
import requests,urllib   #urllib is a package that collects information all over the world .Requests library to send http request
import pylab
import re # Library for regular expression
from wordcloud import WordCloud  # An image composed of words used in a particular text or subject, in which the size of each word indicates its frequency or importance.
APP_ACCESS_TOKEN='5652039245.018aba3.9a7b64bde08f455fafc078efca07fb6a' #Access token for authenticated user(Here its mine)

#Users: "brar_japji","simoni3604","bhavikaa_singla"
BASE_URL='https://api.instagram.com/v1/' # url same in all is a base url

# Function definition to show Access token's owner's details
def self_info():
    request_url=(BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print '\n'
            print "Owner's informtion : "
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

# Function definition to fetch user id by username
def get_user_id(insta_username):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
      if len(user_info['data']):
          return user_info['data'][0]['id']   # return user id
      else:
          return None
  else:
      print 'Status code other than 200 received!'
      exit()


# Function definition to retrieve user information .The function makes use of user id
def get_user_info(insta_username):
  user_id = get_user_id(insta_username)
  if user_id == None:
      print 'User does not exist!'
      exit()
  request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
      if len(user_info['data']):
          print '\n'
          print "Another User's information"
          print 'Username: %s' % (user_info['data']['username'])
          print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
          print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
          print 'No. of posts: %s' % (user_info['data']['counts']['media'])
      else:
          print 'There is no data for this user!'
  else:
      print 'Status code other than 200 received!'


# Function definition to get the most recent post of the owner
def get_own_post():
    request_url=(BASE_URL +'users/self/media/recent/?access_token=%s')% (APP_ACCESS_TOKEN)
    own_media=requests.get(request_url).json()

    if own_media['meta']['code']==200:
        if len(own_media['data']):
          image_name = own_media['data'][0]['id'] + '.jpeg'
          image_url = own_media['data'][0]['images']['standard_resolution']['url']
          urllib.urlretrieve(image_url, image_name)
          print 'Your image has been downloaded!'
        else:
            print "post doesnot exist"
    else:
        print "status code other than 200 received"


# Function definition to get the most recent post of the user by username
def get_user_post(insta_username):
  user_id = get_user_id(insta_username)
  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_media = requests.get(request_url).json()

  if user_media['meta']['code'] == 200:
      if len(user_media['data']):
          image_name = user_media['data'][0]['id'] + '.jpeg'
          image_url = user_media['data'][0]['images']['standard_resolution']['url']
          urllib.urlretrieve(image_url, image_name)
          print 'Your image has been downloaded!'
      else:
          print 'Post does not exist!'
  else:
      print 'Status code other than 200 received!'


# Function definition returns the recent post id
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()
# Function to like a user's post
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

# Function definition to post a comment on user's post
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    text_words=comment_text.split(" ")
    if not any (words.islower() for words in text_words):
        print "Sorry !! you cannot enter a comment with all capital alphabets ."
    elif len(text_words) >=300:
        print "You cross your text limit!!!!"
    elif len(re.findall(r'#[^#]+\b',comment_text,re.UNICODE|re.MULTILINE))>4:
        print "THE COMMENT CANNOT CONTAIN MORE THAN 4 HASHTAGS"
    elif len(re.findall(r'\bhttps?://\S+\.\S+', comment_text)) > 1:
        print "THE COMMENT CANNOT CONTAIN MORE THAN ONE URL"
    else:
        payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
        request_url = (BASE_URL + 'media/%s/comments') % (media_id)
        print 'POST request url : %s' % (request_url)

        make_comment = requests.post(request_url, payload).json()

        if make_comment['meta']['code'] == 200:
            print "Successfully added a new comment!"
        else:
            print "Unable to add comment. Try again!"
# Function to show a list of comments on recent media of user
def list_of_comments(insta_username):
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,APP_ACCESS_TOKEN)

  get_comments=requests.get(request_url).json()
  x = 0
  if get_comments['meta']['code'] == 200:
      for ele in get_comments['data']:
           print get_comments['data'][x]['from']['username'] + ":" + get_comments['data'][x]['text']
           x=x+1
  else:
      print "Status code other than 200 received!"
# Function to do hash analysis of user's post and to plot a graph
def list_of_tags(insta_username):
  hash_item = {}
  user_id = get_user_id(insta_username)
  if user_id == None:
      print "User does not exist!"
      exit()
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id,APP_ACCESS_TOKEN)
  user_media=requests.get(request_url).json()
  if user_media['meta']['code'] == 200:
      if len(user_media['data']):
          for media in range(0, len(user_media['data'])):
              print user_media['data'][media]['tags']
              my_tag_len = len(user_media['data'][media]['tags'])

              for y in range(0, my_tag_len):

                  if user_media['data'][media]['tags'][y] in hash_item:
                      hash_item[user_media['data'][media]['tags'][y]] = hash_item[user_media['data'][media]['tags'][y]] + 1
                  else:
                      hash_item[user_media['data'][media]['tags'][y]] = 1
      else:
          print "Post does not exist!!"
  else:
      print "Status code other than 200 received!"
  print hash_item
  pylab.figure(1)
  x = range(len(hash_item))
  pylab.xticks(x, hash_item.keys())
  pylab.plot(x, hash_item.values(), "g")
  pylab.show()

# Wordcloud to show how many times a tag is appearing and based on that analysis is done
  wordcloud = WordCloud().generate_from_frequencies(hash_item)
  plt.imshow(wordcloud, interpolation="bilinear")
  plt.axis("off")
  plt.show()
# Function definition to show list of likes on user media
def list_of_likes(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    likes = requests.get(request_url).json()
    i=0
    if likes['meta']['code']==200:
        if len(likes['data']):
            for ele in likes['data']:
                print likes['data'][i]['username']
                i=i+1
        else:
            print "post doesnot exist"
    else:
        print "status code other than 200 received"
# Function definition to fetch recent media liked by the user
def recent_media_like():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print "No post liked"
    else:
        print "status code other than 200 received"
# Function definition to get media of user's choice by  taking input from user as index
def get_media_of_your_choice(insta_username):
     user_id = get_user_id(insta_username)
     if user_id == None:
         print 'user does not exist'
     request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
     user_media = requests.get(request_url).json()
     if user_media['meta']['code'] == 200:
         if len(user_media['data']):
             post_number = raw_input("enter no of post which you want : ")
             post_number = int(post_number)
             x = post_number - 1 # Zero based indexing...

             if x<len(user_media['data']):


                 image_name = user_media['data'][x]['id'] + '.jpeg'
                 image_url = user_media['data'][x]['images']['standard_resolution']['url']
                 urllib.urlretrieve(image_url, image_name)
                 print 'Your image has been downloaded!'
             else:
                 print "No media found!!"
         else:
             print'media does not exist'
     else:
         print 'status code error'


#Function definition to start the Instabot
def start_bot():
    print 'Hey! Welcome to instaBot!'
    while True:
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Like the recent post of a user\n"
        print "f.Get a list of comments on the recent post of a user\n"
        print "g.Make a comment on the recent post of a user\n"
        print "h.Wordcloud of user interest\n"
        print "i.Get list of user who liked the recent media\n"
        print "j.Get the recent post liked by the user\n"
        print "k.Get the media of your choice\n"
        print "l.Exit"

        choice = raw_input("Enter you choice: ")
        # Calling of different functions based on user choice
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)>0 and insta_username.isspace()== False and insta_username.isdigit()== False:

             get_user_info(insta_username)
            else:
                print "Please enter a valid username"
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)>0 and insta_username.isspace()== False and insta_username.isdigit()== False:
             get_user_post(insta_username)
            else:
             print "Please enter a valid username"
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)>0 and insta_username.isspace()== False and insta_username.isdigit()== False:
             like_a_post(insta_username)
            else:
                print "Please enter a valid username"
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)>0 and insta_username.isspace()== False and insta_username.isdigit()== False:
             list_of_comments(insta_username)
            else:
                print "Please enter a valid username"
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)>0 and insta_username.isspace()== False and insta_username.isdigit()== False:
             post_a_comment(insta_username)
            else:
                print "Please enter a valid username"
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)>0 and insta_username.isspace()== False and insta_username.isdigit()== False:
             list_of_tags(insta_username)
            else:
             print "Please enter a valid username"
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)>0 and insta_username.isspace()== False and insta_username.isdigit()== False:
             list_of_likes(insta_username)
            else:
                print "Please enter a valid username"

        elif choice == "j":
            recent_media_like()
        elif choice == "k":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)>0 and insta_username.isspace()== False and insta_username.isdigit()== False:
             get_media_of_your_choice(insta_username)
            else:
                print "Please enter a valid username"

        elif choice == "l":
            exit()
        else:
            print "Wrong choice"



# Calling of the function start_bot() to start the instabot
start_bot()


