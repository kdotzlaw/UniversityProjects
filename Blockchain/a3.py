
import hashlib
import json
from socket import *
import sys
import random
from json import JSONDecodeError
import uuid
import time
import traceback

# ----GLOBALS----
DIFFICULTY = 8
chain = []  # to hold the POW majority blockchain
stats = {}  # dict of kvps (height,hash):[peer1,peer2...]
peers = {}  # list of all connected peers
msgids = []  # track message ids so we dont repeat msgs
built = False  # false if we dont have chain built, true if we do
blocks = {}  # list of blocks waiting to be added
statsPeers = []  # has all peers that replied with pow majority blockchain
sameHeight = []  # for tracking if we queried all peers for specific block at height
exclude = []  # stores stats record of a determined invalid chain
chainHeight = 0  # keep track of total chain height
# NEW STUFF
recvGossipTimeout = False  # flag for waiting for gossip replies (True=go, False = wait)
recvStatsTimeout = False  # flag for waiting for stats replies -- if true, set peerReply timeout
peerReply = 0  # peer reply timeout
consensus = True  # tracks if we can do consensus
peerIndex = 0
waiting = -1
invalid = False  # tracks if a block is invalid upon recieving a response
hh = ()
# ----SOCK.SEND----
'''
GOSSIP:  
   PROTOCOL
        REQ
        {
            "type":"GOSSIP",
            "host": "HOST",
            "port": PORT,
            "id": msg id,
            "name": "myname"

        }  
'''


def gossip(msg, peer):
    sock.sendto(json.dumps(msg).encode('utf-8'), peer)


'''
GOSSIP_REPLY:
    PROTOCOL
        {
            "type":"GOSSIP_REPLY",
            "host": "HOST",
            "post": PORT,
            "name": name
        }
'''


def gossipReply(msg, peer):
    resp = {
        "type": "GOSSIP_REPLY",
        "host": HOST,
        "post": PORT,
        "name": name
    }
    if msg['id'] not in msgids:
        sock.sendto(json.dumps(resp).encode('utf-8'), peer)
        msgids.append(msg['id'])
        # forward msg to other peers
        for p in peers:
            gossip(msg, p)


'''
GET_BLOCK: request a block with height from a peer
    PROTOCOL
        {
            "type": "GET_BLOCK",
            "height": 0
        }
'''


def getBlock(height):
    global peerIndex
    msg = {
        "type": "GET_BLOCK",
        "height": height
    }
    # peer = statsPeers[random.randint(0, len(statsPeers) - 1)]
    if len(statsPeers) == 0:
        return
    peer = statsPeers[peerIndex % len(statsPeers)]
    sock.sendto(json.dumps(msg).encode('utf-8'), peer)
    # sock.sendto(json.dumps(msg).encode('utf-8'), wellknownHost)
    peerIndex += 1
    return peer


'''
REPLY_BLOCK
    PROTOCOL
    {
        "type": "GET_BLOCK_REPLY",
        "height": None,
        "hash": None,
        "minedBy": None,
        "messages": None,
        "timestamp":None,
        "nonce": None
    }


'''


def replyBlock(height, peer):
    resp = {
        "type": "GET_BLOCK_REPLY",
        "height": None,
        "hash": None,
        "minedBy": None,
        "messages": None,
        "timestamp": None,
        "nonce": None

    }
    # check if height of req block is in bounds
    if height > len(chain) - 1 or height < 0:
        print("Invalid height, sending none resp to peer")
        sock.sendto(json.dumps(resp).encode('utf-8'), peer)
    # if its in bounds, search for that block with that height in our chain
    else:
        for block in chain:
            if block['height'] == height:
                # found it
                resp = {
                    "type": "GET_BLOCK_REPLY",
                    "height": block['height'],
                    "hash": block['hash'],
                    "minedBy": block['minedBy'],
                    "messages": block['messages'],
                    "timestamp": block['timestamp'],
                    "nonce": block['nonce'],

                }
                break
        # print(f" Found block with height {height}, sending to {peer}")
        sock.sendto(json.dumps(resp).encode('utf-8'), peer)


'''
STATS:
    PROTOCOL
        REQ
        {
            "type":"STATS"
        }
    '''


def getStats(peer):
    global statTimeout, statGetFlag

    # print(f"Asking for stats from {peer}")
    msg = {"type": "STATS"}
    sock.sendto(json.dumps(msg).encode('utf-8'), peer)


'''
 STATS_REPLY: send stats about chain to {peer}
    PROTOCOL
     RESP
        {
           "type": "STATS_REPLY",
           "height": 2,
           "hash": "519507660a0dd9d947e18b863a4a54b90eb53c82dde387e1f5e9b48f3d000000"
        }
    '''


def sendStats(peer):
    resp = {
        "type": "STATS_REPLY",
        "height": len(chain),
        "hash": chain[-1]['hash']
    }
    sock.sendto(json.dumps(resp).encode('utf-8'), peer)


'''
CONSENSUS: force peer to do consensus immediately
    PROTOCOL

        {
            "type": "CONSENSUS"
        }

    '''


def peerConsensus(peer):
    msg = {"type": "CONSENSUS"}
    sock.sendto(json.dumps(msg).encode('utf-8'), peer)


# ----HANDLING----
'''
PEER TIMEOUT: removes timed out peer from peerlist
'''


def peerTimeout():
    # remove peers from list on timeout: if current time - peer['time'] >= TIMEOUT, remove it
    currTime = time.time()
    # print("Peer timeout check")
    temp = []
    for peer in peers:
        if currTime - peers[peer]['time'] >= TIMEOUT * 2:
            print(f"Peer {peer} has timed out. Remove them")
            temp.append(peer)
            # peers.pop(peer)
    for peer in temp:
        peers.pop(peer)


'''
ADD PEER: take peer info and put into dict that will be added to peers[]
'''


def addPeer(pHost, pPort, pName, pTime):
    np = {
        "host": pHost,
        "port": pPort,
        "name": pName,
        "time": pTime
    }
    return np


'''
'''


def longestChain():
    # print("xxxxxxxxxxxxxxxx")
    global chain, built, consensus, peers, stats, blocks, \
        statsCount, statsPeers, exclude, peerReply, bestChain, statGetFlag, chainHeight
    consensus = False  # we are doing consensus so cant do it in loop
    #exclude any chains that we already know are invalid
    if len(exclude) > 0:
        for ex in exclude:
            stats.pop(ex)
    # make sure that stats has no None values
    temp = []
    for key in stats.keys():
        (height, hash) = key
        if height is None or hash is None:
            temp.append(key)
    for i in temp:
        stats.pop(i)

    try:
        # make sure all heights are sent as ints, not strings bc someone is doing that
        for stat in stats.keys():
            if type(stat[0]) is str:
                stat[0] = int(stat[0])
        mv = max(stats)
    except TypeError as e:
        print(f"{stats}:{traceback.format_exc()}")
        # exit(0)
    # print(f"mv: {mv}")
    l = []
    for key in stats:
        if key == mv:
            l.append(len(stats[key]))
    mp = max(l)  # max peers
    # find the stats record with max height and max peers
    for key in stats:  # for all keys in stats
        if key[0] == mv[0] and len(stats[key]) == mp:
            bestChain = {key: stats[key]}
            break
    hh = mv
    print(f"Best chain {bestChain}\n{bestChain[mv]}")
    statsPeers = bestChain[mv]  # sb all the peers that have bestchain -- global var
    # ask all the peers in statsPeers for blocks (done in getBlock())
    chainHeight = mv[0]
    height = 0
    print("Getting blocks...")
    while height < mv[0]:
        # send getBlock(height)
        # OR RR style: getBlock(height, statsPeer[count])
        getBlock(height)
        height += 1
    # print("xxxxxxxxxxxxxxxx")


'''
ADD BLOCK: add validated block to chain, also for ANNOUNCE
    PROTOCOL
        {
           "type": "ANNOUNCE",
           "height": 3,
           "hash": "75fb3c14f11295fd22a42453834bc393872a78e4df1efa3da57a140d96000000"
           "minedBy": "Rob!",
            "messages": ["test123"],
           "nonce": "27104978",


        }
    '''


def addBlock(block):
    # use globals
    global chainHeight, chain, built, blocks, sameHeight, exclude, chainHeight, waiting, invalid
    try:
        if not built:  # if the chain isnt built
            # is this block the genesis block?
            if len(chain) == 0 and block['height'] == 0:
                print("This is genesis block")
                if validateBlock(block):
                    chain.append(block)
                # else:
                # return False
            # is this the next block?
            elif len(chain) == block['height']:
                print(f"{block['height']} is next block")
                if validateBlock(block):
                    chain.append(block)
                # else:
                # return False
                '''//TODO if the block isnt valid, it goes to request a new one
                    need to track if all peers send back an invalid block -- means chain is invalid and we
                    should find next longest chain
                '''
                # do we still have blocks to add?
                if len(chain) != chainHeight:
                    if blocks.get(len(chain)) is not None:
                        # print("We still have more blocks to add")
                        addBlock(blocks.pop(len(chain)))
                    else:
                        # we dont have the next block, get it
                        print(f"Missing a block, sending: GET_BLOCK({len(chain)})")
                        getBlock(len(chain))
                        waiting = len(chain)
                else:
                    # print("No more blocks, chain is built")
                    # we have no more blocks, so chain is built
                    built = True
                    blocks = {}
                    if validateChain():
                        print(f"Chain with height {len(chain)} is valid and is longest chain")
                        # printChain()
            else:
                # not the next block
                blocks[block['height']] = block
                if blocks.get(len(chain)) is not None:
                    addBlock(blocks.pop(len(chain)))
                else:
                    # we're missing this block
                    print(f"Missing a block, sending: GET_BLOCK({len(chain)})")
                    getBlock(len(chain))
                    waiting = len(chain)
                    # getBlock(len(chain))
                    # getBlock(len(chain))
        else:
            print("Chain is built, adding ANNOUNCE block on top...")
            if validateBlock(block):  # chain is built, add ANNOUNCE block on top
                chain.append(block)
    except Exception as e:
        print(f"{e}:{traceback.format_exc()}")
        pass


'''
VALIDATE BLOCK:
    PROCESS
    - start at bottom of the chain, checking block hash and new hashlib from block details is correct
    - in each block, validate that each msg has max 20 chars AND each block should have max 10 msgs
    - in each block, nonce must be less than 40 chars
    - difficulty at least 9
'''


def validateBlock(block, v=True):
    if block['height'] == 0:  # this is genesis block
        # print("*********GENESIS*************")
        # check nonce
        if len(block['nonce']) >= 40:
            print(f"INVALID BLOCK: GENESIS - NONCE TOO LONG! {block}")
            return False
        # check msg amt
        if len(block['messages']) > 10:
            print(f"INVALID BLOCK: GENESIS - TOO MANY MESSAGES! {block}")
            return False
        # check each msg char
        for msg in block['messages']:
            if len(msg) > 20:
                print(f"INVALID BLOCK: GENESIS - A MESSAGE IS TOO LONG! {block} ")
                return False
        # build hash (no prev hash for genesis) -- only check hash after validating all other info, cause if its
        try:
            genesis = hashlib.sha256()
            genesis.update(block['minedBy'].encode())
            for m in block['messages']:
                genesis.update(m.encode())
            genesis.update(block['timestamp'].to_bytes(8, 'big'))
            genesis.update(str(block['nonce']).encode())
            h = genesis.hexdigest()
            if not h == block['hash']:
                print(f"INVALID BLOCK: GENESIS HASH INVALID! {block}")
                return False
            # print('not invalid block if')
            if h[-1 * DIFFICULTY:] != '0' * DIFFICULTY:
                print(f"INVALID BLOCK: DIFFICULTY TOO LOW {block}")
                return False
        except Exception as e:
            print(f"{e}:{traceback.format_exc()}")
            pass
        # print("**********************")
    else:
        # print("**********************")
        # check nonce
        if len(block['nonce']) >= 40:
            print(f"INVALID BLOCK: NONCE TOO LONG! {block}")
            return False
        # check msg amt
        if len(block['messages']) > 10:
            print(f"INVALID BLOCK: TOO MANY MESSAGES! {block}")
            return False
        # check each msg char
        for msg in block['messages']:
            if len(msg) > 20:
                print(f"INVALID BLOCK: A MESSAGE IS TOO LONG! {block} ")
                return False
        # build hash -- only check hash after validating all other info, cause if its wrong hash is wrong
        hashBase = hashlib.sha256()
        if v:
            # print("**************************************")
            prev = chain[len(chain) - 1]  # validate block
        else:
            prev = chain[block['height'] - 1]  # when validating chain

        hashBase.update(prev['hash'].encode())
        hashBase.update(block['minedBy'].encode('utf-8'))
        for m in block['messages']:
            hashBase.update(m.encode('utf-8'))
        hashBase.update(block['timestamp'].to_bytes(8, 'big'))
        hashBase.update(str(block['nonce']).encode('utf-8'))
        h = hashBase.hexdigest()
        if not h == block['hash']:
            print(f"INVALID BLOCK: CIPHERS DONT CHAIN! {block}")
            # print(f'{h}\n{block["hash"]}')
            print(f"{block['height']} - {prev['height']}")
            return False
        if h[-1 * DIFFICULTY:] != '0' * DIFFICULTY:
            print(f"INVALID BLOCK: DIFFICULTY TOO LOW {block}")
            return False
        # print("**********************")
    return True


'''
VALIDATE CHAIN: Validates the entire chain, end-to-end, starting at the bottom
:return: True on valid chain, False otherwise
'''


def validateChain():
    print("VALIDATING CHAIN")
    for block in chain:
        if not validateBlock(block, False):
            return False  # a block is invalid, so chain invalid
    return True


'''
'''


def keepAlive():
    id = str(uuid.uuid4())
    msgids.append(id)
    msg = {"type": "GOSSIP", "host": HOST, "port": PORT, "id": id, "name": name}
    # sock.sendto(json.dumps(msg).encode(), wellknownHost)
    if len(peers) >= 3:
        # send to 3 randos
        temp = []
        for p in peers:
            temp.append(p)
        # temp = peers
        try:
            p1 = random.randint(0, len(peers) - 1)
            sock.sendto(json.dumps(msg).encode(), temp[p1])
            temp.pop(p1)
            p2 = random.randint(0, len(temp) - 1)
            sock.sendto(json.dumps(msg).encode(), temp[p2])
            temp.pop(p2)
            p3 = random.randint(0, len(temp) - 1)
            sock.sendto(json.dumps(msg).encode(), temp[p3])
        except KeyError:
            print(temp, traceback.format_exc())
    else:
        # just send to rob
        sock.sendto(json.dumps(msg).encode(), wellknownHost)


'''
PRINT CHAIN: prints each block in the chain in a nicely formatted way
'''


def printChain():
    # print("Printing chain for visual validation")
    for c in chain:
        print(f"{c['height']}:\n  \t{c['minedBy']}\n \t{c['nonce']}\n \t{str(c['messages'])}\n \t{c['hash']}")


'''
HANDLE: decides what to do based on the message received from a peer
'''


def handle(d, peer):
    # globals
    global chain, built, peers, stats, blocks, exclude, recvGossipTimeout, recvStatsTimeout, peerReply, consensus, \
        chainHeight, waiting, hh
    try:
        data = json.loads(d.decode('utf-8'))
        if type(data) is str:  # someone sent me garbo, had to load again???
            data = json.loads(data)
        if data['type'] == 'ANNOUNCE':
            # print("------------------")
            print(f'recv ANNOUNCE from {peer}')
            # if unknown peer, add to peers
            if (data['host'], data['peer']) not in peers.keys():
                # from new peer -- add new (host,port):peerdict to peers list
                peers[(data['host'], data['port'])] = addPeer(data['host'], data['port'], data['name'], time.time())
            block = {
                "height": data['height'],
                "hash": data['hash'],
                "minedBy": data['minedBy'],
                "messages": data['messages'],
                "timestamp": data['timestamp'],
                "nonce": data['nonce']
            }
            addBlock(block)
            # check timeout
            peerTimeout()
        elif data['type'] == 'GOSSIP' and data['id'] not in msgids:
            print(f'recv GOSSIP from {peer}')
            if data['host'] not in peers.keys() or data['peer'] not in peers:
                # from new peer -- add new peer to peers
                peers[(data['host'], data['port'])] = addPeer(data['host'], data['port'], data['name'], time.time())
            else:
                # update this peers reply time
                peers[(data['host'], data['port'])]['time'] = time.time()
            # data from a known peer
            gossipReply(data, peer)
            # check timeout
            peerTimeout()
        elif data['type'] == 'GOSSIP_REPLY':
            if recvGossipTimeout == 0:
                recvGossipTimeout = time.time()  # got first goss reply, set timeout
            # print("------------------")
            print(f'recv GOSSIP_REPLY from {peer}')
            if data['host'] not in peers.keys() or data['peer'] not in peers:
                # from new peer -- add new peer to peers (dont add me tho)
                peers[(data['host'], data['port'])] = addPeer(data['host'], data['port'], data['name'], time.time())
            else:
                # update this peers reply time
                peers[(data['host'], data['port'])]['time'] = time.time()
            # check timeout
            peerTimeout()
        elif data['type'] == 'GET_BLOCK':
            # print("------------------")
            print(f'recv GET_BLOCK from {peer}')
            # send getblockreply
            replyBlock(data['height'], peer)
        elif data['type'] == 'GET_BLOCK_REPLY' and not built:
            # print("------------------")
            # print(f'recv GET_BLOCK_REPLY from {peer}')
            # build block with sent data
            block = {
                "height": data['height'],
                "hash": data['hash'],
                "minedBy": data['minedBy'],
                "messages": data['messages'],
                "timestamp": data['timestamp'],
                "nonce": data['nonce']
            }
            # if block['hash']!=None:
            # print(block['height'])
            if block['height'] == waiting:
                waiting = -1
            blegh = True
            for x in blocks.values():
                # print(x)
                if x['height'] == block['height']:
                    blegh = False
                    break
            if block['hash'] is not None and blegh:  # and block not in blocks:
                # chainHeight = block['height']
                blocks[block['height']] = block
                addBlock(block)  # validates blocks in method
                '''if ret is not None: #couldnt add block, peer sent invalid block
                    #remove peer from statsPeers bc all blocks after will be invalid
                    statsPeers.pop(statsPeers.index(peer))
                    if len(statsPeers)==0:
                        #need to switch chains -- this one is invalid
                        exclude.append(hh)'''
            # check timeout
            peerTimeout()
        elif data['type'] == 'STATS':
            # print("------------------")
            print(f'recv STATS from {peer}')
            # send my chain out if its built & valid
            if built and validateChain():
                sendStats(peer)
            # check timeout
            peerTimeout()
        elif data['type'] == 'STATS_REPLY':
            if recvStatsTimeout:
                peerReply = time.time()
                recvStatsTimeout = False
                # print(f"Reply >=1: {time.time() - peerReply >= 1}, built? {built}, stats >0 : {len(stats) > 0},"
                # f" allowed to do consensus?  {consensus}")
            # print("------------------")  # //gives top block, height and hash
            print(f"recv STATS_REPLY from {peer}")
            # if we dont have this height/hash pairing, add it to stats list
            if stats.get((data['height'], data['hash'])) is None:
                stats[(data['height'], data['hash'])] = []
                # add the peer that sent it
                stats[(data['height'], data['hash'])].append(peer)
            else:
                # we have this height/hash pairing, add the peer if not already in list
                if peer not in stats[(data['height'], data['hash'])]:
                    stats[(data['height'], data['hash'])].append(peer)
            # check timeout
            peerTimeout()
        elif data['type'] == 'CONSENSUS' and not built:  # only do this if im not currently building a chain
            # print("------------------")
            print(f'recv CONSENSUS from {peer}')
            # someone wants me to do consensus --> clear vars and request chain
            chain = []
            blocks = {}
            built = False
            exclude = []
            consensus = True
            # consensusTime = time.time()
            stats = {}
            # send STATS msg to get stats to build chain
            print("Requesting stats...")
            for p in peers:
                getStats(p)
            # reset stats timeout var
            recvStatsTimeout = True
            # check timeout
            peerTimeout()
    except KeyError as k:
        print(f"INVALID JSON KEY: {k}\n from peer {peer} with message: {d}")
        pass
    except JSONDecodeError as j:
        print(f"JSON DECODE ERROR: {j}\n from peer: {peer} with message: {d}")
        pass
        # if peer != ("130.179.28.116",8999): #ignore goose for now
        # print(f"JSON DECODE ERROR: {j}\n from peer: {peer} with message: {d}")
        # print("JSON DECODE ERROR - This is fine, its probably goose")
    except Exception as exception:
        print(f"OTHER EXCEPTION: {exception}\n from peer: {peer} with message: {d}")
        #print(traceback.format_exc())
        pass
        # print(blocks)
        # exit(0)



    # ----MAIN----


if __name__ == '__main__':
    # -----SETUP------
    # SOCKET SETUP - UDP: socket, bind, send, recv, close
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # set sockop so we can reuse addrs
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    name = "rat"
    sock.bind((HOST, PORT))
    # set timeout
    TIMEOUT = 30  # bc ping wellknown host every 30s, but dropped after 60s
    sock.settimeout(TIMEOUT * 2)
    # GET WELLKNOWN HOST
    #wellknownHost = ('192.168.101.248', 8999)  # umber
    wellknownHost = (gethostbyname('130.179.28.37'), 8999) #-- silicon
    #print(wellknownHost)
    # ------JOIN NETWORK & TIMEOUT STUFF-----
    lastTimeout = time.time()
    consensusTime = time.time()
    # we've joined the network, send keepAlive to wellknown host
    keepAlive()
    reqStats = True
    waittime = time.time()
    # getBlock(1984)
    while True:
        try:
            # recv data from peer
            data, peer = sock.recvfrom(1024)
            # print(data)
            # exit(0)
            if data != b'{}' and data != b'':  # make sure data isnt empty string or empty msg
                handle(data, peer)
            # should only request stats if reqStats is true
            if reqStats and time.time() - recvGossipTimeout >= 5 and not built:
                # reset stats timeout var
                recvStatsTimeout = True
                # request stats from all peers
                reqStats = False
                for peer in peers:
                    getStats(peer)
            if time.time() - peerReply >= 1 and not built and len(stats) > 0 and consensus:
                print("-FINDING LONGEST CHAIN-")
                longestChain()
                # printChain()
            if time.time() - consensusTime >= 120:  # do consensus every 2 mins
                consensusTime = time.time()
                chain = []
                blocks = {}
                built = False
                exclude = []
                consensus = True
                stats = {}
                reqStats = True
            if waiting > -1 and time.time() - waittime > 1:  # we are waiting for block with height=waiting
                waittime = time.time()
                p = getBlock(waiting)
                print(f"requesting next block at height {waiting} from {p}")

            # timeout/keepAlive
            if time.time() - lastTimeout >= TIMEOUT:
                keepAlive()
                lastTimeout = time.time()
            sys.stdout.flush()  # clear buffer and print all stuff
        except KeyboardInterrupt:
            # print("Recieved keyboard interrupt, getting stats...")
            '''if len(stats) > 0:
                for stat in stats:
                    print(f"{str(stat)}:{str(stats.get(stat))}")'''
            if built:
                print(f"Printing chain with height {len(chain)} and hash {chain[len(chain) - 1]['hash']}")
                printChain()
            # print(peers)
            sock.close()
            sys.exit(0)
        except ConnectionError as e:
            print(f"Disconnected from socket manually: {e}::{traceback.format_exc()}")
            sock.close()
            sys.exit(0)
        except JSONDecodeError as e:
            print(f"Error decoding JSON: {e}::{traceback.format_exc()}")
            print("Probably bad peer: improperly formatted messages")
            pass
            # sock.close()
            # sys.exit(0)
        except timeout:
            keepAlive()
            print("Socket timed out, handling timeout")
