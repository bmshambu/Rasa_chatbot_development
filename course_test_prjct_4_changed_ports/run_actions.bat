@echo on
call C:\Users\bmsha\Anaconda3\Scripts\activate.bat
call activate rasapy38
call rasa run actions --port 5056
pause