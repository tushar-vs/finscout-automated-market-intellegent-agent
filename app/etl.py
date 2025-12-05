import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataTransformer:
    @staticmethod
    def clean(raw_data: list) -> list:
        if not raw_data:
            return []
            
        logger.info("Starting ETL Transformation...")
        df = pd.DataFrame(raw_data)

        # 1. Clean Price: Remove commas, convert to float
        
        df['price'] = pd.to_numeric(df['price_raw'].astype(str).str.replace(',', ''), errors='coerce')

        # 2. Clean Volume: Convert "M" (Million) and "B" (Billion) to numbers
        
        def parse_volume(vol_str):
            vol_str = str(vol_str).replace(',', '')
            if 'T' in vol_str:
                return float(vol_str.replace('T', '')) * 1_000_000_000_000
            if 'B' in vol_str:
                return float(vol_str.replace('B', '')) * 1_000_000_000
            if 'M' in vol_str:
                return float(vol_str.replace('M', '')) * 1_000_000
            try:
                return float(vol_str)
            except:
                return 0.0

        df['volume'] = df['volume_raw'].apply(parse_volume)

        # 3. Select final columns
        final_df = df[['symbol', 'name', 'price', 'change', 'volume']]
        
        # Convert back to list of dicts for the database
        cleaned_data = final_df.to_dict(orient='records')
        logger.info(f"ETL Complete. Processed {len(cleaned_data)} records.")
        return cleaned_data