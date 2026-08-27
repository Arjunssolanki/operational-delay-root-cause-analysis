import pandas as pd
import numpy as np
from scipy import stats
import mysql.connector
import os
from dotenv import load_dotenv 
load_dotenv()

def execute_mysql_analytics_pipeline():
    print(f"[INFO] Current Active Directory: {os.getcwd()}")
    print("[INFO] Attempting secure link to your local MySQL instance...")
    
    # 🛑 ACTION REQUIRED: Change 'your_password' below to your actual local MySQL password!
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': os.getenv('DB_PASSWORD'),  
        'database': 'logistics_analytics'
    }
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        print(f"\n[ERROR] Connection failed: {err}")
        print("[TIP] Ensure your MySQL Server service is running and your password is correct.")
        return

    # ====================================================================
    # SUB-STEP A: GENERATING LOGISTICS TRANSACTION DATA (In-Memory)
    # ====================================================================
    print("[INFO] Simulating 1,000 corporate shipping records...")
    np.random.seed(42)
    mock_records = 1000
    
    carriers = ['Bluedart', 'Delhivery', 'DHL', 'FedEx']
    origins = ['Delhi', 'Mumbai', 'Bangalore']
    destinations = ['Pune', 'Chennai', 'Kolkata']
    risk_tiers = ['Low Risk', 'Moderate Risk', 'High Risk']
    
    tx_ids = [f'TXN{i:05d}' for i in range(mock_records)]
    chosen_carriers = np.random.choice(carriers, size=mock_records)
    chosen_origins = np.random.choice(origins, size=mock_records)
    chosen_destinations = np.random.choice(destinations, size=mock_records)
    planned_hours = np.random.uniform(24, 72, size=mock_records)
    chosen_risks = np.random.choice(risk_tiers, size=mock_records, p=[0.5, 0.3, 0.2])
    
    # Adding systemic transit delay hours linked to specific risk categories
    risk_adder = np.vectorize(lambda x: 1.2 if x == 'Low Risk' else (3.5 if x == 'Moderate Risk' else 8.1))(chosen_risks)
    actual_hours = planned_hours + risk_adder + np.random.normal(0, 2, mock_records)

    # ====================================================================
    # SUB-STEP B: EXECUTING BULK INGESTION INTO MYSQL SERVER
    # ====================================================================
    print("[INFO] Clearing existing logs and piping datasets to MySQL database...")
    cursor.execute("TRUNCATE TABLE logistics_delivery_logs;")
    
    insert_query = """
    INSERT INTO logistics_delivery_logs 
    (transaction_id, carrier_name, origin_city, destination_city, planned_transit_hours, actual_transit_hours, risk_classification, operational_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    batch_data = [
        (tx_ids[i], chosen_carriers[i], chosen_origins[i], chosen_destinations[i], 
         float(planned_hours[i]), float(actual_hours[i]), chosen_risks[i], 'Completed')
        for i in range(mock_records)
    ]
    
    cursor.executemany(insert_query, batch_data)
    conn.commit()
    print(f"[SUCCESS] Ingested {cursor.rowcount} data rows into MySQL server table successfully.")

    # ====================================================================
    # SUB-STEP C: SERVER-SIDE DATABASE ANALYTICS (CTEs & Windows)
    # ====================================================================
    print("[INFO] Pushing advanced analytical SQL calculations to MySQL Engine...")
    
    mysql_analytical_query = """
    WITH CalculatedDeviations AS (
        SELECT 
            transaction_id, carrier_name, origin_city, destination_city, risk_classification, 
            planned_transit_hours, actual_transit_hours, 
            (actual_transit_hours - planned_transit_hours) AS delivery_time_deviation 
        FROM logistics_delivery_logs 
        WHERE operational_status = 'Completed'
    ), 
    SLAFlaggedData AS (
        SELECT *, 
            CASE WHEN delivery_time_deviation > 4.0 THEN 1 ELSE 0 END AS sla_breached, 
            AVG(delivery_time_deviation) OVER(PARTITION BY carrier_name) AS carrier_avg_deviation 
        FROM CalculatedDeviations
    ) 
    SELECT 
        transaction_id, carrier_name, origin_city, destination_city, risk_classification, 
        ROUND(delivery_time_deviation, 2) as delivery_time_deviation, 
        sla_breached, 
        ROUND(carrier_avg_deviation, 2) as carrier_avg_deviation 
    FROM SLAFlaggedData;
    """
    
    analysis_df = pd.read_sql_query(mysql_analytical_query, conn)

    # ====================================================================
    # SUB-STEP D: SCIENTIFIC ROOT-CAUSE TESTING (One-Way ANOVA)
    # ====================================================================
    print("\n" + "="*60)
    print("🔬 RUNNING SCIENTIFIC ROOT-CAUSE ANALYSIS (ONE-WAY ANOVA)")
    print("="*60)
    
    groups = [
        analysis_df[analysis_df['risk_classification'] == tier]['delivery_time_deviation']
        for tier in ['Low Risk', 'Moderate Risk', 'High Risk']
    ]
    
    f_stat, p_value = stats.f_oneway(*groups)
    print(f"Calculated F-Statistic metric : {f_stat:.4f}")
    print(f"Calculated P-Value metrics     : {p_value:.6e}")
    
    if p_value < 0.05:
        print("\n🔥 STATUS: SIGNIFICANT OPERATIONAL BOTTLENECK VERIFIED.")
        print("Conclusion: Route variations across risk tiers are structural, not accidental.")
    else:
        print("\n⚖️ STATUS: RANDOM DISTRIBUTION DETECTED.")
        print("Conclusion: Delays are uniformly distributed across system assets.")
    print("="*60 + "\n")
    
    # Export clean datasets directly into your dashboard visualization directories
    analysis_df.to_csv('bi_dashboard_input.csv', index=False)
    print("[SUCCESS] Export data pipeline written cleanly to 'bi_dashboard_input.csv'.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    execute_mysql_analytics_pipeline()
