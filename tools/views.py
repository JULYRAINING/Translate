from _datetime import datetime
import hashlib
import json  
import random
import urllib

from django.http.response import HttpResponse
from django.shortcuts import render
from pymongo.mongo_client import MongoClient


#main page
def index(request):
    return render(request, 'tools/translate.html')

#main page
def index_long(request):
    return render(request, 'tools/translate_baidu.html')



def translate(request, material):
    print(material)
    appid = '20161204000033373'
    secretKey = 'qjpLG2Qms0wdrWDML9Pl'
    
    q = material
    fromLang = 'auto'
    toLang = 'zh'
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = random.uniform(32768, 65536)
    
    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    
    values = {
        'appid':appid,
        'q':urllib.parse.quote(q),
        'from':fromLang,
        'to':toLang,
        'salt':salt,
        'sign':sign
        }
    
    result = ''
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    try:
        data = urllib.parse.urlencode(values)
        response = urllib.request.urlopen(myurl)
        
        result = response.read().decode('unicode_escape')
        print('result:', end = '')
        print(result)
    except Exception as e:
        print('error:', end = '')
        print(e)
   
        

    
    
     
    return HttpResponse(json.dumps(result), content_type="application/json")  


def saveRecord(request):
    
    if request.method == 'GET':
        datastr_list = request.GET.getlist('material')
        print(request.body)
        datastr = datastr_list[0]
        print(datastr)
        dataobj = json.loads(datastr)
        
        
        dataobj['time'] = datetime.utcnow()
        #print(dataobj)
        #save to mongo
        client = MongoClient("localhost", 27017)
        db = client.translate
        collection = db.volcabulary
        collection.insert(dataobj)
        print('saved')
        return HttpResponse(json.dumps('("a":"success")'), content_type="application/json")  
    '''
        for key in request.GET:
            print(key)
            valuelist = request.GET.getlist(key)
            print(valuelist)
    
        
    
    else:
        for key in request.POST:
            print(key)
            valuelist = request.POST.getlist(key)
            print(valuelist)
            
    '''   
    
    return HttpResponse(json.dumps('("a":"failed")'), content_type="application/json")  
    