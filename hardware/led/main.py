import subprocess
import threading

# Paths to the scripts
midi2led_script = "/home/capstone/csce483-capstone/hardware/led/MIDI2LED_rijul.py"
midi_lcd_script = "/home/capstone/csce483-capstone/hardware/lcd/midi_lcd_test.py"

def run_script(script_path):
    subprocess.run(["python", script_path])

# Create threads for each script
thread1 = threading.Thread(target=run_script, args=(midi2led_script,))
thread2 = threading.Thread(target=run_script, args=(midi_lcd_script,))

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()