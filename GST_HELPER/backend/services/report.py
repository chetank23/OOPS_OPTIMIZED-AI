import pandas as pd
import os
from datetime import datetime

def generate(data):
    try:
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"reports/report_{timestamp}.csv"
        
        flattened = []
        for item in data:
            flat_item = {
                "filename": item.get("filename", ""),
                "gstin": item.get("fields", {}).get("gstin", ""),
                "invoice_no": item.get("fields", {}).get("invoice_no", ""),
                "date": item.get("fields", {}).get("date", ""),
                "amount": item.get("fields", {}).get("amount", 0),
                "status": item.get("validation", {}).get("status", ""),
                "issues": "|".join(item.get("validation", {}).get("issues", []))
            }
            flattened.append(flat_item)
        
        if flattened:
            pd.DataFrame(flattened).to_csv(path, index=False)
        
        return path
    except Exception as e:
        print(f"Report Generation Error: {str(e)}")
        return f"Error generating report: {str(e)}"