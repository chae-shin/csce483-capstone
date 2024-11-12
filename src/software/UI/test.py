import mido
with mido.open_input('Midi Through:Midi Through Port-0 14:0') as input_port:
    for msg in input_port:
        print(msg)
    