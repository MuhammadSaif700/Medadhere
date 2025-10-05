"""Quick test to check if Panadol search works"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.pill_data_service import PillDataService

async def test_panadol():
    service = PillDataService()
    
    print("\n🔍 Testing search for 'Panadol'...")
    results = await service.search_by_name("Panadol")
    
    print(f"\n✅ Found {len(results)} results:")
    for i, result in enumerate(results[:5], 1):
        print(f"\n{i}. {result.get('name', 'Unknown')}")
        print(f"   Dosage: {result.get('dosage', 'Unknown')}")
        print(f"   Source: {result.get('source', 'Unknown')}")
        print(f"   Generic: {result.get('generic_name', 'Unknown')}")

if __name__ == "__main__":
    asyncio.run(test_panadol())
