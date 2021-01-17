import json, sys, os, xmltodict, csv
from os.path import join
from utils import *
import shutil

PATH = sys.argv[1]
DIR = PATH.replace('extracted/','')

print("importing",DIR)

file = join(PATH,'Posts.xml')

# clean方法用于移除x中的特殊字符
def clean(x):
    #neo4j-import doesn't support: multiline (coming soon), quotes next to each other and escape quotes with '\""'
    return x.replace('\n','').replace('\r','').replace('\\','').replace('"','')

def open_csv(name):
    return csv.writer(open('csvs/{}.csv'.format(name), 'w'), doublequote=False, escapechar='\\')

try:
    # 该方法递归删除文件夹下的所有子文件夹和子文件
    shutil.rmtree('csvs/')
except:
    pass
os.mkdir('csvs')

posts = open_csv('posts')
posts_rel = open_csv('posts_rel')
users = open_csv('users')
users_posts_rel = open_csv('users_posts_rel')
tags = open_csv('tags')
tags_posts_rel = open_csv('tags_posts_rel')

posts.writerow(['postId:ID(Post)', 'title', 'body','score','views','comments'])
posts_rel.writerow([':START_ID(Post)', ':END_ID(Post)'])

users_things = ['displayname', 'reputation', 'aboutme', \
    'websiteurl', 'location', 'profileimageurl', 'views', 'upvotes', 'downvotes']
users.writerow(['userId:ID(User)'] + users_things)
users_posts_rel.writerow([':START_ID(User)', ':END_ID(Post)'])

tags.writerow(['tagId:ID(Tag)'])
tags_posts_rel.writerow([':START_ID(Post)', ':END_ID(Tag)'])

# enumerate 对于一个可迭代的（iterable）/可遍历的对象（如列表、字符串），enumerate将其组成一个索引序列，利用它可以同时获得索引和值
for i, line in enumerate(open(file, encoding="gbk", errors="ignore")):
    # strip用于移除字符串头尾指定的字符或字符序列（默认是空格或换行符）
    line = line.strip()
    try:
        if line.startswith("<row"):
            # parse方法将xml变得像json
            el = xmltodict.parse(line)['row']
            # replace_keys用于将每项的key改为小写并且移除'@'字符
            el = replace_keys(el)
            posts.writerow([
                el['id'],
                clean(el.get('title','')),
                clean(el.get('body',''))[:100],
                clean(el.get('score','')),
                clean(el.get('viewcount','')),
                clean(el.get('commentcount','')),
            ])
            if el.get('parentid'):
                posts_rel.writerow([el['parentid'],el['id']])
            if el.get('owneruserid'):
                users_posts_rel.writerow([el['owneruserid'],el['id']])
            if el.get('tags'):
                eltags = [x.replace('<','') for x in el.get('tags').split('>')]
                for tag in [x for x in eltags if x]:
                    tags_posts_rel.writerow([el['id'],tag])
    except Exception as e:
        print('x',e)
    if i and i % 5000 == 0:
        print('.',end='')
    if i and i % 1000000 == 0:
        print(i)

print(i,'posts ok')

file = join(PATH,'Users.xml')

for i, line in enumerate(open(file, encoding="gbk", errors="ignore")):
    line = line.strip()
    try:
        if line.startswith("<row"):
            el = xmltodict.parse(line)['row']
            el = replace_keys(el)
            row = [el['id'],]
            for k in users_things:
                row.append(clean(el.get(k,'')[:100]))
            users.writerow(row)
    except Exception as e:
        print('x',e)
    if i % 5000 == 0:
        print('.',end='')

print(i,'users ok')

file = join(PATH,'Tags.xml')

for i, line in enumerate(open(file, encoding="gbk", errors="ignore")):
    line = line.strip()
    try:
        if line.startswith("<row"):
            el = xmltodict.parse(line)['row']
            el = replace_keys(el)
            tags.writerow([
                el['tagname'],
            ])
    except Exception as e:
        print('x',e)
    if i % 5000 == 0:
        print('.',end='')

print(i,'tags ok')
