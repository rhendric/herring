from celery import shared_task
from puzzles.models import Puzzle
from herring.secrets import SECRETS
import slacker

# A token logged in as a legitimate user. Turns out that "bots" can't
# do the things we want to automate!
SLACK = slacker.Slacker(SECRETS['slack-user-token'])


@shared_task
def create_puzzle_channel(slug):
    puzzle = Puzzle.objects.get(slug=slug)
    channel_name = '#' + slug
    try:
        created = SLACK.channels.create(channel_name)
    except slacker.Error:
        created = SLACK.channels.join(channel_name)

    channel_id = created.body['channel']['id']
    SLACK.channels.set_topic(channel_id, puzzle.name)
    SLACK.channels.set_purpose(channel_id, 'solving {}'.format(puzzle.hunt_url))
    
    # not using pinned messages, yet, but leaving this for future reference
    #posted = SLACK.chat.post_message(channel_id, hunt_link)
    #msg_timestamp = posted.body['ts']
    #SLACK.pins.add(channel_id, timestamp=msg_timestamp)

