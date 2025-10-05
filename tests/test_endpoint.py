"""Test the search endpoint directly"""
import requests

url = "http://localhost:8010/api/v1/pills/search?name=Panadol"

print(f"\n🔍 Testing: {url}")
print("="*60)

try:
    response = requests.get(url)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.ok:
        data = response.json()
        print(f"\n✅ Success! Found {len(data)} results\n")
        
        for i, pill in enumerate(data[:5], 1):
            print(f"{i}. {pill.get('name', 'Unknown')}")
            print(f"   Dosage: {pill.get('dosage', 'Unknown')}")
            print(f"   Manufacturer: {pill.get('manufacturer', 'Unknown')}")
            print(f"   Shape: {pill.get('shape', 'unknown')}, Color: {pill.get('color', 'unknown')}")
            print()
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ Exception: {e}")
