import requests

APP_ACCESS_TOKEN='5652039245.018aba3.9a7b64bde08f455fafc078efca07fb6a'
BASE_URL='https://api.instagram.com/v1/'


def get_user_id(insta_username):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code'] == 200:
      if len(user_info['data']):
          return user_info['data'][0]['id']
      else:
          return None
  else:
      print 'Status code other than 200 received!'
      exit()





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
          return user_media['data'][0]['id']
      else:
          print "There is no recent post!"
  else:
      print "Status code other than 200 received!"
  return None

def like_a_post(insta_username):
  media_id = get_user_post(insta_username)
  request_url = (BASE_URL + 'media/%s/likes') % (media_id)
  payload = {"access_token": APP_ACCESS_TOKEN}
  print 'POST request url : %s' % (request_url)
  post_a_like = requests.post(request_url, payload).json()


  if post_a_like['meta']['code'] == 200:

     print 'Like was successful!'
  else:
      print 'Your like was unsuccessful. Try again!'

like_a_post('samrao_aman')



def post_a_comment(insta_username):
  media_id = get_user_post(insta_username)
  comment_text = raw_input("Your comment: ")
  payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
  request_url = (BASE_URL + 'media/%s/comments') % (media_id)
  print 'POST request url : %s' % (request_url)

  make_comment = requests.post(request_url, payload).json()
  if make_comment['meta']['code'] == 200:
      print "Successfully added a new comment!"
  else:
      print "Unable to add comment. Try again!"
post_a_comment('samrao_aman')