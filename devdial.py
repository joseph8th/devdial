#!/usr/bin/env python3

"""
Ring phones in paging group 999 and play Salt'n Peppa OR Baby Fuckin' Wheel.
AUTHORS: Mark Warren, Joseph Edwards
"""

import os, sys
import argparse
from asterisk.ami import AMIClient
from asterisk.ami.action import SimpleAction

VERBOSE=False


def dev_dial(action):
    """Function that actually makes the asterisk call."""

    try:
        client = AMIClient(address='10.0.4.61', port=5038)
        client.login(username='devmin', secret='KnWaRpm0Rhcu')

        future = client.send_action(action)
        if VERBOSE:
            print(future.response or "None")

        client.logoff()

    except Exception as e:
        print("Error: %s" % e.strerror)
        sys.exit(1)


if __name__=="__main__":
    # Follow symbolic link
    realfile = os.path.realpath(__file__)

    # If we have a channel map then use those as choices instead of any numeric
    CHANNEL_MAP = None
    if os.path.exists(os.path.join(os.path.dirname(realfile), 'settings.py')):
        from settings import CHANNEL_MAP
    description = "Channel choices: {"+', '.join(CHANNEL_MAP.keys())+"}" if CHANNEL_MAP else None

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("channel", nargs="?", default='999', help="the channel to play")
    parser.add_argument("-v", "--verbose", action="store_true", help="output asterisk responses")
    parser.add_argument("-o", "--outbound", help="outbound number to dial")
    parser.add_argument("-e", "--exten", help="extension to dial")
    parser.add_argument(
        "-c", "--caller_id", default="CES <3052328182>", help="CallerID string, i.e., 'CES <3052328182>'"
    )
    args = parser.parse_args()

    # If we used the channel map, then get the correct channel for the choice
    if not args.channel.isnumeric():
        if not CHANNEL_MAP:
            sys.exit("Unrecognized channel slug '{0}'".format(args.channel))
        else:
            args.channel = CHANNEL_MAP[args.channel]

    # Config args for asterisk action
    if args.outbound:
        cdict = {
            "Channel": "SIP/vitelity-outbound/{outbound}".format(outbound=args.outbound),
            "Context": "app-miscapps",
            "Exten": "*{channel}".format(channel=args.channel),
        }
    elif args.exten:
        cdict = {
            "Channel": "SIP/{exten}".format(exten=args.exten),
            "Context": "app-miscapps",
            "Exten": "*{channel}".format(channel=args.channel),
        }
    else:
        cdict = {
            "Channel": "Local/*{channel}@app-miscapps".format(channel=args.channel),
            "Context": "ext-paging",
            "Exten": "999"
        }

    cdict.update({"CallerID": args.caller_id, "Priority": 1,})

    VERBOSE = args.verbose
    if VERBOSE:
        print(cdict)

    # Create action and dial
    action = SimpleAction("Originate", **cdict)
    dev_dial(action)
