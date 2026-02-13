import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, ClassificationPreset

class ModelMonitor:
    def __init__(self):
        self.report = None

    def detect_data_drift(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping=None):
        """
        Runs the data drift detection.
        """
        self.report = Report(metrics=[DataDriftPreset()])
        self.report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)

    def detect_prediction_drift(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping=None):
        """
        Runs the prediction (target) drift detection.
        """
        self.report = Report(metrics=[TargetDriftPreset()])
        self.report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)

    def detect_performance_drift(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping=None):
        """
        Runs the classification performance monitoring.
        """
        self.report = Report(metrics=[ClassificationPreset()])
        self.report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)

    def run_full_suite(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping=None):
        """
        Runs a full suite of monitoring metrics.
        """
        self.report = Report(metrics=[
            DataDriftPreset(),
            TargetDriftPreset(),
            ClassificationPreset()
        ])
        self.report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)

    def save_report(self, filepath: str):
        """
        Saves the generated report to an HTML file.
        
        Args:
            filepath (str): The path to save the HTML report.
        """
        self.report.save_html(filepath)
