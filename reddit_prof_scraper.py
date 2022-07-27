import requests
import praw
import time
import subprocess
import pprint
import os

# get API creds
praw_id = os.environ.get("REDDIT_OSINT_PRAW_ID")
praw_secret = os.environ.get("REDDIT_OSINT_PRAW_SECRET")
google_key = os.environ.get("REDDIT_OSINT_GOOGLE_KEY")
browser = os.environ.get("BROWSER")

if None in [praw_id, praw_secret, google_key, browser]:
    print([praw_id, praw_secret, google_key, browser])
    print(
        "API credentials must be set as environment variables. See README for details"
    )
    os._exit(0)

print(
    """
Enter in a profession (ie 'a teacher'). 
This will be turned into a few permutations of the search string 'I am a <profession>', specifically 
    'I work as []'
    'I was []'
    'I'm []'
After entering a profession (with an article), comma separated alternate queries may optionally be added, ie
    'I teach at'
    'My profession is teaching'
The final input should look something like 'a teacher, I teach at, My profession is teaching' or just 'a teacher'"""
)

search_queries = [term.strip() for term in input("profession here> ").split(",")]

profession = search_queries[0]

# The query passed to Google
search_queries[0] = f"I am {profession}"

search_queries.append(f"I was {profession}")
search_queries.append(f"I work as {profession}")
search_queries.append(f"I'm {profession}")
pprint.pprint(f"QUERIES: {search_queries}")

# urlencoding for Google API
q = f"%22{search_queries[0]}%22".replace(" ", "%20")
print(f"SEARCHING {q}")

# TODO: this may cause issues if the 'cx' parameter doesn't carry over between accounts
google_resp = requests.get(
    f"https://www.googleapis.com/customsearch/v1?key={google_key}&cx=5560161f2f92197cc&q={q}"
).json()
if google_resp["error"]:
    print("\nYou have reached the Google API ratelimit")
    print("or you have some other generic Google API error")
    pprint.pprint(google_resp)
    os._exit(0)

print(f"TOTAL RESULTS: {google_resp['queries']['request'][1]['totalResults']}")

links_all = {}
usernames_all = {}

reddit = praw.Reddit(
    client_id=praw_id,
    client_secret=praw_secret,
    user_agent="Reddit profession scraper",
)

print("PRAW INITIALIZED")

# Can only get 10 results from Google API at a time
# in range(9) to get ~100 users total
for iteration_cnt in range(9):
    links = {}

    for item in google_resp["items"]:
        links[(item["link"])] = item["snippet"]

    print(f"LINKS ACQUIRED [round {iteration_cnt+1}]")

    usernames = {}

    for link in links:
        # use url= *or else* 400 error
        print(f"PARSING LINK: {link}")
        sub = reddit.submission(url=link)

        # check if any of search_queries are in the title or text
        # of main post, otherwise check all of the comments
        try:
            if [q for q in search_queries if (q in sub.title)] or [
                q for q in search_queries if (q in sub.selftext)
            ]:
                # has to be iterator
                for most_recent_comment in sub.author.comments.new(limit=1):
                    last_seen = time.time() - most_recent_comment.created_utc
                username = sub.author.name
                print(f"\tFOUND ONE (post): {username} | {last_seen/86400}")
                usernames[username] = last_seen
            else:
                for comment in sub.comments:
                    for q in search_queries:
                        if q in comment.body:
                            username = comment.author.name
                            for most_recent_comment in comment.author.comments.new(
                                limit=1
                            ):
                                last_seen = (
                                    time.time() - most_recent_comment.created_utc
                                )
                            print(
                                f"\tFOUND ONE (comment): {username} | {last_seen/86400}"
                            )

                            usernames[username] = last_seen
        # user is shadowbanned -> exception -> caught and ignored
        except:
            continue

        google_resp = requests.get(
            f"https://www.googleapis.com/customsearch/v1?key={google_key}&cx=5560161f2f92197cc&start={(iteration_cnt+1)*10}&q={q}"
        ).json()
        all_links.update(links)
        all_usernames.update(usernames)
# Data collection complete

# Sort usernames by time last seen (least to most - and scaled from seconds to days)
all_usernames = {
    k: v / 86400 for k, v in sorted(all_usernames.items(), key=lambda item: item[1])
}
pprint.pprint(f"NAMES AND TIMES, SORTED: {names_all}", sort_dicts=False)

# write to file
with open(f"reddit_log_{search_queries[0]}.txt", "w+") as f:
    f.write("NAMES AND TIMES: \n")
    print(all_usernames, file=f)
    f.write("\nLINKS AND SNIPPETS: \n")
    print(all_links, file=f)

print(
    "** Results written to reddit_log_{search_queries[0]}.txt (in current working directory) **"
)

# open top 15 most active user profiles in browser
for u in names.keys()[:-15]:
    subprocess.Popen(f"{browser} 'https://redditmetis.com/user/{u}'", shell=True)
