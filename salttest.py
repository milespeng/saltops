import yaml

from saltjob.salt_https_api import salt_api_token, salt_api_jobs
from saltjob.salt_token_id import token_id
from saltops.settings import SALT_REST_URL

# ins = salt_api_token({'fun': 'saltutil.find_job', 'tgt': '*'},
#                      SALT_REST_URL, {'X-Auth-Token': token_id()})
# rs = salt_api_jobs(url=SALT_REST_URL, token=token_id())
# minions_list_all = salt_api_jobs(
#     url=SALT_REST_URL + '/jobs',
#     token=token_id()
# )
# voilet_test = minions_list_all.run()
# while True:
#     print(voilet_test)
# rs = open('/home/kira/dev/github/saltops/doc/script/ls.sls', 'r')

# r = yaml.load(rs)
# print(r)
