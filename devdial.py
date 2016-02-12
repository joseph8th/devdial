#!/usr/bin/env python3

"""
Ring phones in paging group 999 and play Salt'n Peppa OR Baby Fuckin' Wheel.
AUTHOR: GroundControl (Mark Warren)
"""

import asterisk.manager
import sys

def page_channel(channel):

    try:
        # connect to the manager
        try:
            manager.connect('10.0.4.61')
            manager.login('devmin', 'KnWaRpm0Rhcu')

            # get a status report
            response = manager.status()
            #print(response)
            # Logic to do the dialing
            response = manager.command(
                'channel originate Local/*{0}@app-miscapps extension 999@ext-paging'.format(
                    channel
                )
            )
            #print(response.data)

            manager.logoff()
        except asterisk.manager.ManagerSocketException as e:
            print ("Error connecting to the manager") % e.strerror
            sys.exit(1)
        except asterisk.manager.ManagerAuthException as e:
            print ("Error logging in to the manager") % e.strerror
            sys.exit(1)
        except asterisk.manager.ManagerException as e:
            print ("Error: %s") % e.strerror
            sys.exit(1)

    finally:
        # remember to clean up
        manager.close()


if __name__=="__main__":
    if len(sys.argv) == 2:
        channel = sys.argv[1]
    else:
        channel = 999

    manager = asterisk.manager.Manager()
    page_channel(channel)
