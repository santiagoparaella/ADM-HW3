import collector_utils as cu

for i in range(1, 4, 1):
    url='https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies'+str(i)+'.html'
    cu.crawl(url, '/tmp/')  # path /tmp/ it's only an exaple. We changed it.
