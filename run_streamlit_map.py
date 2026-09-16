import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from streamlit.web import cli as stcli
sys.argv = ["streamlit", "run", "visualizations/raster/app.py",
            "--server.headless", "true", "--server.port", "8501",
            "--browser.gatherUsageStats", "false"]
stcli.main()
