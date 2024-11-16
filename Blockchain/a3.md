## Joining the Network

On joining the network, a `keep_alive()` GOSSIP is sent to 3 random peers (or just to wellknown host if there's less than 3 peers). Any GOSSIPs that have ids that are not in the global list of ids are replied to via GOSSIP_REPLY.
Any peers that have not sent a GOSSIP for at least a minute are assumed to have timed out and are removed from the global list of peers via `peerTimeout()`. 
To ensure that the application is not timed out by peers, GOSSIPs are sent every 30 seconds via `keep_alive()`. GOSSIPs are also sent out if the socket times out.


## Consensus Process
send STATS-->wait & recv STAT_REPLYs-->`longest_chain()`-->send `GET_BLOCKS (height)` to peers with longest chain -->validate block--> `add_block(block)` to local chain/send `GET_BLOCKS(height) for missing blocks --> validate chain

After joining the network and receiving GOSSIP_REPLYs, the consensus process begins. 
A STATS request is sent to all known peers. After waiting a timeout amount of time for STAT_REPLYs, the longest chain is identified using max(height,hash) included in the reply and the method `longest_chain()`. Ties are immediately broken by finding the max number of peers with the max height. After determining the longest chain, blocks are requested round-robin from all peers that have the longest chain via `get_blocks(height)`. 


When adding a block to the local chain:
- All blocks are validated before being added
- Blocks are stored in a global list since they might not be received in height order and popped off if they are the next block 
- If the next block needed is missing, send another `get_block(height)` request to known peers with longest chain
- Blocks that are mined and ANNOUNCED are either added to the top of the chain if it is built, or stored in the global list

To be considered valid a block must meet the following criteria:
- Its nonce must be at most 40 characters
- A block must have less than 10 messages
- Each message in the block must be at most 20 characters
- Its hash must respect the order predefined by instructor
- The block difficulty must be at least 9

To ensure local chain synchronization with the distributed chain:
- Consensus is done every 2 minutes 
- Consensus can be requested by peers via CONSENSUS request
- Validate the entire local chain before sending it upon receiving a STATS request from a peer


