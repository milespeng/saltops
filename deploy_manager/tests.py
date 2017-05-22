import json

from django.test import TestCase

# Create your tests here.
a = {

}
a['rs'] = 1
a['a'] = []
print(json.dumps(a))
