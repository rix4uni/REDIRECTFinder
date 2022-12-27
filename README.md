# REDIRECTFinder

A Light Weight Tool for checking Cross Site Scripting (Open Redirect) vulnerabilities by replacing openredirect payloads in the parameters values and checking 'evil.com' in the response.

## Installation
```
git clone https://github.com/rix4uni/REDIRECTFinder.git
cd REDIRECTFinder
#pip3 install -r requirements.txt
```

## Example usages

Note: must use `uro`

Single URL:
```
echo "http://testphp.vulnweb.com/showimage.php?file=./pictures/1.jpg" | python3 redirectfinder.py
```

Multiple URLs:
```
cat redirect-urls.txt | python3 redirectfinder.py
```

## Chaining With Other Tools
```
echo "http://testphp.vulnweb.com" | waybackurls | gf redirect | uro | anew | python3 redirectfinder.py --threads 50
echo "http://testphp.vulnweb.com" | waybackurls | gf redirect | uro | anew redirect-urls.txt # use this output in Multiple URLs
```
## To get best results
```
open redirect_payloads.txt add your favraioute payloads
```

## How It Works
```
For Example Url is:- 
http://testphp.vulnweb.com/showimage.php?file=first&cat=second

It will check all redirectpayloads one by one:-
NOT VULNERABLE: http://testphp.vulnweb.com/showimage.php?file=http:/\/\evil.com&cat=http:/\/\evil.com
VULNERABLE: http://testphp.vulnweb.com/redir.php?r=https:/\evil.com
NOT VULNERABLE: http://testphp.vulnweb.com/showimage.php?file=testphp.vulnweb.com.evil.com&cat=testphp.vulnweb.com.evil.com
```
