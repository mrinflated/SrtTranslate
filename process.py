import srt,requests,json,sys,os,time
from urllib.parse import urlencode
from urllib.parse import quote
from tqdm import tqdm

#from google.cloud import translate


APIKey = "AIzaSyAPdRo0-dFQoKPp5GbB6FyVPIspt-ntjKU" #Here is your API key
Url = "https://translation.googleapis.com/language/translate/v2?key="

def translate(queryString,source,target,mode="baidu"):
    if(mode =="baidu"):
        translation = translate_baidu(queryString,source,target)
    elif (mode =="google"):
        translation = translate_google(queryString,source,target)
    
    return translation
 
def translate_google(queryString,source,target):
    requestURL = Url  + APIKey + "&source=" + source + "&target=" + target + "&q=" + queryString  
    response = requests.get(requestURL)
    translation = json.loads(response.text)["data"]["translations"][0]['translatedText']
    return translation

def translate_baidu(query,source,target):
    
    url = "http://crashcourse.club/api/translate/q=%s&from=%s&to=%s"%(quote(query),source,target)
    translated = ""
    response = requests.get(url)
    translated = response.json()["trans_result"][0]["dst"]
    
    return translated


def process(mode,path,source,target):
    fileName = path
    with open(path,'rt',encoding='utf-8',errors='ignore') as f:
        data = f.read()
        f.close()
    
    subs = list(srt.parse(data))

    for k in tqdm(subs):
        text = k.content
        translation = translate(text,source,target,mode)

        k.content = translation
  
    srtTranslated = srt.compose(subs)

    # write the srt file translated...
    with open("%s_%s_Translated.srt"%(os.path.splitext(os.path.split(path)[-1])[0],mode),'xt',encoding='utf-8',errors='ignore') as f:
        f.write(data)
        f.write(srtTranslated)
        f.close()

if __name__ == "__main__":
    process(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])




