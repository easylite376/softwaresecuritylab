- Extension list for random files
- Create randomized string until length of 13 for bruteforce
- predefine locations to look for (/backup /config whatever)

- later: Webcrawler to crawl all links

- docker-container for testing: easylite376/test-apache
  - config.txt in root directory
  - password.txt in backup directory
  - files are at `/usr/local/apache2/htdocs` in container

- TODO:
  - use of the wordlist of bsds svn instead of randomize? -> Randomizing is very slow with permutation. It is broken at the moment
  - extensionlist? Where to find, didn't fine one
  - descide which subfolders we want to look at
  - webcrawler
  - multithread?
  