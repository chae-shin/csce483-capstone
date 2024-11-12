import mido
import time
import pretty_midi
import threading

ime = time.time()
start_time = None  # Record the start time
end_time = None
note_times = {}  # Dictionary to store note start times

userSong = pretty_midi.PrettyMIDI()
piano = pretty_midi.Instrument(program=0)

# Flag to stop the listening loop
stop_flag = threading.Event()

def listen_to_midi(input_port):
    global start_time, end_time, note_times
    print("Listening to MIDI input...")
    try:
        for msg in input_port:
            if stop_flag.is_set():
                break  # Exit the loop if stop flag is set

            if str(msg.type) == "clock":
                continue  # Skip processing if clock time is 0

            print(f"Note: {msg.note}" if hasattr(msg, 'note') else "No Note")
            print(f"Velocity: {msg.velocity}" if hasattr(msg, 'velocity') else "No Velocity")
            print("-" * 20)

            if str(msg.type) == 'note_on' and int(msg.velocity) > 0:  # Note On (key pressed)
                if start_time is None:
                    start_time = time.time()-ime  # Record start time for the song
                note_times[int(msg.note)-36] = time.time()  # Record start time for the note
                print(f"Note {int(msg.note)-36} started")
                noteTime = time.time() - ime
                print("Note played at : ", noteTime)

            if (int(msg.velocity) == 0):  # Note Off (key released)
                if int(msg.note)-36 in note_times:
                    duration = time.time() - note_times[int(msg.note)-36]  # Calculate duration
                    print(f"Note {int(msg.note)-36} ended, duration: {duration:.3f} seconds")
                    del note_times[int(msg.note)-36]  # Remove the note from the dictionary
                    end_time = time.time()-ime
                    # print("NEEE:",msg.note)
                    note = pretty_midi.Note(velocity=80, pitch=(msg.note), start=end_time-duration, end=end_time)
                    piano.notes.append(note)


    except TimeoutError:
        print("No messages received in the last second...")

# Function to start listening in a separate thread
def start_listening():
    with mido.open_input('USB MIDI Interface:USB MIDI Interface MIDI 1 28:0') as input_port:
        listen_to_midi(input_port)

# Start the listening thread
listener_thread = threading.Thread(target=start_listening)
listener_thread.start()

# Handle keyboard interrupt gracefully
try:
    while listener_thread.is_alive():
        listener_thread.join(timeout=1)  # Keep checking the thread status
except KeyboardInterrupt:
    print("Stopped listening.")
    stop_flag.set()  # Set the stop flag to break the loop in the listener thread
    listener_thread.join()  # Wait for the listener thread to finish

    if start_time and end_time:
        total_duration = end_time - start_time
        print(f"Total song duration: {total_duration:.3f} seconds")
        userSong.instruments.append(piano)
        userSong.write('UserInputRecorded/user.mid')
