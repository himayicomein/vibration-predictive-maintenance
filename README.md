# Predictive Maintenance Project (Vibration Analysis)

โปรเจคนี้ใช้สำหรับวิเคราะห์แนวโน้มสุขภาพของเครื่องจักร (Condition Monitoring) โดยใช้ข้อมูลความสั่นสะเทือน (Vibration Data) จากไฟล์ตาราง Waveform Amplitudes

## วัตถุประสงค์
- เพื่อคำนวณค่าพลังงานความสั่นสะเทือน (RMS) จากไฟล์เครื่องจักร
- เพื่อเปรียบเทียบแนวโน้ม (Trend) ความสั่นสะเทือนในแต่ละเดือน (Jun, Sep, Oct 2024)
- เพื่อแจ้งเตือนก่อนที่เครื่องจักรจะเกิดความเสียหาย

## โครงสร้างโปรเจค
- `data/`: เก็บไฟล์ .txt ของ Cooling Pump และ Motor Compressor
- `analysis.py`: สคริปต์หลักในการคำนวณและสร้างกราฟ
- `requirements.txt`: รายชื่อ Library ที่จำเป็น

## วิธีรันโปรเจค
1. ติดตั้ง Library: `pip install -r requirements.txt`
2. รันโปรแกรม: `python analysis.py`

## Analysis Result
![Vibration Prediction Plot](prediction_plot.png)