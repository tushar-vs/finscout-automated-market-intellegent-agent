import pytest
from app.etl import DataTransformer

# Test the ETL Logic (Unit Test)
def test_volume_conversion():
    raw_data = [{"symbol": "TEST", "name": "Test", "price_raw": "100", "change": "+1", "volume_raw": "2.5M"}]
    clean_data = DataTransformer.clean(raw_data)
    
    assert len(clean_data) == 1
    assert clean_data[0]['volume'] == 2_500_000.0  

def test_price_cleanup():
    raw_data = [{"symbol": "TEST", "name": "Test", "price_raw": "1,000.50", "change": "+1", "volume_raw": "100"}]
    clean_data = DataTransformer.clean(raw_data)
    
    assert clean_data[0]['price'] == 1000.50  