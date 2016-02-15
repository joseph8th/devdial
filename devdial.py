#!/usr/bin/env python3

"""
Ring phones in paging group 999 and play Salt'n Peppa OR Baby Fuckin' Wheel.
AUTHORS: Mark Warren, Joseph Edwards
"""

import asterisk.manager
import sys

CONNECT_IP = ''
LOGIN_UN = ''
LOGIN_PW = ''
PAGING_GROUP = 999

def page_channel(feature_code):

    try:
        # connect to the manager
        try:
            manager.connect(CONNECT_IP)
            manager.login(LOGIN_UN, LOGIN_PW)

            # get a status report
            response = manager.status()
            #print(response)
            # Logic to do the dialing
            response = manager.command(
                'channel originate Local/*{0}@app-miscapps extension {1}@ext-paging'.format(
                    feature_code, PAGING_GROUP
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
        feature_code = sys.argv[1]
    else:
        feature_code = 999

    manager = asterisk.manager.Manager()
    page_channel(feature_code)
