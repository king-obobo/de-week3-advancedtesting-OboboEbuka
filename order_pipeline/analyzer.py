# Computes:
# Total revenue
# Average revenue
# total number of paid/pending/refunded each

class Analyzer:
    
    def __init__(self, file: list):
        self.file = file
        

    def compute_revenue_vals(self) -> int | float:
        # Get all the revenue and store in a list
        # Calculate the total from here
        all_totals = []
        for row in self.file:
            all_totals.append(row["total"])
        
        return sum(all_totals), len(all_totals)

    
    def compute_total_revenue(self):
        total_revenue, _ = self.compute_revenue_vals()
        return round(total_revenue, 2)
    
    
    def compute_average_revenue(self) -> int | float:
        # Get all the revenue and store in a list
        # Calculate the total from here
        total_revenue, no_of_revenue_value = self.compute_revenue_vals()
        return round(total_revenue / no_of_revenue_value, 2)
    
    
    def compute_payment_status(self) -> dict:
        paid = 0
        pending = 0
        refunded = 0
        
        for row in self.file:
            if row["payment_status"] == "paid":
                paid+=1
            if row["payment_status"] == "pending":
                pending+=1
            if row["payment_status"] == "refunded":
                refunded+=1
                
        return {
            "paid": paid,
            "pending": pending,
            "refunded": refunded
        }