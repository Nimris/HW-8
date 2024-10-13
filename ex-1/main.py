from mdls import Authors, Quotes
import conn
import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def get_quotes_name(value):
    print("Function called")
    author = Authors.objects.get(fullname__istartswith=value.strip())
    quotes = Quotes.objects(author=author)
    if not quotes:
        return('No quotes found')
    return "\n".join(quote.quote for quote in quotes)
    
    
@cache
def get_quotes_tag(value):
    print("Function called")
    quotes = Quotes.objects(tags__istartswith=value.strip().lower())
    if not quotes:
        return('No quotes found')
    return "\n".join(quote.quote for quote in quotes)
    
    
def get_quotes_tags(value):
    tags = [tag.strip().lower() for tag in value.split(',')]
    quotes = Quotes.objects(tags__in=tags)
    if not quotes:
        return('No quotes found')
    return "\n".join(quote.quote for quote in quotes)


if __name__ == '__main__':
    while True:
        input_data = input("Enter command: ")
        command, value = input_data.split(':')
        
        if command == 'name':
            print(get_quotes_name(value))
                
        elif command == 'tag':
            print(get_quotes_tag(value))
            
        elif command == 'tags':
            print(get_quotes_tags(value))
                
        elif command == 'exit':
            break
            
        else:
            print("Invalid command")