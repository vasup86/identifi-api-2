import mysql.connector

from xrpl.clients import JsonRpcClient
from xrpl.models import Payment, Memo
from xrpl.transaction import submit_and_wait
from xrpl.wallet import Wallet
from xrpl.models.amounts import Amount
from xrpl.utils import str_to_hex
from xrpl.core.keypairs import derive_keypair, derive_classic_address

from xrpl.utils import xrp_to_drops

from groth16Proof import verifyMDL
import os
from dotenv import load_dotenv



testnet_url = "https://s.altnet.rippletest.net:51234/"

def sendPayment(sender_username, receiver_username, amount):
    
    load_dotenv()

    pswd = f"{os.getenv('PASSWORD')}"
    user = f"{os.getenv('USER')}"
    url = f"{os.getenv('URL')}"

    # Connect to server
    connection = mysql.connector.connect(
        host=url,
        user=user,
        port=13361,
        password=pswd,
        database="xrpl"
    )
    # timeout = 10
    # connection = pymysql.connect(
    # charset="utf8mb4",
    # connect_timeout=timeout,
    # cursorclass=pymysql.cursors.DictCursor,
    # db="xrpl",
    # 
    # read_timeout=timeout,
    # port=13361,
    # user=f"{os.getenv('DATABASE_PASSWORD')}",
    # write_timeout=timeout,
    # )

    # Get a cursor
    cur = connection.cursor()

    # Execute a query
    cur.execute(f"SELECT * from accounts where UserName = '{receiver_username}'")

    # Fetch one result
    receiver = cur.fetchall()


    # ! Throw error for no user
    # verify the user
    if len(receiver) < 1:
        return "Error"

    cur.execute(f"SELECT * from accounts where UserName = '{sender_username}'")

    # sender and receiver info
    receiver = receiver[0]
    sender = cur.fetchall()[0]

    # close the connection
    connection.close()


    # ! perfrom the zkp

    # Load JSON MDL file
    # with open("mdl.json", "r") as f:
    #     mdlData = json.load(f)

    # verifyMDL(mdlData)

    # if the proof is no, send the error


    # ! store the full proof


    # ! perform the transaction
    client = JsonRpcClient(testnet_url)

    memo_data_hex = str_to_hex(f"Hello Bob received {amount}")
    payment_memo = Memo(
        memo_type=str_to_hex("TestType"),
        memo_format=str_to_hex("text/plain"),
        memo_data=memo_data_hex
    )

    seed = str(sender[3])

    senderWallet = Wallet.from_seed(seed)
    payment_tx = Payment(
        account=senderWallet.address,
        amount=xrp_to_drops(int(amount)),
        destination=str(receiver[2]),
        memos=[payment_memo]
    )
    payment_response = submit_and_wait(payment_tx, client, senderWallet)
    # print("Transaction was submitted")

    # print(payment_response)
    