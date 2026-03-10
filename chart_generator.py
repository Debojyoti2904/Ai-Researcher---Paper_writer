import matplotlib.pyplot as plt
from langchain_core.tools import tool
from pathlib import Path

# -------------------------------
# Project paths
# -------------------------------
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "output"

@tool
def generate_chart(
    title: str, 
    x_label: str, 
    y_label: str, 
    x_data: list[str], 
    y_data: list[float], 
    filename: str, 
    chart_type: str = "bar"
) -> str:
    """
    Generates a chart and saves it as a PNG image for use in LaTeX.
    
    Args:
        title: The title of the chart.
        x_label: Label for the X axis.
        y_label: Label for the Y axis.
        x_data: List of strings for the X axis categories.
        y_data: List of numbers for the Y axis values.
        filename: Name of the file (e.g., 'accuracy_plot.png'). MUST end in .png.
        chart_type: The type of chart ('bar' or 'line').
        
    Returns:
        str: A success message with instructions for LaTeX, or an error message.
    """
    try:
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        # Ensure the filename ends with .png
        if not filename.endswith(".png"):
            filename += ".png"
            
        filepath = OUTPUT_DIR / filename
        
        # Clear any existing plots in memory
        plt.clf()
        plt.figure(figsize=(8, 5))
        
        # Draw the requested chart type
        if chart_type == "line":
            plt.plot(x_data, y_data, marker='o', linestyle='-', color='b')
        else:
            plt.bar(x_data, y_data, color='skyblue')
            
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        # Save the file to the output directory
        plt.savefig(filepath)
        plt.close()
        
        return (
            f"Success! Chart saved as {filename}. "
            f"You can now include it in your LaTeX code using \\includegraphics{{{filename}}}."
        )
        
    except Exception as e:
        # Return the error to the AI so it can fix its data
        return f"Chart Generation Failed. Error: {str(e)}. Check your data arrays and try again."