import re
import time
from collections import namedtuple
import operator
import json
import collections


    
    
IndexEntry = namedtuple('IndexEntry', ['corrections', 'words'])
    
class SpellCorrection():
    SPELL_CORRECTION_INDEXING_SIZE = 4
    index = {}
    filter_non_ascii = re.compile("[^a-zA-Z0-9 ]")
    '''
    when the query matches any of the list of words , it returns this ret_val
    '''
    def __init__(self):
        self.index = {}
    
    def add_map_to_index_bulk(self, d):
        m = 0
        for word in d:
            l = len(word)       
            for sz in range(min(l-2 ,3) , self.SPELL_CORRECTION_INDEXING_SIZE+1):
                _letters = set()
                for i in range(l):
                    for j in range(i+1,min(i+4,l-sz+1)+1):
                        temp = word[i]+word[j:j+sz-1]
                        
                        if(temp in _letters):
                            continue
                            
                        _letters.add(temp)
                                                
                        arr = None
                        if(True or len(temp)>2 or j-i<3):
                            if(not self.index.get(temp,None)):
                                arr = set()
                                self.index[temp] = IndexEntry(arr, None)
                            else:
                                arr = self.index[temp].corrections
                            ##considers first letter to be utmost priority
                            # multiplied by inverted shape forming distance 
                            # number can be tweaked
                            wgt = len(temp)*int (4.0/((j-i)*(i+1)))
                            arr.add(word+"_"+str(wgt)+"_"+ str(l))
                            
                            if(len(arr)>m and len(temp)!=2):
                                m  = len(arr)
                                w = temp
            
        total = 0    
        for i in self.index:
            total+=len(self.index[i].corrections)
            

        print "total entries: " , (total)
        print "max in set: "+str(m)
        print "max combination letters: ",w
        index_total_size = len(self.index)
        print "letter_set_size:" , str(index_total_size)

    def add_to_correction_index(self, list_of_words , ret_val=None):
        if(isinstance(list_of_words, basestring)):
            list_of_words = list_of_words.split(" ")
            
        list_of_words = map(lambda x : x.lower() , list_of_words)
        m = 0
        append_to_index = {}
            
        for tag in list_of_words:
            tag = self.filter_non_ascii.sub("",tag)
            l = len(tag)       
            for sz in range(min(3 , l-2) ,self.SPELL_CORRECTION_INDEXING_SIZE+1):
                _letters = set()
                for i in range(l):
                    for j in range(i+1,min(i+4,l-sz+1)+1):
                        temp = tag[i]+tag[j:j+sz-1]
                        
                        if(temp in _letters):
                            continue
                            
                        _letters.add(temp)
                                                
                        arr = None
                        if(True or len(temp)>2 or j-i<3):# indexing all , if true is removed it will index only length >2 and distance < 3
                            if(not append_to_index.get(temp,None)):
                                append_to_index[temp] = arr = set()
                            else:
                                arr = append_to_index[temp]
                            ##considers first letter to be utmost priority
                            # multiplied by inverted shape forming distance 
                            # number can be tweaked
                            wgt = int (16.0/((j-i)*(i+1)))
                            
                            
                            arr.add( ret_val+"_"+str(wgt)+"_"+ str(l))
                            
                            if(len(arr)>m and len(temp)!=2):
                                m  = len(arr)
                                w = temp
    
        #print "Read entities"," {:0>8}".format(datetime.timedelta(seconds=time.time() - start_time))
        for key in append_to_index:
            existing_index = self.index.get(key, None)
            if(not existing_index):
                self.index[key] = IndexEntry(append_to_index[key], None)
            else:
                should_insert  = False
                for expr_props in append_to_index[key]:
                    if(not expr_props in existing_index.corrections):
                        should_insert = True
                        existing_index.corrections.add(expr_props)
                        
#                 for word in append_to_index[key][1]:
#                     if(not word in existing_index.words):
#                         should_insert = True
#                         existing_index.words.append(word)
                
            #print SpellCorrectionIndex1.insert(key , map(lambda x : x.strip() , index[key][0]), map(lambda x : x.strip() , index[key][1]))
        #print items
        #print "inserted updated entities"," {:0>8}".format(datetime.timedelta(seconds=time.time() - start_time))
    
    
    
    def querying(self, query=None):
        empty = ([],[])
        queries  = 0
        h = {}
        entity_weights = {}  
        query = self.filter_non_ascii.sub("",query)
            
        query_words = map( lambda x : x.lower() ,query.split(" "))
        for q in query_words:
            l = len(q)
            is_seen_queries = {}
            for sz in range(min(3 , l-2), self.SPELL_CORRECTION_INDEXING_SIZE+1):
                hs = {}
                for i in range(l):
                    for j in range(i+1,min(i+4,l-sz+1)+1):
                        queries+=1
                        temp = q[i]+q[j:j+sz-1]
                        if(is_seen_queries.get(temp, None) or len(temp)<2):
                            continue
                        is_seen_queries[temp] = True
                        ent = self.index.get(temp , None)
                        for k in ent.corrections if ent else [ ]:                            
                            temp3 = k.split("_")
                            idx = temp3[0]
                            weight , le = temp3[-2:]
                            
                            weight = 1+(int(weight)) * len(temp)/((j-i)*(i+1))* 4.0/(1 +abs(int(le)-l))
                            if(entity_weights.get(idx,None) and not hs.get(idx+"_"+temp,None)):
                                entity_weights[idx]+= weight
                            else:
                                entity_weights[idx] = weight
                                hs[idx+"_"+temp]=True                       
        
        sorted_x = sorted(entity_weights.items(), key=operator.itemgetter(1))
        sorted_x.reverse()
        count = 0   
        ret_vals = []
        if(sorted_x):
            for k in sorted_x:
                if(count>10):
                    break
                count+=1
#                 if(change!=k[1]):
#                     change = k[1]
#                     changed_times+=1
#                     if(changed_times>10):
#                         break
                ret_vals.append(k)         
                 
#                                 
        return ret_vals
    
    def sentences(self, l_l , index=0 ):
        if(index>=len(l_l)):
            return [""]
        ret = []
        for i in l_l[index]:
            for s in self.sentences(l_l, index+1):
                ret.append(i+" "+s)
        
        return ret

    
def main():
    pass


def test(tests):
    def words(text): return re.findall('[a-z]+', text.lower()) 
    
    
    
    corrector = SpellCorrection()
    l = words(file('big.txt').read())

    def train(features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model
    NWORDS = train(l)
    start = time.clock()
    print len(l)
    corrector.add_map_to_index_bulk(l)
    print int(time.clock()-start), "sec to build index"
    def spelltest(tests, bias=None, verbose=False):
        import time
        n, bad, unknown = 0, 0, 0
        for target,wrongs in tests.items():
            for wrong in wrongs.split():
                n += 1
                w , weight= corrector.querying(wrong)
                print w , wrong
                if w!=target:
                    bad += 1
                    unknown += (target not in NWORDS)
                    if verbose:
                        print 'correct(%r) => %r (%d); expected %r (%d)' % (
                            wrong, w, NWORDS[w], target, NWORDS[target])
        return dict(bad=bad, n=n, bias=bias, pct=int(100. - 100.*bad/n), 
                    unknown=unknown, secs=int(time.clock()-start) )
    
    print spelltest(tests)
