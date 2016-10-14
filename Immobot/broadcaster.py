from slackclient import SlackClient
from private import slackToken

def slackBroadcast(avis, area, price,bart_dist,name, url) :

    SLACK_CHANNEL = "#immobilier"

    sc = SlackClient(slackToken)
    desc = "{0} | {1} m2 | {2} EUR | {3} | {4} | <{5}>".format(avis, area, price,bart_dist,name, url)

    sc.api_call(
        "chat.postMessage", channel=SLACK_CHANNEL, text=desc,
        username='pybot', icon_emoji=':robot_face:'
    )