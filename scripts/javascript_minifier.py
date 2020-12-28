# Usage: python javascript_minifier.py

# -*- coding: utf-8 -*-
import os, sys
import requests

SOURCE_DIR = 'D:\\Workspaces\\Django\\django_chinese\\src\\static\\site\\js'

def minifier(path):
    print(path)
    # Grab the file contents
    js = None
    with open(path, 'r') as rfile:
        js = rfile.read()

    # Pack it, ship it    
    payload = {'input': js}
    url = 'https://javascript-minifier.com/raw'
    print("Requesting minify of {}. . .".format(path.split('/')[-1]))
    response = requests.post(url, payload).text

    # Write out minified version
    js_min_file = path.replace('.js', '.min.js')
    with open(js_min_file, 'w') as wfile:
        wfile.write(response)

    print("Minification complete. See {}\n".format(js_min_file.split('/')[-1]))

try:
    items = os.listdir(SOURCE_DIR)
    for item in items:
        if ('.js' in item) and ('.min.js' not in item):
            minifier(os.path.join(SOURCE_DIR, item))
        # First level directory
        elif (not '.DS_Store' in item) and (not '.min.js' in item):
            subitems = os.listdir(os.path.join(SOURCE_DIR, item))
            for subitem in subitems:
                if ('.js' in subitem) and ('.min.js' not in subitem):
                    minifier(os.path.join(SOURCE_DIR, item, subitem))
                elif (not '.DS_Store' in subitem) and (not '.min.js' in subitem):
                    subsubitems = os.listdir(os.path.join(SOURCE_DIR, item, subitem))
                    for subsubitem in subsubitems:
                        if ('.js' in subsubitem) and ('.min.js' not in subsubitem):
                            minifier(os.path.join(SOURCE_DIR, item, subitem, subsubitem))
except Exception as e:
    print(e)
    sys.exit()

