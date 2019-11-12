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
import csv
import traceback

from parser_utils import find_intro
from parser_utils import find_plot
from parser_utils import find_info
from parser_utils import clean_all
from parser_utils import save_as_tsv

save_as_tsv()
