import requests
import re
def image_to_text(image_url):        
    url = f'https://lens.google.com/uploadbyurl?url={image_url}&hl=en'
    print("Request URL:",url)
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'}
    google_lens_api= requests.get(url,headers=headers)
    html = google_lens_api.text
    get_script_tag_pattern = r'<script nonce="[^"]*">(.*?)</script>'
    script_contents = re.findall(get_script_tag_pattern, html, re.DOTALL)
    test_data= " ".join(script_contents)
    pattern = r'\[\[.*?\[(.*?)\]\]\]'
    matches = re.findall(pattern, test_data)

    text_data = ""
    for i in matches:
        if '"en",[[[' in i or '"fr",[[[' in i or 'null,[[["' in i or '"rw",[[[' in i:
            if text_data:
                if len(i) < len(text_data):
                    text_data = i
            else:
                text_data  = i

    text_data = re.findall(r'\b[A-Za-z]+\b', text_data)
    
    remove_common_words_filter = ["null", "www", "com", "google", "http", "https", "jpg", "png", "true", "en",]
    filtered_text_data = [word for word in text_data if len(word) >1 if word not in remove_common_words_filter]

    google_lens_output = " ".join(filtered_text_data)
    return google_lens_output

