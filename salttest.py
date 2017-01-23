# import salt.client
# import time
#
# local = salt.client.LocalClient()
# jid = local.cmd_async('*', 'state.sls', ['es'])
# t = 0
# while not local.get_full_returns(jid,'*'):
#     time.sleep(1)
#     if t == 100:
#         print 'Connection Failed!'
#         break
#     else:
#         t += 1
#         print "Not Finish" + str(t)
#
# print local.get_full_returns(jid,'*')
import datetime

str = '15:38:30.077481'
datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
