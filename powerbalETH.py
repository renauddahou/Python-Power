from threading import Thread
from multiprocessing import cpu_count
from time import sleep
import secp256k1 as ice
import json, requests, random
from rich import print
from tqdm import tqdm

j=0
pbar=tqdm(initial=j)

mizogg= '''[red]
              ___            ___  
             (o o)          (o o) 
            (  V  ) MIZOGG (  V  )
            --m-m------------m-m--
[/red]'''
print(mizogg)
available_cores = cpu_count()
print(f"\nNumber of available cores: [purple]{available_cores}[/purple]\n \n[yellow] How many Threads to be used? Try 20 x {available_cores} cores [/yellow]")
threads_count = int(input(f" \n Amount of Threads to use > "))
threads = list()

# Check wallet balance
def check_balance(addr, dec, HEX):
    try:
        contents = requests.get("https://ethbook.guarda.co/api/v2/address/" + addr)
        res = contents.json()
        ress = json.dumps(res)
        resload = json.loads(ress)
        info = str(resload)
        balance = (resload['balance'])
        txs = (resload['txs'])
        addressinfo = (resload['address'])
        #pbar.update(12)
        print('\n[red][*]Dec:[*] [/red][purple] >>' + str(dec) + ' [/purple] ETH Address '+ addressinfo + ' Balance: [blue] [' + str(balance) + '][/blue] txs: [blue][' +  str(txs) + '][/blue]')
        if txs > 0:
            print('[yellow] WOW OMG [/yellow] \n[green][*]Dec:[*] [/green][purple] >>' + str(dec) + ' [/purple] \nETH Address '+ addressinfo + ' Balance: [green] [' + str(balance) + '][/green] txs: [green][' +  str(txs) + '][/green] \n [yellow] WOW OMG [/yellow] ')
            with open("winner.txt", "a") as file:
                file.write('===========================================================================\n')
                file.write(f"DEC Key: {dec} \n HEX Key: {HEX} \nETH Address {addressinfo}  \nBalance [{balance}]  txs [{txs}] \n")
                file.write('===========================================================================\n')
                file.close()
    except TypeError:
        print("Oops! There was some kind of error, don't be afraid, everything is written in errors.txt")
        with open("errors.txt", "a") as errors:
            errors.write(f"Dec: {dec}\nPrivateKey: {HEX}\n")
        sleep(5)
        check_balance(addr, dec, HEX)


# Generate wallet info
def ETH_generate():
    while True:
        dec =int(random.randrange(1, 115792089237316195423570985008687907852837564279074904382605163141518161494336))
        addr = ice.privatekey_to_ETH_address(dec)
        HEX = "%064x" % dec
        check_balance(addr, dec, f"{HEX}")


# Starting script
for _ in range(threads_count):
    thread = Thread(target=ETH_generate)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()