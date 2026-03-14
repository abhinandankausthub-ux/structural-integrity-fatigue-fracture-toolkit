@echo off

cd %USERPROFILE%\Documents\engineering_portfolio\Engineering_Analysis_ToolKit

echo Checking required Python packages...

python -c "import streamlit, numpy, matplotlib, reportlab, rainflow" 2>NUL

IF %ERRORLEVEL% NEQ 0 (
    echo Missing packages detected. Installing requirements...
    python -m pip install -r requirements.txt
) ELSE (
    echo All required packages already installed.
)

echo Launching Structural Integrity Toolkit...
streamlit run app.py

pause