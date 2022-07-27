# Reddit Profession Scraper
This takes a profession (ie 'teacher') and returns a list of usernames, sorted by last_seen (most recent to least). It also gives context in which the user identified as such (ie 'I am a teacher and I don't know what do do about these students) and opens the top 15 users' profiles in [redditmetis](https://redditmetis.com), a profiler. The intended use is to connect with some people of a certain profession by DMing them and chatting. Would recommend not misusing this but it's your accounts that will be blocked so do as you wish.

Also, any query string (or array of strings) can be used instead of just "I am a <profession>" (ie "I enjoy biking"). You can alter the source yourself to get that functionality.

## Quickstart
### Creating API keys and Setting Environment Variables
This is a pain. But necessary. Should take around 5 minutes to set up.

#### Reddit (2 mins)
Sign into a Reddit account, and go to https://www.reddit.com/prefs/apps
Click `create another app`, fill out the name, set the type as script, add http://locahost:8080 as the redirect uri. `export REDDIT_OSINT_PRAW_SECRET=<secret>` and `export REDDIT_OSINT_PRAW_ID=<client-id>`. The ID is the string under "personal use script", and don't add spaces when exporting variables.

#### Google (2 mins)
Sign into your Google account, then go to https://developers.google.com/custom-search/v1/overview and find a blue box proclaiming "Get a Key". Create a project with a random name and copy the API key provided in the following popup window. `export REDDIT_OSINT_GOOGLE_KEY=<key>`

#### Browser (15 secs)
Many Linux distributions set an environment variable named $BROWSER to identify the default browser. If it isn't set already, add it to your `~/.bashrc` or `~/.zshrc` (same deal, add a line with `export BROWSER=<name of your browser binary eg 'chromium'>`) and save, then `source ~/.bashrc`

Checklist:
- Reddit API secret (`$REDDIT_OSINT_PRAW_SECRET`)
- Reddit Client ID (`$REDDIT_OSINT_PRAW_ID`)
- Google API key (`$REDDIT_OSINT_GOOGLE_KEY`)
- Default browser set (`$BROWSER`)
You need a Reddit API key and Client ID, and a Google API key

### Dependencies
There is a single non-std dependency: PRAW (reddit API bindings)

`pip3 install praw`

### Usage
```bash
python3 reddit_prof_scraper.py
```
Output of that will be

```
Enter in a profession (ie 'a teacher'). 
This will be turned into a few permutations of the 
search string 'I am a <profession>', specifically 
    'I work as []'
    'I was []'
    'I'm []'
After entering a profession (with an article), 
comma separated alternate queries may optionally be added, ie
    'I teach at'
    'My profession is teaching'
The final input should look something like 'a teacher, 
I teach at, My profession is teaching' or just 'a teacher'

profession here>
```
Once a profession is specified, the program will run, logs will be outputted throughout runtime, and all collected information will be saved to a log file when completed.
