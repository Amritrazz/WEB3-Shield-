import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from neo4j import AsyncGraphDatabase
from app.config import settings

# 1. Mock Threat Data Packets
PHISHING_DOMAINS = [
    {"url": "https://metamask-wallet-connect.xyz", "threat_type": "wallet_drainer", "severity": "CRITICAL"},
    {"url": "https://uniswap-claims-compromised.com", "threat_type": "phishing_rewards", "severity": "HIGH"},
    {"url": "https://free-eth-airdrop.net", "threat_type": "credential_harvesting", "severity": "HIGH"},
    {"url": "https://opensea-mint-scam.co", "threat_type": "malicious_mint", "severity": "CRITICAL"}
]

WALLET_GRAPH_NODES = [
    {"address": "0xScamAttacker111", "label": "AttackerRoot"},
    {"address": "0xDrainerContract222", "label": "ExploitContract"},
    {"address": "0xVictimWallet333", "label": "Victim"}
]

async def seed_mongodb():
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client[settings.PROJECT_NAME.lower().replace("-", "_")]
    collection = db["threat_intelligence"]
    
    # Clean previous records and insert fresh data
    await collection.delete_many({})
    result = await collection.insert_many(PHISHING_DOMAINS)
    print(f"✅ MongoDB Seeded Successfully! Inserted {len(result.inserted_ids)} threat entries.")
    client.close()

async def seed_neo4j():
    print("Connecting to Neo4j Graph Database...")
    # Neo4j connections require the Bolt protocol driver format
    bolt_url = settings.MONGO_URL.replace("mongodb://", "bolt://").split("@")[-1]
    # Fallback directly to defaults if parsing gets complex
    uri = "bolt://neo4j:7687" 
    
    # Extracted from your environment or .env configuration setups
    auth_credentials = ("neo4j", "my_secure_neo4j_pass_2026")
    
    async with AsyncGraphDatabase.driver(uri, auth=auth_credentials) as driver:
        async with driver.session() as session:
            print("Wiping old Neo4j graph nodes...")
            await session.run("MATCH (n) DETACH DELETE n")
            
            print("Building core scam network relationships...")
            # Create nodes and forge trace links tracking asset theft routes
            await session.run("""
                CREATE (a:Wallet {address: '0xScamAttacker111', type: 'Attacker'})
                CREATE (c:SmartContract {address: '0xDrainerContract222', type: 'Drainer'})
                CREATE (v:Wallet {address: '0xVictimWallet333', type: 'Victim'})
                
                CREATE (c)-[:DIVERTS_FUNDS_TO]->(a)
                CREATE (v)-[:INTERACTED_WITH {loss_eth: 4.5}]->(c)
            """)
    print("✅ Neo4j Graph Network Engine Seeded Successfully!")

async def main():
    print("=== Starting Web3-Shield Initial Seeding Loop ===")
    try:
        await seed_mongodb()
        await seed_neo4j()
        print("=== Database Initialization Script Completed Efficiently ===")
    except Exception as e:
        print(f"❌ Seeding Failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())