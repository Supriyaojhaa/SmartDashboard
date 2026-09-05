import pandas as pd
import numpy as np
import os
import matplotlib

# CORE LIBRARIES
import datetime
import math
import sys

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from utils.decorators import log_function, timer
from utils.generators import data_generator, multiplier
from utils.iterators import DatasetIterator
from modules.serialization import save_results
from modules.base_processor import BaseProcessor
from utils.mixins import LoggingMixin, ExportMixin


def apply_theme(fig, ax, title, xlabel, ylabel):
    """Applies modern dark-glassmorphism theme matching the dashboard UI."""
    fig.patch.set_facecolor("#0b0f19")
    ax.set_facecolor("#111827")

    # Title styling with clean modern font & padding
    ax.set_title(title, color="#f8fafc", fontsize=11, fontweight="bold", pad=12)

    # Axis labels with muted slate color
    ax.set_xlabel(xlabel, color="#94a3b8", fontsize=9.5, fontweight="600", labelpad=8)
    ax.set_ylabel(ylabel, color="#94a3b8", fontsize=9.5, fontweight="600", labelpad=8)

    # Ticks styling
    ax.tick_params(colors="#94a3b8", labelsize=8.5, width=0.8)

    # Spines (borders) - remove top and right for clean modern look
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_color("#1f293d")
        ax.spines[spine].set_linewidth(0.8)

    # Subtle modern grid
    ax.grid(True, linestyle="--", alpha=0.25, color="#334155")
    ax.set_axisbelow(True)


class AdvancedProcessor(BaseProcessor, LoggingMixin, ExportMixin): 
    def process(self, data):
        self.log("Processing dataset using AdvancedProcessor")
        return self.export_data(data)

@log_function
@timer
def process_dataset(filepath):

    # ERROR HANDLING
    try:
        fp_lower = filepath.lower()
        if fp_lower.endswith(".csv"):
            try:
                df = pd.read_csv(filepath)
            except pd.errors.ParserError:
                df = pd.read_csv(filepath, on_bad_lines="skip")
        elif fp_lower.endswith(".json"):
            df = pd.read_json(filepath)
        else:
            return None
    except Exception as e:
        print("Error reading file:", e)
        return None

    stats = {}

    numeric_columns = df.select_dtypes(include=np.number).columns

    data = df.values.tolist()

    # Generator usage - only numeric columns
    numeric_df = df[numeric_columns]
    numeric_data = numeric_df.values.tolist()
    
    column_sums = {}
    column_counts = {}
    
    for column in numeric_columns:
        column_sums[column] = 0
        column_counts[column] = 0

    for row in data_generator(numeric_data):
        for i, column in enumerate(numeric_columns):
            column_sums[column] += row[i]
            column_counts[column] += 1

    # Closure
    double = multiplier(2)

    # CORE LIBRARY USAGE
    print("Processing Time:", datetime.datetime.now())
    print("Python Version:", sys.version)
    print("Square root demo:", math.sqrt(16))

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    charts_folder = os.path.join(BASE_DIR, "../../frontend/static/charts")

    os.makedirs(charts_folder, exist_ok=True)

    for file in os.listdir(charts_folder):
        os.remove(os.path.join(charts_folder, file))

    for column in numeric_columns:

        valid_series = df[column].dropna()
        if len(valid_series) == 0:
            continue

        mean_value = (column_sums[column] / column_counts[column]) if column_counts[column] > 0 else 0.0
        med_value = df[column].median()
        std_value = df[column].std()

        stats[column] = {
            "mean": float(mean_value) if not pd.isna(mean_value) else 0.0,
            "median": float(med_value) if not pd.isna(med_value) else 0.0,
            "std": float(std_value) if not pd.isna(std_value) else 0.0
        }

        # Closure usage
        doubled_mean = double(mean_value)

        try:
            col_label = column.replace('_', ' ').title()

            # LINE GRAPH - Modern gradient line with markers and glow fill
            fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=140)
            apply_theme(fig, ax, f"{col_label} - Trend Line", "Record Index", col_label)
            
            x_vals = range(len(df[column]))
            y_vals = df[column].values
            
            ax.plot(x_vals, y_vals, color="#818cf8", linewidth=3.5, alpha=0.25)
            ax.plot(x_vals, y_vals, color="#6366f1", linewidth=2, marker="o", markersize=4,
                    markerfacecolor="#38bdf8", markeredgecolor="#ffffff", markeredgewidth=1)
            ax.fill_between(x_vals, y_vals, color="#6366f1", alpha=0.15)
            
            plt.tight_layout()
            plt.savefig(os.path.join(charts_folder, f"{column}_line.png"), facecolor=fig.get_facecolor(), edgecolor="none")
            plt.close(fig)

            # BAR GRAPH - Cyan modern bar chart
            fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=140)
            apply_theme(fig, ax, f"{col_label} - Bar Comparison", "Record Index", col_label)
            
            x_indices = range(len(df[column]))
            ax.bar(x_indices, y_vals, color="#06b6d4", edgecolor="#38bdf8", linewidth=0.8, width=0.62, alpha=0.88)
            
            if len(x_indices) > 12:
                step = max(1, len(x_indices) // 8)
                ax.set_xticks(list(x_indices)[::step])
                
            plt.tight_layout()
            plt.savefig(os.path.join(charts_folder, f"{column}_bar.png"), facecolor=fig.get_facecolor(), edgecolor="none")
            plt.close(fig)

            # HISTOGRAM - Purple distribution with mean reference line
            fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=140)
            apply_theme(fig, ax, f"{col_label} - Distribution Spread", col_label, "Frequency")
            
            n, bins, patches = ax.hist(valid_series, bins=10, color="#8b5cf6", edgecolor="#c084fc", linewidth=1, alpha=0.85, rwidth=0.85)
            
            mean_val = float(mean_value)
            ax.axvline(mean_val, color="#34d399", linestyle="--", linewidth=1.6, label=f"Mean: {mean_val:.1f}")
            ax.legend(facecolor="#111827", edgecolor="#1f293d", labelcolor="#f8fafc", fontsize=8.5, loc="upper right")
            
            plt.tight_layout()
            plt.savefig(os.path.join(charts_folder, f"{column}_hist.png"), facecolor=fig.get_facecolor(), edgecolor="none")
            plt.close(fig)

        except Exception as pe:
            print(f"Error plotting chart for {column}:", pe)
            plt.close()

    # Iterator usage
    iterator = DatasetIterator(data)
    for _ in iterator:
        pass

    print(iterator)       
    print(len(iterator)) 

    # Mixins + Abstract Class
    processor = AdvancedProcessor()
    processor.process(stats)

    # JSON storage
    save_results(stats)

    return stats


# CUSTOM CHART GENERATION
def generate_custom_charts(filepath, x_col, y_col):
    return generate_column_chart(filepath, x_col, y_col)


def generate_column_chart(filepath, x_col, y_col):
    filepath = filepath.replace("/", "\\")

    fp_lower = filepath.lower()
    try:
        if fp_lower.endswith(".csv"):
            try:
                df = pd.read_csv(filepath)
            except pd.errors.ParserError:
                df = pd.read_csv(filepath, on_bad_lines="skip")
        elif fp_lower.endswith(".json"):
            df = pd.read_json(filepath)
        else:
            return None
    except Exception:
        return None

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    charts_folder = os.path.join(BASE_DIR, "../../frontend/static/charts")
    os.makedirs(charts_folder, exist_ok=True)

    x_labels = df[x_col].astype(str).tolist()
    y_vals = pd.to_numeric(df[y_col], errors="coerce").fillna(0).values
    x_indices = range(len(x_labels))

    x_title = x_col.replace('_', ' ').title()
    y_title = y_col.replace('_', ' ').title()

    # LINE GRAPH with custom axes
    fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=140)
    apply_theme(fig, ax, f"{y_title} vs {x_title} (Line)", x_title, y_title)
    
    ax.plot(x_indices, y_vals, color="#818cf8", linewidth=3.5, alpha=0.25)
    ax.plot(x_indices, y_vals, color="#6366f1", linewidth=2, marker="o", markersize=4.5,
            markerfacecolor="#38bdf8", markeredgecolor="#ffffff", markeredgewidth=1)
    ax.fill_between(x_indices, y_vals, color="#6366f1", alpha=0.15)
    
    if len(x_indices) > 15:
        step = max(1, len(x_indices) // 10)
        ax.set_xticks(list(x_indices)[::step])
        ax.set_xticklabels(x_labels[::step], rotation=35, ha="right", color="#94a3b8", fontsize=8)
    else:
        ax.set_xticks(list(x_indices))
        ax.set_xticklabels(x_labels, rotation=35, ha="right", color="#94a3b8", fontsize=8)

    plt.tight_layout()
    line_path = f"{y_col}_custom_line.png"
    plt.savefig(os.path.join(charts_folder, line_path), facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)

    # BAR GRAPH with custom axes
    fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=140)
    apply_theme(fig, ax, f"{y_title} vs {x_title} (Bar)", x_title, y_title)
    
    ax.bar(x_indices, y_vals, color="#06b6d4", edgecolor="#38bdf8", linewidth=0.8, width=0.62, alpha=0.88)
    
    if len(x_indices) > 15:
        step = max(1, len(x_indices) // 10)
        ax.set_xticks(list(x_indices)[::step])
        ax.set_xticklabels(x_labels[::step], rotation=35, ha="right", color="#94a3b8", fontsize=8)
    else:
        ax.set_xticks(list(x_indices))
        ax.set_xticklabels(x_labels, rotation=35, ha="right", color="#94a3b8", fontsize=8)

    plt.tight_layout()
    bar_path = f"{y_col}_custom_bar.png"
    plt.savefig(os.path.join(charts_folder, bar_path), facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)

    return {
        "line": f"/static/charts/{line_path}",
        "bar": f"/static/charts/{bar_path}"
    }
