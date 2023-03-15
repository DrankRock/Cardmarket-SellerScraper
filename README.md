# Cardmarket-SellerScraper
Scrape the content of a seller's page and export to a csv file

## Install
```console
$ git clone https://github.com/DrankRock/Cardmarket-SellerScraper.git
$ cd Cardmarket-SellerScraper
$ python -m pip install -r requirements.txt
```

## Use :
```console
$ python cmss.py -h
usage: cmss.py [-h] -u URL -o OUTPUT

Scrape the items sold by a seller on Cardmarket

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     url to a seller page containing items, such as the single page
  -o OUTPUT, --output OUTPUT
                        path to the csv file used as output
```
`python cmss.py -u https://www.cardmarket.com/en/YuGiOh/Users/TCGATZENJENS/Offers/Singles?idExpansion=1653 -o output.csv`    
(I used this because it's a top seller on Cardmarket)

## Output :
Note : When opening the csv, you have to use `,` as delimiter and `"` as string delimiter.      
![image](https://user-images.githubusercontent.com/32172257/225280387-5f5b326d-bcf0-4f94-829a-2bb8a67b4a75.png)
