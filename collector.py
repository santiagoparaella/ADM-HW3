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
import hader as h

for i in range(1, 4, 1):
    url=h.PATH_MOVIE_DOWNLOAD+'movies'+str(i)+'.html'
    cu.crawl(url, h.PATH_MOVIE)
