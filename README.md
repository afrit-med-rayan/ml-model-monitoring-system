# ML Model Monitoring System

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)](https://grafana.com/)
[![Evidently AI](https://img.shields.io/badge/Evidently%20AI-4D4D4D?style=for-the-badge)](https://www.evidentlyai.com/)

An end-to-end Machine Learning model monitoring system that tracks data drift, prediction drift, and classification performance. Built with FastAPI, Evidently AI, Prometheus, and Grafana.

## 🚀 Features

- **Real-time Inference**: FastAPI-based endpoint for model predictions.
- **Monitoring Suite**: Integrated Evidently AI for deep analysis of data and model health.
- **Observability**: Prometheus metrics export and Grafana dashboards for visualization.
- **Alerting**: Threshold-based alerts for drift and accuracy degradation.
- **Dockerized**: Easy deployment using Docker and Docker Compose.
- **Simulation Scripts**: Tools to simulate data drift and performance degradation for testing.

## 🏗️ Architecture

The system consists of an API service, a monitoring engine, and an observability stack.

- **FastAPI**: Serves the model and exposes metrics.
- **Evidently AI**: Generates PDF/HTML reports on data and model drift.
- **Prometheus**: Collects and stores performance metrics.
- **Grafana**: Visualizes metrics and alerts.

For more details, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 🛠️ Installation & Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (if running locally)

### Using Docker (Recommended)
1. **Clone the repository**:
   ```bash
   git clone https://github.com/afrit-med-rayan/ml-model-monitoring-system.git
   cd ml-model-monitoring-system
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access the Services**:
   - **API**: [http://localhost:8000](http://localhost:8000)
   - **Prometheus**: [http://localhost:9090](http://localhost:9090)
   - **Grafana**: [http://localhost:3000](http://localhost:3000) (Default Login: `admin`/`admin`)

## 📖 Usage

### API Endpoints
- `POST /predict`: Submit features for model prediction.
- `POST /monitoring/run`: Manually trigger a monitoring report.
- `GET /reports/latest`: Download the latest monitoring report.

See [API.md](docs/API.md) for full documentation.

### Simulating Drift
To test the monitoring capabilities, use the provided simulation scripts:
```bash
# Simulate data drift
python src/scripts/simulate_drift.py

# Simulate performance degradation
python src/scripts/simulate_performance.py
```

## 📊 Dashboards
The Grafana dashboard is pre-configured to show:
- **Data Drift Score**: Tracks shifts in input feature distributions.
- **Model Accuracy**: Monitors real-time classification performance.
- **Prediction Volume**: Tracks the number of requests over time.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
