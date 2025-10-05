"""
Service to fetch real pill data from external medical databases
"""
import httpx
import logging
from typing import Dict, List, Optional, Any
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

class PillDataService:
    """
    Fetches real pill/medication data from FDA and other medical APIs
    """
    
    def __init__(self):
        self.fda_api_base = "https://api.fda.gov/drug"
        self.rxnorm_api_base = "https://rxnav.nlm.nih.gov/REST"
        self.timeout = 10.0
        
    async def search_by_name(self, medication_name: str) -> List[Dict[str, Any]]:
        """
        Search for medications by name using FDA and RxNorm APIs
        
        Args:
            medication_name: Name of the medication to search for
            
        Returns:
            List of matching medication records with standardized format
        """
        results = []
        
        # Try RxNorm first (free, no API key needed, comprehensive)
        try:
            rxnorm_results = await self._search_rxnorm(medication_name)
            results.extend(rxnorm_results)
        except Exception as e:
            logger.warning(f"RxNorm search failed: {e}")
        
        # Try FDA OpenFDA API
        try:
            fda_results = await self._search_fda(medication_name)
            results.extend(fda_results)
        except Exception as e:
            logger.warning(f"FDA search failed: {e}")
        
        # Deduplicate and rank by relevance
        results = self._deduplicate_and_rank(results, medication_name)
        
        return results[:10]  # Return top 10 results
    
    async def search_by_imprint(self, imprint: str) -> List[Dict[str, Any]]:
        """
        Search for pills by imprint code
        
        Args:
            imprint: Text/code on the pill
            
        Returns:
            List of matching pills
        """
        try:
            # Use FDA's drug label API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Clean imprint text
                clean_imprint = imprint.strip().upper()
                
                # Search FDA NDC directory
                url = f"{self.fda_api_base}/ndc.json"
                params = {
                    "search": f'openfda.brand_name:"{clean_imprint}" OR openfda.generic_name:"{clean_imprint}"',
                    "limit": 10
                }
                
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return self._format_fda_ndc_results(data)
                    
        except Exception as e:
            logger.error(f"Imprint search error: {e}")
        
        return []
    
    async def _search_rxnorm(self, name: str) -> List[Dict[str, Any]]:
        """Search RxNorm API"""
        results = []
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Approximate match search
                url = f"{self.rxnorm_api_base}/approximateTerm.json"
                params = {"term": name, "maxEntries": 10}
                
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    
                    if "approximateGroup" in data and "candidate" in data["approximateGroup"]:
                        for candidate in data["approximateGroup"]["candidate"]:
                            # Get detailed info for each candidate
                            rxcui = candidate.get("rxcui")
                            if rxcui:
                                details = await self._get_rxnorm_details(rxcui)
                                if details:
                                    results.append(details)
                                    
        except Exception as e:
            logger.error(f"RxNorm search error: {e}")
        
        return results
    
    async def _get_rxnorm_details(self, rxcui: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for an RxNorm concept"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.rxnorm_api_base}/rxcui/{rxcui}/properties.json"
                response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    props = data.get("properties", {})
                    
                    return {
                        "name": props.get("name", "Unknown"),
                        "dosage": self._extract_dosage(props.get("name", "")),
                        "generic_name": props.get("name", ""),
                        "rxcui": rxcui,
                        "source": "RxNorm",
                        "shape": "unknown",
                        "color": "unknown",
                        "manufacturer": "Various",
                        "description": f"RxNorm ID: {rxcui}"
                    }
        except Exception as e:
            logger.error(f"RxNorm details error: {e}")
        
        return None
    
    async def _search_fda(self, name: str) -> List[Dict[str, Any]]:
        """Search FDA OpenFDA API"""
        results = []
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Try NDC directory first
                url = f"{self.fda_api_base}/ndc.json"
                params = {
                    "search": f'(brand_name:"{name}" OR generic_name:"{name}")',
                    "limit": 10
                }
                
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    results.extend(self._format_fda_ndc_results(data))
                    
        except Exception as e:
            logger.error(f"FDA search error: {e}")
        
        return results
    
    def _format_fda_ndc_results(self, data: Dict) -> List[Dict[str, Any]]:
        """Format FDA NDC API results to our schema"""
        results = []
        
        if "results" in data:
            for item in data["results"]:
                result = {
                    "name": item.get("brand_name", item.get("generic_name", "Unknown")),
                    "generic_name": item.get("generic_name", ""),
                    "dosage": item.get("active_ingredients", [{}])[0].get("strength", ""),
                    "shape": "unknown",
                    "color": "unknown",
                    "ndc_number": item.get("product_ndc", ""),
                    "manufacturer": item.get("labeler_name", "Unknown"),
                    "source": "FDA",
                    "description": item.get("dosage_form", "")
                }
                results.append(result)
        
        return results
    
    def _extract_dosage(self, name: str) -> str:
        """Extract dosage from medication name"""
        import re
        # Look for patterns like "10mg", "5 mg", "100MG"
        match = re.search(r'(\d+\.?\d*)\s*(mg|mcg|g|ml|%)', name, re.IGNORECASE)
        if match:
            return match.group(0)
        return ""
    
    def _deduplicate_and_rank(self, results: List[Dict], query: str) -> List[Dict]:
        """Remove duplicates and rank by relevance to query"""
        seen = set()
        unique_results = []
        
        for result in results:
            # Create a key for deduplication
            key = (
                result.get("name", "").lower(),
                result.get("dosage", "").lower(),
                result.get("generic_name", "").lower()
            )
            
            if key not in seen:
                seen.add(key)
                # Add relevance score
                result["relevance"] = self._calculate_relevance(result, query)
                unique_results.append(result)
        
        # Sort by relevance
        unique_results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        
        return unique_results
    
    def _calculate_relevance(self, result: Dict, query: str) -> float:
        """Calculate relevance score for ranking"""
        query_lower = query.lower()
        name = result.get("name", "").lower()
        generic = result.get("generic_name", "").lower()
        
        # Exact match gets highest score
        if query_lower == name or query_lower == generic:
            return 1.0
        
        # Use sequence matching for partial matches
        name_ratio = SequenceMatcher(None, query_lower, name).ratio()
        generic_ratio = SequenceMatcher(None, query_lower, generic).ratio()
        
        return max(name_ratio, generic_ratio)
