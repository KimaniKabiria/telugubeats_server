import os
import json
import collections
from operator import itemgetter
import operator
import re
from additional_utils.spell_corrections import SpellCorrection
import subprocess
import sys
from twisted.spread.util import FilePager




def convermp3To128(file_path):
    """
    mp4f:     mp4 file
    mp3f:     mp3 file
    odir:     output directory
    kbps:     quality in kbps, ex: 320000
    callback: callback() to recieve progress
    efsize:   estimated file size, if there is will callback() with %
    Important:
    communicate() blocks until the child process returns, so the rest of the lines 
    in your loop will only get executed after the child process has finished running. 
    Reading from stderr will block too, unless you read character by character like here.
    """
    
    
    file_path = file_path.lower()
    output_path = "/Users/abhinav/Desktop/"+("/".join(file_path.split("/")[3:]))
                
                
    if not os.path.exists(os.path.dirname(output_path)):                    
        os.makedirs(os.path.dirname(output_path))
        
    

    cmdf = ['/usr/local/bin/ffmpeg', '-i', file_path ] + ("-vn -ar 44100 -ac 2 -ab 128k -f mp3".split(" "))+  [output_path]
    print cmdf
    child = subprocess.Popen(cmdf,stderr=subprocess.PIPE)
    
    while True:
        char = child.stderr.read(1)
        if char == '' and child.poll() != None:
            break
        if char != '':
            # simple print to console
            sys.stdout.write(char)
            sys.stdout.flush()

def clean_folder_names(txt, remove_curve_braces=False):
    if(remove_curve_braces):
        filter_non_ascii = re.compile("[^a-zA-Z0-9 ()]")
        p = re.compile("(\([^)]*\))|(\[[^\]]*\])")
    else:
        filter_non_ascii = re.compile("[^a-zA-Z0-9 ]")
        p = re.compile("(\[[^\]]*\])")#(\([^)]*\))|

    after_tilda = re.compile("~.*$", re.IGNORECASE|re.DOTALL)
    remove_numbers  = re.compile("(^\d+)|(\d+$)")
    remove_vbr_kbps = re.compile("(kbps)|(vbr)", re.IGNORECASE)
    
    
    
    
    
    
    while(True):
        temp = txt
        replace_braces = p.sub("", txt)
        remove_after_tilda = after_tilda.sub("",replace_braces)    
        filter_non_ascii_later  = filter_non_ascii.sub("", remove_after_tilda).strip()
        
        strip_numbers = remove_numbers.sub("", filter_non_ascii_later)
        
        strip_vbr_kbps =remove_vbr_kbps.sub("", strip_numbers)
        if(temp==strip_vbr_kbps):
            break
        
        txt =  strip_vbr_kbps 
    
    return txt
    

def get_all_movie_songs(path= [] , movies = {}):
    dir_path  = "/"+"/".join(path)
    for name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, name)
        if(os.path.isfile(file_path)):
            if(not movies.get(path[-1],None)):                    
                movies[path[-1]] = {"path": path[:] , "songs": [],"images":[]}
                
            file_name, file_extension  = os.path.splitext(file_path)
            file_ext = file_extension.lower()
            songs = movies[path[-1]]["songs"]
            images = movies[path[-1]]["images"]
            if(file_ext==".jpg" or file_ext==".jpeg" or file_ext==".png"):
                images.append(file_name+ file_extension)
                
            if(file_ext==".mp3"):
                file_path = file_name+file_extension      
                #convermp3To128(file_path)
                songs.append(file_name+file_extension)
                
        else:
            get_all_movie_songs(path+[name], movies)
        
        print "read " , dir_path, name 
               
def edit_distance(s1, s2):
    m=len(s1)+1
    n=len(s2)+1

    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

    return tbl[i,j]


def main():
    
    
    ret = {}
    if(os.path.exists(os.getcwd()+"/song_files.txt")):
        movies = json.loads(open("song_files.txt","r").read())
    else:
        movies = {}
        get_all_movie_songs("/Users/abhinav/Desktop/Telugu/".split("/")[1:], movies)
        f = open("song_files.txt","w")
        f.write(json.dumps(movies,indent=4, sort_keys=True))
        f.close()        
        print len(movies)
    
    # match with the raaga crawl
    movies_2 = json.loads(open("song_data.json").read())
    
    '''
    for matches with i in sorted order
    '''
        
    corrections = SpellCorrection()
    for movie_key in movies_2:
        corrections.add_to_correction_index(movie_key.split(" "), movie_key)
    
    for i in movies:#folders
        if(not i or not i.strip()): continue
        print "query :: ",i
        movie_name_key_folder = i
        possible_movies =  corrections.querying(i)
        print possible_movies
        sorted_x = []
        songs_folder = map(lambda x : os.path.splitext(os.path.split(x)[1])[0] , movies[i]["songs"])
        songs_file_names = SpellCorrection()
        for s in songs_folder:
            songs_file_names.add_to_correction_index( s, s)
            
        
        change_score = possible_movies[0][1]
        for raga_movie_key , score in possible_movies[:10]:
#             if(change_score!=score):
#                 continue# pick only higest scorers
#             
#             songs_raga = map(lambda x : x["name"] , movies_2[raga_movie_key]["songs"])
#             songs_map = {}
#             song_score = 1
#             for s in songs_raga:
#                 match = songs_file_names.querying(s)
#                 if(not match): continue
#                 song_score*=(match[0][1])/len(songs_raga)
#                 songs_map[s] = match[0][0]
            movie_name_key_folder = i
            s2 =  clean_folder_names(movie_name_key_folder)
            sorted_x.append((raga_movie_key , edit_distance(raga_movie_key, s2)))# adding weights of songs too
        
        sorted_x  = sorted(sorted_x , key=operator.itemgetter(1))
        print sorted_x
        print "mapping" , sorted_x[0][0] , "to" , movie_name_key_folder
        ret[sorted_x[0][0]] = temp = movies_2[sorted_x[0][0]]
        
        temp["song_entries"] = map(lambda x : (clean_folder_names(os.path.splitext(os.path.split(x)[1])[0], True) , x), movies[i]["songs"])
        
    open("mapped_songs.json","w").write(json.dumps(ret, indent=4))
            
            

        
if __name__ =="__main__":
    #clean_folder_names("Idharammayilatho (2013) 320 Kbps")
    main()
        
        
            
    
        

