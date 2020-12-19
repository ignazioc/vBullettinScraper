Python script to fetch all the links posted in a vbullettin forum board. Because life is too short manually check your forum every day.

### Usage

```
http_client = VbullettinFetcher("https://example.com/", "username", "password")
http_client.doLogin()
base_page = http_client.get('https://example.com/forum/my_interesting_section/')
threads = http_client.extractThreads(base_page)
links = http_client.extractAllLinksFromThreads(threads)


# print the response:
for item in links:
    print(item["title"])
    print(item["url"])
    for l in item["links"]:
        print("  " + l)
    print()
```


