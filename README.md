# 🌱 Crop Growing Degree Days (GDD) Dataset

This project provides a structured and queryable dataset of crop temperature thresholds and Growing Degree Days (GDD), based on FAO guidelines.

---

## 📊 Features

- FAO-based crop dataset  
- Temperature thresholds:
  - Base temperature (`T_base`)
  - Upper temperature (`T_upper`)  
- Growing Degree Days (GDD)  
- Multi-variant support:
  - seasonal (short/long)
  - production type (e.g. ratoon, virgin)
  - growth cycle (1st year, 2nd year)
- Notes for non-exact matches (genus-level, inferred data)  
- Query-ready JSON structure  
- Python CLI tool for searching and filtering  

---

## 📁 Project Structure
├── crops_query.json # Main dataset
├── crops_query.py # Query script (CLI tool)


---

## 🚀 Usage

### Run the query script

```bash
python crops_query.py tomato

Example Output
🌱 Tomato
Scientific name: Solanum lycopersicum

GDD variants:
  - industry: 1900 °C
  - market: 2065 °C
🔍 Search Examples
python crops_query.py mint
python crops_query.py sorghum
python crops_query.py citrus
📚 Source

FAO (2025) – Crop Evapotranspiration: Guidelines for Computing Crop Water Requirements
Table 6.10 (p. 204)

📄 License
Code: MIT License
Data: Crop evapotranspiration: Guidelines for computing crop water requirements
(FAO Irrigation and Drainage Paper No. 56, Rev. 1), Table 6.10, p. 204 — CC BY 4.0
