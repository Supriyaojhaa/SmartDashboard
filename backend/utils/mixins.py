class LoggingMixin:

    def log(self, message):
        print(f"[LOG]: {message}")


class ExportMixin:

    def export_data(self, data):
        print("Exporting data...")
        return data