@echo on
call C:\Users\bmsha\Anaconda3\Scripts\activate.bat
call activate rasapy38
call rasa run -m models --enable-api --cors "*" -p 5006
pause