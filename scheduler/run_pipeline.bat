@echo off

REM Change directory to your TMDB pipeline folder
cd /d C:\Users\Subham Das\Desktop\data science\Capstone Projects\Imdb_movie_analysis


REM Activate the virtual environment
CALL .venv\Scripts\activate.bat

REM Run the ETL pipeline once
python -m src.main
