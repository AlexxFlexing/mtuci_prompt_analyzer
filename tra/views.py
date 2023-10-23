from django.shortcuts import render
import random
from string import ascii_letters
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# Create your views here.

def home(request):
    context = {
        'random_str': random_string()
    }
    return render(request, "home.html",context)

def random_string():
    random_str = ''
    for i in range(random.randint(31,63)):
        random_str += random.choice(ascii_letters)
    return random_str

