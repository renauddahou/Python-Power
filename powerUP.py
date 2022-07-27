import secp256k1 as ice
from rich import print
from time import sleep, time
import os
import threading
import json, requests, random
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

Mizogg = '''[red]
                ╔═╗╔═╗                   
                ║║╚╝║║                   
                ║╔╗╔╗║╔╗╔═══╗╔══╗╔══╗╔══╗
                ║║║║║║╠╣╠══║║║╔╗║║╔╗║║╔╗║
                ║║║║║║║║║║══╣║╚╝║║╚╝║║╚╝║
                ╚╝╚╝╚╝╚╝╚═══╝╚══╝╚═╗║╚═╗║
                                 ╔═╝║╔═╝║
                                 ╚══╝╚══╝
                  ___            ___  
                 (o o)          (o o) 
                (  V  ) MIZOGG (  V  )
                --m-m------------m-m--
[/red]'''

if os.path.exists(os.getcwd()+"/save_scan.txt") == False:
    open("save_scan.txt", "w+")

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
        wifc = ice.btc_pvk_to_wif(HEX)
        wifu = ice.btc_pvk_to_wif(HEX, False)
        #pbar.update(12)
        print('[red][*]Dec:[*] [/red][purple] >>' + str(dec) + ' [/purple] \nBTC Address '+ addressinfo + ' Balance: [blue] [' + str(balance) + '][/blue] totalReceived: [blue][' +  str(totalReceived) + '][/blue] txs:[blue][' + str(txs) + '][/blue]')
        #print('\nBTC Address [purple]'+ addressinfo + '[/purple] Balance: [blue] [' + str(balance) + '][/blue] totalReceived: [blue][' +  str(totalReceived) + '][/blue] txs:[blue][' + str(txs) + '][/blue]')
        if txs > 0:
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
        
class POWER():
    def __init__(work):
        work.start_time = 0
        work.prev_n = 0
        work.cur_n = 0
        work.start_n = 0
        work.end_n = 0
        work.seq = False
        work.start_r = 0

    def speed(work):
        while True:
            if work.cur_n != 0:
                cur_t = time()
                n = work.cur_n
                if work.prev_n == 0:
                    work.prev_n = n
                elapsed_t=cur_t-work.start_time
                print("Current : "+str(n)+", Current rate Per/CPU : "+str(abs(n-work.prev_n)//2)+"/s"+f", Time Elapsed: [{str(elapsed_t//3600)[:-2]}:{str(elapsed_t//60%60)[:-2]}:{int(elapsed_t%60)}], Total Scanned Per/CPU : {n-work.start_r} ", end="\r")
                work.prev_n = n
                if work.seq:
                    open("save_scan.txt","w").write(f"{work.cur_n}-{work.start_r}-{work.end_n}")
            sleep(2)
        
    def random_scan(work, n):
        work.cur_n=n
        dec =int(random.randrange(1, 115792089237316195423570985008687907852837564279074904382605163141518161494336))
        uaddr = ice.privatekey_to_address(0, False, dec)
        caddr = ice.privatekey_to_address(0, True, dec)
        HEX = "%064x" % dec
        check_balance(caddr, dec, f"{HEX}")
        check_balance(uaddr, dec, f"{HEX}")

            
    def sequential_scan(work, n):
        work.cur_n=n
        dec = int(n)
        uaddr = ice.privatekey_to_address(0, False, dec)
        caddr = ice.privatekey_to_address(0, True, dec)
        HEX = "%064x" % dec
        check_balance(caddr, dec, f"{HEX}")
        check_balance(uaddr, dec, f"{HEX}")
    
    def num_of_cores(work):
        available_cores = cpu_count()
        print(f"\nNumber of available cores: [purple]{available_cores}[/purple]\n \nHow many cores to be used? [yellow](leave empty to use all available cores)[/yellow]")
        cores = input(f" \n Amount of CPU Cores to use > ")
        if cores == "":
            work.cores = int(available_cores)
        elif cores.isdigit():
            cores = int(cores)
            if 0 < cores <= available_cores:
                work.cores = cores
            elif cores<=0 :
                print(f"Not Possible to use {cores} number of cpu cores!!")
                input("[red]Press Enter to exit[/red]")
                raise ValueError("negative number!")
            elif cores > available_cores:
                print(f"\n You only have {available_cores} cores")
                print(f" Are you sure you want to use {cores} cores?")
                core_input = input("\n[y]es or [n]o>")
                if core_input == "y":
                    work.cores = cores
                else:
                    print("using available number of cores")
                    work.cores = available_cores
        else:
            print("Wrong input!")
            input("Press Enter to exit")
            exit()
            
            
    def get_user_input(work):
        print (Mizogg)
        print ("[green]\n 1 for Random Scan [/green]\n [blue]2 for Sequential Scan [/blue]")
        method_input = input("\n : Type 1-2 to begin :")
        if method_input=="1":
            target = work.random_scan
        elif method_input=="2":
            if open("save_scan.txt", "r").read() != "":
                resume=open("save_scan.txt").read().split("-")
                print(f"[purple] Resuming  Sequential Scan Range [/purple] {resume[0]}-{resume[2]}")
                with ThreadPoolExecutor(max_workers=work.num_of_cores()) as pool:
                    print("\n Resuming ...\n")
                    work.start_time = time()
                    work.start_r = int(resume[1])
                    work.start_n = int(resume[0])
                    work.end_n = int(resume[2])
                    work.seq=True
                    for i in range(work.start_n,work.end_n):
                        pool.submit(work.sequential_scan, i)
                    print("Stopping\n")
                    exit()
            else:
                range0 = input("\n Enter range \n (example:1-115792089237316195423570985008687907852837564279074904382605163141518161494336) \n> ")
                resume = range0.split("-")
                resume.insert(1,resume[0])
                open("save_scan.txt", "w").write("-".join(resume))
                with ThreadPoolExecutor(max_workers=work.num_of_cores()) as pool:
                    print("\n Starting ...")
                    work.start_time = time()
                    work.start_r = int(resume[1])
                    work.start_n = int(resume[0])
                    work.end_n = int(resume[2])
                    work.seq=True
                    for i in range(work.start_n,work.end_n):
                        pool.submit(work.sequential_scan, i)
                    print("Stopping\n")
                    exit()
        else:
            print("exitting...")
            exit()

        with ThreadPoolExecutor(max_workers=work.num_of_cores()) as pool:
            r = range(100000000000000000)
            print("\n Starting ...")
            work.start_time = time()
            work.start_n = 0
            for i in r:
                pool.submit(target, i)
            print("Stopping\n")
            exit()



if __name__ =="__main__":
        obj = POWER()
        try:
            t0 = threading.Thread(target=obj.get_user_input)
            t1 = threading.Thread(target=obj.speed)
            t1.daemon = True
            t0.daemon = True
            t0.start()
            t1.start()
            sleep(4000000)
            sleep(4000000)
        except KeyboardInterrupt:
            print("\n\nCtrl+C pressed. \nexitting...")
            exit()
        else:
            print(f"\n\nError: {Exception.args}\n")
            exit()