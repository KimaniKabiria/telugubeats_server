import random
import string
import time
def get_random_id(length=10):
    '''returns a 10 character random string containing numbers lowercase upper case'''
    '''http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python'''

    key_str = ("%.15f" % time.time())+"-" + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits+string.ascii_lowercase) for _ in range(length))
    #key_str = hashlib.md5(key_str).hexdigest()
    return key_str

