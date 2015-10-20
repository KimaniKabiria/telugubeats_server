


def c(id=None, viewType="LinearLayout"):
    return {"type":"c", "id": id , "viewType":viewType}

def h(*args):
    id = None
    if(args and isinstance(args[0] , basestring)):
        id = args[0]
        args = args[1:]        
    return {"type":"h" , "children":args, "id":id} 


def v(*args):
    id = None
    if(args and isinstance(args[0] , basestring)):
        id = args[0]
        args = args[1:]
        
    return {"type":"v" , "children":args, "id":id }

 
def l(*args):
    id = None
    if(args and isinstance(args[0] , basestring)):
        id = args[0]
        args = args[1:]
        
    return {"type":"l" , "children":args, "id":id }

def s(*args):
    id = None
    if(args and isinstance(args[0] , basestring)):
        id = args[0]
        args = args[1:]
        
    return {"type":"s" , "children":args, "id":id }



def underscore_to_camelcase(value):
    def camelcase(): 
        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(c.next()(x) if x else '_' for x in value.split("_"))

def get_android_id(id):    
    return 'android:id="@+id/'+id+'"' if id else ""

def parse(layout, parent_type=None, ui_handle=[]):
    
    if(layout==None):
        return

    children = layout.get("children",None)
    type = layout["type"]
    id = layout.get("id", "none")
    viewType = layout.get("viewType",None)
    if(type=="l"):
        if(id):
            ui_handle.append([("FrameLayout "+underscore_to_camelcase(id) , 
                               'uiHandle.'+underscore_to_camelcase(id) +' = (FrameLayout)layout.findViewById(R.id.'+id+')')])
        return '''<FrameLayout
        '''+get_android_id(id)+'''
    android:layout_width="match_parent"
    android:layout_height="wrap_content">
    '''+"\n".join(map(lambda x: parse(x, ui_handle=ui_handle) ,  children)) +'''
    </FrameLayout>
    '''
    if(type=="c"):
        if(id):
            ui_handle.append((viewType+" "+underscore_to_camelcase(id) , 
                               'uiHandle.'+underscore_to_camelcase(id) +' = ('+viewType+')layout.findViewById(R.id.'+id+')'))
        
        return '''<'''+viewType+'''
       '''+get_android_id(id)+'''
        android:layout_width="match_parent"
        '''+('android:orientation="vertical"' if viewType=="LinearLayout" else "" )+'''
        android:layout_height="wrap_content"/>'''
    
    if(type=='v'):
        if(id):
            ui_handle.append(("LinearLayout "+underscore_to_camelcase(id) , 
                               'uiHandle.'+underscore_to_camelcase(id) +' = (LinearLayout)layout.findViewById(R.id.'+id+')'))
      
        return '''<LinearLayout 
    android:orientation="vertical"
    '''+get_android_id(id)+'''
    android:layout_width="match_parent"
    android:layout_height="wrap_content">
    '''+("\n".join(map(lambda x: parse(x, 'v' ,ui_handle=ui_handle) , children ))) +'''
    </LinearLayout>
    '''
    
    if(type=='h'):
        if(id):
            ui_handle.append(("LinearLayout "+underscore_to_camelcase(id) , 
                               'uiHandle.'+underscore_to_camelcase(id) +' = (LinearLayout)layout.findViewById(R.id.'+id+')'))

        return '''<LinearLayout 
    android:orientation="horizontal"
    '''+get_android_id(id)+'''
    android:layout_width="match_parent"
    android:layout_height="wrap_content">
    '''+"\n".join(map(lambda x: parse(x, 'h' , ui_handle=ui_handle) ,  children)) +'''
    </LinearLayout>
    '''
    
    if(type=='s'):
        if(id):
            ui_handle.append(("ScrollView "+underscore_to_camelcase(id) , 
                               'uiHandle.'+underscore_to_camelcase(id) +' = (ScrollView)layout.findViewById(R.id.'+id+')'))

        return '''<ScrollView 
    '''+get_android_id(id)+'''
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    '''+"\n".join(map(lambda x: parse(x, 'h' , ui_handle=ui_handle) ,  children)) +'''
    </ScrollView>
    '''


def print_java_code(layout):
        
        
        ui_handle = []
        
        print '''<?xml version="1.0" encoding="utf-8"?>'''
        l= parse (layout, ui_handle=ui_handle).split("\n")
        print l[0]+ ''' xmlns:android="http://schemas.android.com/apk/res/android"'''
        print "\n".join(l[1:])
        print '''public static class UiHandle{
        '''
        for i, j  in ui_handle:
            print i+";"
        
        print '''
        }'''
            
        print '''
         UiHandle uiHandle = new UiHandle();
         
        public UiHandle initUiHandle(ViewGroup layout){
        '''
        
        for i, j  in ui_handle:
            print j+";"
        print '''
        return uiHandle;
        }'''
            

#h - horizontal
#v - vertical
#c - id , layout type
#s - scrollView vertical
#l - layered stack over one another

print_java_code(h(
                  c('image', 'ImageView') , v(c('user_name','TextView'),
                                              c('user_message','TextView')
                                            ),
                  
                  )
                )


# (v(
#                 h(c("poll_image","ImageView"), v(
#                                 h(c("poll_title","TextView"), c("voted", "TextView")),
#                                 h(c("poll_subtitle","TextView") ,  c("poll_subtitle2", "TextView")),
#                                 c("poll_subtitle3","TextView")
#                                 )
#                         ),
#                         h(c("poll_percentage"),
#                                 c("poll_count","TextView")
#                         )
#                 ))

# (v(c("live_polls_heading","TextView"),
#                 c("live_polls_list","ListView")
#                 ))


#(                 v(s(
#                   v(
#                                 c("song_and_title","TextView"),
#                                 c("scrolling_dedications"),
#                                 h(c(None, "TextView"), c("music_directors", "TextView")),
#                                 h(c(None, "TextView"), c("actors", "TextView")),
#                                 h(c(None,"TextView"), c("directors", "TextView")),
#                                 h(c(None,"TextView"), c("singers", "TextView")),
#                                 c(None),
#                                 h(c("live_users","TextView"), c("whats_app_dedicate")),
#                                 c("visualizer"),
#                                 c("playing_image", "ImageView")
#                         )
#                     )
#               ))


                
        
            
            