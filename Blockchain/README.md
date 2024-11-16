# READ ME
##### Katrina Dotzlaw 7833061   
##### COMP 3010 A3   

## Run Instructions   
Run with: `python3 a3.py {host} {port}`
##### If Testing on Silicon
- Local host and port that i used to test on silicon was on aviary's owl machine: ` 130.179.28.127 8055`
- Line 706 sets the wellknown host to silicon's ip and port (comment out line 705). The chain on silicon is really long so it'll take a bit to sync up.
##### If Testing on Umber Test Network:
- Local ip needs to be a 192.x.y.z,  when I tested i used `192.168.101.248 8055` as local host and port.
- Line 705 sets wellknown host to umber's ip and port (comment out line 706).
## Code Info
- My code accepts CONSENSUS requests from peers in the following form (Rob just said specify what request we implemented):
`  {
            "type": "CONSENSUS"
        }`   
- My peer name is **rat**
- On keyboard interrupt, if a chain is built it will be printed to console. 
### Issues
- On the silicon blockchain, I was having issues after receiving ANNOUNCE from peer leorize, who sent nonces that looked like: Vzcq.E|%@Eu`|
  - I can request stats, find the longest chain, and validate it. There's just an issue with that peer announcing a new block. I dont
  think this is going to be an issue when testing, but now you know just in case it is.
  - My code works great on all the test networks, its literally just a problem with that peer.

## Rubric
### Joining
- On joining, i immediately send a `keepAlive()` GOSSIP to 3 random peers (or just to wellknown host if there's less than 3 peers) (line 698)
- GOSSIPS with ids that are not in my list of seen ids are replied to via GOSSIP_REPLY (line 559)
- `peerTimeout()` removes peers that have not sent a GOSSIP in a minute (line 222). `peerTimeout()` is called when handling any message type.
- I send GOSSIPs via `keepAlive()` every 30 seconds (line 748) and if the socket times out (line 772).

### Building Chain
- `getBlock(height)`: Blocks are requested round-robin from all peers that sent STATS_REPLYs with longest chain (line 93).
- `addBlock(block)` (lines 323-379): 
  - all blocks are validated before being added. 
  - Blocks are stored in a global list (so ANNOUNCE blocks would go here)
  - block is popped off if its  the next block. 
  - If we dont have the next block, I send another `getBlock(height)` request and track that Im waiting for that height.
  - Once the length of the chain is equal to the max height, chain is built and is validated.
- `validateChain()` (line 480): validates end-to-end by validating each block in the chain using `validateBlock(block,True/False)` (lines 392-471).
  - True if validating block while its being built, False if we are validating a fully-built chain.
  - Validates: nonce <= 40 chars, messages[] < 10, len(message) <=20 chars, hash (respects order defined in A3), and difficulty >= 9
- `ANNOUNCE` blocks added ontop of a built chain, or put into global list of blocks and added to top of chain 
after its built (lines: 558, 365)   

### Consensus
- CONSENSUS process: send STATS to all known peers, wait for timeout amount of time,  `longestChain()`, `GET_BLOCKS(height)` sent to all peers that have longest chain,
`addBlock(block)`, validate each block, request missing blocks. Validate chain end-to-end when its built.
- After joining the network and receiving GOSSIP_REPLYs from peers, I send STATS to all known peers (line 728), begin consensus after 
receiving STATS_REPLYs (determined by a timeout,  line 729 ).
  - I also do CONSENSUS every 2 minutes (line 733)
- `longestChain()`finds the max (height,hash) key in the STATS_REPLYs (stored in statsPeers: `{(height,hash}:[peer1,peer2...]}`). It should immediately break ties by finding the max number of peers with max height (line 255).
- When receiving a STATS from a peer, I validate the entire chain before sending it.

