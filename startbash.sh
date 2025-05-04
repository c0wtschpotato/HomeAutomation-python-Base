
#!/bin/bash
# usefull to start scripts in screen for later use
sleep 5
source remote/bin/activate
python3 HomeAutomation-python-Base/remote_machine.py
#### komplette bashline für screen \n = ENTER
###screen -S remote -X stuff 'cd HomeAutomation-python-Base/\nsource remote/bin/activate\npython remote_machine.py\n'