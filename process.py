import srt,requests,json,sys
from google.cloud import translate


APIKey = "" #Here is your API key
Url = "https://translation.googleapis.com/language/translate/v2?key="

def translate(queryString,source,target):
    requestURL = Url  + APIKey + "&source=" + source + "&target=" + target + "&q=" + queryString  
    response = requests.get(requestURL)
    translation = json.loads(response.text)["data"]["translations"][0]['translatedText']
    return translation





def process(path,source,target):
    with open(path,'rt',encoding='utf-8',errors='ignore') as f:
        data = f.read()
        f.close()
    
    subs = list(srt.parse(data))

    for k in subs:
        text = k.content
        translation = translate(text,'en','zh-CN')

        k.content = translation
        sys.stdout.write("Line [%d/%d] completed!\r"%(k.index,len(subs)))
        sys.stdout.flush()
        #print("Line[%d/%d]:",k.index,"completed!")
    srtTranslated = srt.compose(subs)

    # write the srt file translated...
    with open("Translated.srt",'xt') as f:
        f.write(srtTranslated)
        f.write(data)
        f.close()

if __name__ == "__main__":
    process(sys.argv[1],sys.argv[2],sys.argv[3])




