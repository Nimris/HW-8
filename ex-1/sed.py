from mdls import Authors, Quotes
import json
import conn


with open("authors.json", 'r', encoding='utf-8') as file:
    data = json.load(file)
    
    for item in data:
        author = Authors(**item)
        author.save()
    

with open("quotes.json", 'r', encoding='utf-8') as file:
    data = json.load(file)
    
    for item in data:
        author = Authors.objects.get(fullname=item["author"])
        quote = Quotes(tags=item["tags"], author=author, quote=item["quote"])
        quote.save()