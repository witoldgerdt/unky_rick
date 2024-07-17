import sys

def is_testing(request):
    return {'is_testing': 'test' in sys.argv}
