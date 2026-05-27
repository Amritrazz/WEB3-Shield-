from neo4j import AsyncGraphDatabase
from app.config import settings

driver = AsyncGraphDatabase.driver(
    settings.neo4j_url,
    auth=(settings.neo4j_user, settings.neo4j_pass)
)

async def create_wallet(address: str, chain: str, label: str = "unknown"):
    async with driver.session() as s:
        await s.run(
            "MERGE (w:Wallet {address: $addr}) "
            "SET w.chain=$chain, w.label=$label",
            addr=address, chain=chain, label=label
        )

async def create_transaction(from_addr: str, to_addr: str,
                              amount: float, token: str):
    async with driver.session() as s:
        await s.run("""
            MERGE (a:Wallet {address: $from_addr})
            MERGE (b:Wallet {address: $to_addr})
            CREATE (a)-[:SENT_TO {
                amount: $amount,
                token: $token,
                ts: datetime()
         }]->(b)
        """, from_addr=from_addr, to_addr=to_addr,
             amount=amount, token=token)

async def get_scam_distance(address: str) -> dict:
    """How many hops from this wallet to a known scammer?"""
    async with driver.session() as s:
        result = await s.run("""
            MATCH (target:Wallet {address: $addr})
            MATCH (scammer:Wallet {label: 'scammer'})
            MATCH path = shortestPath(
                (target)-[:SENT_TO*1..5]-(scammer)
            )            
                             RETURN length(path) as hops, scammer.address as scammer
            ORDER BY hops ASC LIMIT 1
        """, addr=address)
        record = await result.single()
        if record:
            return {"hops": record["hops"], "scammer": record["scammer"]}
        return {"hops": None, "scammer": None}

async def get_wallet_subgraph(address: str) -> dict:
    """Get 2-hop network around a wallet for visualization"""
    async with driver.session() as s:
        result = await s.run("""
            MATCH (w:Wallet {address: $addr})-[:SENT_TO*1..2]-(neighbor)
            RETURN w, neighbor
        """, addr=address)
        records = await result.data()
        return {"nodes": records}