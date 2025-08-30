import diskcache as dc
cache = dc.Cache('tushar-ai-cache')


nuggets = ['Washing Machine', 'Tolstoy', 'Hitchiking']

# STICKING THINGS IN (OR SAVING TO DISK)
for nugget in nuggets:
    print("Calculating key for NAME of the nugget: " + nugget)
    keyName = nugget + "_name"
    keyValue =  nugget
    cache[keyName] = keyValue # Saving the NAME of the nugget

    print("Calculating key for Google Search URL of the nugget: " + nugget)
    keyName = nugget + "_url"
    keyValue = "https://www.google.com/search?q=" + nugget # Saving the Google URL of the nugget
    cache[keyName] = keyValue

    print("Calculating key for text snippet previously returned by Google of nugget: " + nugget)
    keyName = nugget + "_shortBlurb"
    keyValue = "This is the blurb for " + nugget + ". End of the blurb."
    cache[keyName] = keyValue # Saving the summary snippet / blurb for the nugget


# DEMO 1: User input and then lookup in disk cache
nugget = input("DEMO 1 : Enter a nugget: ")
keyName = nugget + "_name"
if keyName in cache:
    print(cache[keyName])
    print(cache[nugget + "_url"])
    print(cache[nugget + "_shortBlurb"])
else:
    print("Nugget not found in cache: " + nugget)
print("END OF DEMO 1 ")

# DEMO 2: Ask cache for ALL ITS KEYS, and prints its values ONE BY ONE. 
print("--- START OF DEMO 2 ")
for key in cache:
    print(key + " --> " + cache[key])
print("--- END OF DEMO 2 ")
