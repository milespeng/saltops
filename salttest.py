from saltjob.salt_https_api import salt_api_token, salt_api_jobs
from saltjob.salt_token_id import token_id
from saltops.settings import SALT_REST_URL

# ins = salt_api_token({'fun': 'state.sls', 'tgt': '*', 'arg': 'ls'},
#                      SALT_REST_URL, {'X-Auth-Token': token_id()})
# result = ins.run()['return'][0]['jid']
#
# while True:
#     print(ins.loadJob(result))
