import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import sys

arguments = sys.argv
u_flag = 0
t_flag = 0
o_flag = 0
for i in arguments:
    if(i == '-u'):
        u_flag = 1
    elif(i == '-t'):
        t_flag = 1
    elif(i == '-o'):
        o_flag = 1
    
if(t_flag == 0):
    print("Error!! Please enter valid threshold flag")
    sys.exit();
if(u_flag == 0):
    print("Error!! Please enter valid url flag")
    sys.exit()

threshold = int(arguments[4]);
if(threshold < 1):
    print("Errr!! Please enter valid threshold value")
    sys.exit()

def web_crawler(url, recursion_depth, store_link_dic, link_numbering):
    if(recursion_depth == (threshold+1)): return;

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    all_link = []  # collects all link in url file
    for href_link_tag in soup.find_all(href=True):  # extracting all href link in a list
        all_link.append(href_link_tag.get('href'))

    for src_link_tag in soup.find_all(src=True):  # extracting all src link in a list
        all_link.append(src_link_tag.get('src'))



    for link in all_link:  # iterating over all link
        parsed_url = urlparse(url)  # Parse the current web page URL
        parsed_link = urlparse(link)  # Parse the link URL

        if(parsed_link.netloc == ""):
            link = parsed_url.netloc+link
        if(parsed_link.scheme == ""):
            link = parsed_url.scheme+"://" + link  # making the internal link complet

        parsed_link = urlparse(link)  # Parse the link URL again

        is_internal = parsed_link.netloc == parsed_url.netloc  # Check if the link domain matches the current web page domain

        # Extract the file extension from the path or filename
        file_extension = os.path.splitext(parsed_link.path)[1]
        file_extension = file_extension[1:]

        # storing every link in a dictionary with key indicating internal/external and recursion depth
        if(is_internal):
            store_link_dic[file_extension + "," + "internal" + "," + str(recursion_depth) + "," + str(link_numbering)] = link
            link_numbering = link_numbering+1
            web_crawler(link, recursion_depth+1, store_link_dic, link_numbering)
        else:
            store_link_dic[file_extension + "," + "external" + "," + str(recursion_depth) + "," + str(link_numbering)] = link
            link_numbering = link_numbering+1


store_link_dic = {}  # stores all link corresponding to the file
url = arguments[2]
link_numbering = 1
web_crawler(url, 1, store_link_dic, link_numbering)

# All the link with required information is stored in store_link_dic dictionary
internal_dic = {} # will store internal links
external_dic = {} # will store external links
for key, value in store_link_dic.items():
    helper_list = key.split(',')
    if(helper_list[1] == 'internal'):
        internal_dic[key] = value
    else:
        external_dic[key] = value


# dealing with internal links
internal_main_dic = {}
for i in range(1,threshold+1):
    internal_main_dic[str(i)] = {};

for key, value in internal_dic.items():
    helper_list = key.split(",")
    if(helper_list[0] == ''): 
        helper_list[0] = "miscellaneous"
    if helper_list[0] in internal_main_dic[helper_list[2]]:
        internal_main_dic[helper_list[2]][helper_list[0]].append(value)
    else:
        internal_main_dic[helper_list[2]][helper_list[0]] = [value]


# dealing with external links
external_main_dic = {}
for i in range(1,threshold+1):
    external_main_dic[str(i)] = {};

for key, value in external_dic.items():
    helper_list = key.split(",")
    if(helper_list[0] == ''): 
        helper_list[0] = "miscellaneous"
    if helper_list[0] in external_main_dic[helper_list[2]]:
        external_main_dic[helper_list[2]][helper_list[0]].append(value)
    else:
        external_main_dic[helper_list[2]][helper_list[0]] = [value]
    

# output file name is given
if(o_flag == 1):  
    output_file_name = arguments[6]
    # writing my output in a file
    with open(f"{output_file_name}.txt", 'w') as file:
        file.write("<----------------------WEB CRAWLER---------------------->\n\n")

        # printing total number of link in given url
        total_link = len(store_link_dic) 
        file.write(f"Total number of link present in all the given recursion level is {total_link}\n\n")

        for i in range(1, (threshold+1)):
            file.write(f"<---------Recursion Level {i}--------->\n")

            # printing number of link a particular recursion level
            no_of_link_inside_recursion = 0
            for key, value in internal_main_dic[str(i)].items():
                no_of_link_inside_recursion += len(value)

            for key, value in external_main_dic[str(i)].items():
                no_of_link_inside_recursion += len(value)

            file.write(f"Total number of link in recursion level {i} is {no_of_link_inside_recursion}\n\n")
            # printing internal link
            file.write("[[Internal Links]]\n")
            #print number of internal link
            no_of_internal_link = 0
            for key, value in internal_main_dic[str(i)].items():
                no_of_internal_link += len(value)
            file.write(f"Total number of internal link in recursion level {i} is {no_of_internal_link}\n\n")
            
            # printing the internal link in a paticular recursion level
            for key,value in internal_main_dic[str(i)].items():
                file.write(f"{key}:\n")
                file.write(f"Total number of link in {key} is {len(value)}\n") # printing number of link in a particular extension
                for link in value:
                    file.write(f"{link}\n")
                file.write("\n")
            file.write("\n")

            # printing external link
            file.write("[[External Links]]\n")
            # printing number of external link
            no_of_external_link = 0
            for key, value in external_main_dic[str(i)].items():
                no_of_external_link += len(value)
            file.write(f"Total number of external link in recursion level {i} is {no_of_external_link}\n\n")

            # printing the external link in a particular recursion level
            for key,value in external_main_dic[str(i)].items():
                file.write(f"{key}:\n")
                file.write(f"Total number of link in {key} is {len(value)}\n") # printing number of link in a particular extension
                for link in value:
                    file.write(f"{link}\n")
                file.write("\n")
            file.write("<-------------------------------------------------------------------->\n\n")
        file.write("<--------------------END-------------------->")

# output file not given
else:
    print("<----------------------WEB CRAWLER---------------------->\n\n")

    # printing total number of link in given url
    total_link = len(store_link_dic) 
    print(f"Total number of link present in all the given recursion level is {total_link}\n\n")

    for i in range(1, (threshold+1)):
        print(f"<---------Recursion Level {i}--------->\n")

        # printing number of link a particular recursion level
        no_of_link_inside_recursion = 0
        for key, value in internal_main_dic[str(i)].items():
            no_of_link_inside_recursion += len(value)

        for key, value in external_main_dic[str(i)].items():
            no_of_link_inside_recursion += len(value)

        print(f"Total number of link in recursion level {i} is {no_of_link_inside_recursion}\n\n")
        # printing internal link
        print("[[Internal Links]]\n")
        #print number of internal link
        no_of_internal_link = 0
        for key, value in internal_main_dic[str(i)].items():
            no_of_internal_link += len(value)
        print(f"Total number of internal link in recursion level {i} is {no_of_internal_link}\n\n")
            
        # printing the internal link in a paticular recursion level
        for key,value in internal_main_dic[str(i)].items():
            print(f"{key}:\n")
            print(f"Total number of link in {key} is {len(value)}\n") # printing number of link in a particular extension
            for link in value:
                print(f"{link}\n")
            print("\n")
        print("\n")

        # printing external link
        print("[[External Links]]\n")
        # printing number of external link
        no_of_external_link = 0
        for key, value in external_main_dic[str(i)].items():
            no_of_external_link += len(value)
        print(f"Total number of external link in recursion level {i} is {no_of_external_link}\n\n")

        # printing the external link in a particular recursion level
        for key,value in external_main_dic[str(i)].items():
            print(f"{key}:\n")
            print(f"Total number of link in {key} is {len(value)}\n") # printing number of link in a particular extension
            for link in value:
                print(f"{link}\n")
            print("\n")
        print("<-------------------------------------------------------------------->\n\n")
    print("<--------------------END-------------------->")
