from threading import Thread
from multiprocessing import cpu_count
from time import sleep
import secp256k1 as ice
import json, requests, random
from rich import print

mizogg= '''[red]
              ___            ___  
             (o o)          (o o) 
            (  V  ) MIZOGG (  V  )
            --m-m------------m-m--
[/red]'''
print(mizogg)
available_cores = cpu_count()
print(f"\n[purple]Welcome to powerbal.py RANDOM :[/purple] [blue](edit line 54 to change range)[/blue] \n \n[yellow]How many Threads to be used? Dont use to many API block \n \nTry [/yellow][purple]{available_cores}[/purple][yellow] or [/yellow][purple]{2*available_cores}[/purple][yellow] or [/yellow][purple]{3*available_cores}[/purple][yellow] Threads? [/yellow]")
threads_count = int(input(f" \nAmount of Threads to use > "))
threads = list()

# Check wallet balance
def check_balance(addr, dec, HEX):
    try:
        contents = requests.get("https://btcbook.guarda.co/api/v2/address/" + addr)
        res = contents.json()
        ress = json.dumps(res)
        resload = json.loads(ress)
        info = str(resload)
        balance = (resload['balance'])
        totalReceived = (resload['totalReceived'])
        txs = (resload['txs'])
        addressinfo = (resload['address'])
        print('[red][*]Dec :[*][/red][purple] >> ' + str(dec)[1:10] + '.... [/purple] BTC Address '+ addressinfo + ' Balance: [blue] [' + str(balance) + '][/blue] totalReceived: [blue][' +  str(totalReceived) + '][/blue] txs:[blue][' + str(txs) + '][/blue]', end='\r')
        if txs > 0:
            wifc = ice.btc_pvk_to_wif(HEX)
            wifu = ice.btc_pvk_to_wif(HEX, False)
            print('[yellow] WOW OMG [/yellow] \n[green][*]Dec:[*] [/green][purple] >>' + str(dec) + ' [/purple] \nBTC Address '+ addressinfo + ' Balance: [green] [' + str(balance) + '][/green] totalReceived: [green][' +  str(totalReceived) + '][/green] txs:[green][' + str(txs) + '][/green] \n [yellow] WOW OMG [/yellow] ')
            with open("winner.txt", "a") as file:
                file.write('===========================================================================\n')
                file.write(f"DEC Key: {dec} \n HEX Key: {HEX} \nBTC Address {addressinfo}  \nBalance [{balance}]  TotalReceived [{totalReceived}] TXS [{txs}] \nWIF Compressed: {wifc} \nWIF Uncompressed: {wifu} \n")
                file.write('===========================================================================\n')
                file.close()
    except TypeError:
        print("Oops! There was some kind of error, don't be afraid, everything is written in errors.txt")
        with open("errors.txt", "a") as errors:
            errors.write(f"Dec: {dec}\nPrivateKey: {HEX}\n")
        sleep(5)
        check_balance(caddr, dec, HEX)
        check_balance(uaddr, dec, HEX)


# Generate wallet info
def BTC_generate():
    while True:
        dec =int(random.randrange(1, 115792089237316195423570985008687907852837564279074904382605163141518161494336))
        uaddr = ice.privatekey_to_address(0, False, dec)
        caddr = ice.privatekey_to_address(0, True, dec)

        HEX = "%064x" % dec
        check_balance(caddr, dec, f"{HEX}")
        check_balance(uaddr, dec, f"{HEX}")


# Starting script
for _ in range(threads_count):
    thread = Thread(target=BTC_generate)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()