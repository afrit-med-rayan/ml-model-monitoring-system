import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

class ModelMonitor:
    def __init__(self):
        # Initialize the report with DataDriftPreset
        self.report = Report(metrics=[DataDriftPreset()])

    def detect_data_drift(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping=None):
        """
        Runs the data drift detection.
        
        Args:
            reference_data (pd.DataFrame): The reference dataset (e.g., training data).
            current_data (pd.DataFrame): The current dataset (e.g., production data).
            column_mapping (ValidationColumnMapping, optional): Column mapping for Evidently.
        """
        self.report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)

    def save_report(self, filepath: str):
        """
        Saves the generated report to an HTML file.
        
        Args:
            filepath (str): The path to save the HTML report.
        """
        self.report.save_html(filepath)
