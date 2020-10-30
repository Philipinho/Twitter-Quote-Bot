from tweepy import Stream, StreamListener, TweepError
from config import authenticate_api

bot_username = "BOT_USERNAME_HERE"


def success_response(user_replied_to, tweet_referenced_id):
    reply = "@" + user_replied_to + " https://twitter.com/search?q=url:" + str(tweet_referenced_id) \
            + "%20-from:" + bot_username + "&src=live"

    return reply


class MentionStream(StreamListener):

    def __init__(self, api):
        super(StreamListener, self).__init__()
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        tweet_referenced_id = "-1"

        if hasattr(tweet, 'quoted_status'):
            tweet_referenced_id = tweet.quoted_status_id

        elif tweet.in_reply_to_status_id is not None:
            tweet_referenced_id = tweet.in_reply_to_status_id

        if tweet_referenced_id is not "-1" and (str(tweet.user.screen_name).lower() is not bot_username
                                                or str(tweet.in_reply_to_screen_name).lower() is not bot_username):

            mention_id = tweet.id
            user_to_reply = tweet.user.screen_name

            response_message = success_response(user_to_reply, str(tweet_referenced_id))

            try:
                self.api.update_status(response_message, mention_id)
                print("Replied to " + user_to_reply)
            except TweepError as e:
                print(e)
                pass

    def on_error(self, status):
        print(status + " streaming error")


def main():
    while True:
        try:
            api = authenticate_api()
            tweets_listener = MentionStream(api)

            user_to_track = "@" + bot_username

            stream = Stream(api.auth, tweets_listener)
            stream.filter(track=[user_to_track])

        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
