import time
from tqdm import tqdm
print("Cardmarket Seller Scraper for user XXX :")
pbar1 = tqdm(total=100, position=1)
pbar2 = tqdm(total=200, position=0)

for i in range(10):
    pbar1.update(10)
    pbar2.update(20)
    time.sleep(1)