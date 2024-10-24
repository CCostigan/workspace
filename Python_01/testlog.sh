
find . -name "*.log" -exec rm {} \;

#input "Press enter"

watch -n 0.1 python3 src/ZTest.py 
