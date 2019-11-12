import requests as req
from bs4 import BeautifulSoup
import random
import time
import os
import codecs
import re
import json
import numpy as np
import collections

import collector_utils as cu
path = "/Users/Dario/Desktop/HMW3_Data/"

for i in range(1, 4, 1):
    url='https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies'+str(i)+'.html'
    cu.crawl(url, '/tmp/')
