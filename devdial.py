#!/usr/bin/env python3

"""
Ring phones in paging group 999 and play Salt'n Peppa OR Baby Fuckin' Wheel.
AUTHORS: Mark Warren, Joseph Edwards
"""

import asterisk.manager
import sys
import argparse

VERBOSE=False

def handle_shutdown(event, manager):
    if VERBOSE:
        print("Received shutdown event")
    manager.close()

def handle_event(event, manager):
    if VERBOSE:
        print("Received event: %s" % event.name)


def dev_dial(command):
    manager = asterisk.manager.Manager()

    # connect to the manager
    try:
        manager.connect('10.0.4.61')
        manager.login('devmin', 'KnWaRpm0Rhcu')

        # register some callbacks
        manager.register_event('Shutdown', handle_shutdown) # shutdown
        #manager.register_event('*', handle_event) # all

        # Logic to do the dialing
        response = manager.command(command)

        """
        response = manager.send_action({
            "Action": "Originate",
            "Channel": "SIP/vitelity-outbound/15757378046",
            "CallerID": "CES <3052328182>",
            "Context": "app-miscapps",
            "Exten": "*1005",
            "Timeout": 30,
            "Account": "default"
        })
        """

        if VERBOSE:
            print("Response:", response.data or "None")

        # get a status report
        if VERBOSE:
            response = manager.status()
            print("Status:", response)

        manager.logoff()

    except asterisk.manager.ManagerSocketException as e:
        print("Error connecting to the manager" % e.strerror)
        sys.exit(1)
    except asterisk.manager.ManagerAuthException as e:
        print("Error logging in to the manager" % e.strerror)
        sys.exit(1)
    except asterisk.manager.ManagerException as e:
        print("Error: %s" % e.strerror)
        sys.exit(1)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("channel", nargs="?", default='999', help="the channel to play")
    parser.add_argument("-e", "--extern", help="external number to dial")
    parser.add_argument("-v", "--verbose", action="store_true", help="output asterisk responses")
    args = parser.parse_args()

    page_cmd = 'channel originate Local/*{channel}@app-miscapps extension 999@ext-paging'
    call_cmd = 'channel originate SIP/vitelity-outbound/{extern} extension *{channel}@app-miscapps'
    if not args.extern:
        command = page_cmd.format(channel=args.channel)
    else:
        command = call_cmd.format(channel=args.channel, extern=args.extern)

    VERBOSE = args.verbose
    dev_dial(command)
