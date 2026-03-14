import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import re
from sklearn.linear_model import LinearRegression
from datetime import timedelta

def parse_vibration_file(filepath):
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        date_str = ""
        for line in lines[:10]:
            if "Date/Time:" in line:
                date_str = re.search(r'(\d{2}-\w{3}-\d{2})', line).group(1)
                break
        raw_data = pd.read_csv(filepath, skiprows=8, sep='\s+', header=None)
        amplitudes = pd.concat([raw_data[1], raw_data[3], raw_data[5], raw_data[7]]).dropna()
        rms = np.sqrt(np.mean(np.square(amplitudes)))
        return date_str, rms
    except:
        return None, None

def main():
    files = glob.glob("data/*.txt")
    if not files: return print("No data found in data/ folder")

    results = []
    for f in files:
        category = "Cooling Pump" if "Cooling" in f else "Motor Compressor"
        date, rms = parse_vibration_file(f)
        if date:
            results.append({'Machine': category, 'Date': pd.to_datetime(date), 'RMS': rms})

    df = pd.DataFrame(results).sort_values('Date')

    # --- Predictive Part: Linear Regression ---
    THRESHOLD = 0.5  # สมมติว่าค่า RMS เกิน 0.5 G คืออันตราย
    
    plt.figure(figsize=(12, 7))
    
    for machine in df['Machine'].unique():
        m_data = df[df['Machine'] == machine].copy()
        
        # แปลงวันที่เป็นตัวเลข (จำนวนวันนับจากจุดเริ่มต้น) เพื่อเข้าโมเดล
        start_date = m_data['Date'].min()
        m_data['Days'] = (m_data['Date'] - start_date).dt.days
        
        X = m_data[['Days']].values
        y = m_data['RMS'].values
        
        # สร้างและเทรนโมเดล Linear Regression
        model = LinearRegression()
        model.fit(X, y)
        
        # พยากรณ์ไปข้างหน้าอีก 90 วัน
        future_days = np.array([[i] for i in range(0, 150)])
        future_rms = model.predict(future_days)
        future_dates = [start_date + timedelta(days=int(i)) for i in future_days.flatten()]
        
        # พล็อตข้อมูลจริง
        plt.scatter(m_data['Date'], m_data['RMS'], label=f'{machine} (Actual)')
        # พล็อตเส้นพยากรณ์
        plt.plot(future_dates, future_rms, '--', alpha=0.6, label=f'{machine} (Trend)')

    plt.axhline(y=THRESHOLD, color='r', linestyle='-', label='Danger Threshold (0.5G)')
    plt.title('Predictive Maintenance: Vibration Trend Forecasting')
    plt.ylabel('Vibration RMS (G)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('prediction_plot.png')
    plt.show()

    print("Model Training Complete. Visualization saved as 'prediction_plot.png'")

if __name__ == "__main__":
    main()