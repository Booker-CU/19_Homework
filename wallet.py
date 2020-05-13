from constants import *
from web3 import Web3, middleware, Account
from bit import PrivateKeyTestnet, wif_to_key
from bit.network import NetworkAPI
import subprocess
import json


from web3.middleware import geth_poa_middleware

#w3.middleware_onion.inject(geth_poa_middleware, layer=0)

w3 = Web3(Web3.HTTPProvider("IP address"))

def derive_wallets(MNEMONIC,coins):
    
    command = f'./derive -g --mnemonic="{MNEMONIC}" --cols=path,address,privkey,pubkey,pubkeyhash,xprv,xpub --coin="{coins}" --numderive=3 --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    
    p_status = p.wait()
    
    keys = json.loads(output)
    return(keys)


def priv_key_to_account(coin,privkey):
    
    if coin == ETH:
        
        account = Account.privateKeyToAccount(privkey)
        
        return account
    
    elif coin == BTCTEST:
        
        account = PrivateKeyTestnet(privkey)
        
        return account
    
    else:
        print("Error with function")
    

def create_tx(coin,account,to,amount):
        
        if coin == ETH:
            
            gasEstimate = w3.eth.estimateGas(
                {"from": account.address, "to": to, "value": amount}
            )
            return {
                "from": account.address,
                "to": to,
                "value": amount,
                "gasPrice": w3.eth.gasPrice,
                "gas": gasEstimate,
                "nonce": w3.eth.getTransactionCount(account.address),
                #"chain ID": w3.eth.chainId
            }

        
        elif coin == BTCTEST: 
            tx_data = PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
            return tx_data
        
        else:
            print("Error with function")
        
        
def send_tx(coin,account,to,amount):
        
        if coin == ETH:
            raw_tx = create_tx(coin,account,to,amount)
            signed_tx = account.sign_transaction(raw_tx)
            result_eth = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            #print(result_eth.hex())
            return result_eth.hex()
        
        elif coin == BTCTEST:
            
            raw_tx = create_tx(coin,account,to,amount)
            #print(raw_tx)
            signed_tx = account.sign_transaction(raw_tx)
            #print(signed_tx)
            result_btctest = NetworkAPI.broadcast_tx_testnet(signed_tx)
            print(result_btctest)
            return result_btctest
        
        else:
            print("Error with function")



        
