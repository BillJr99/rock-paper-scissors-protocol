def on_button_pressed_a():
    global my_id
    my_id += 1
    basic.show_number(my_id)
input.on_button_pressed(Button.A, on_button_pressed_a)

def check_play():
    global result
    basic.show_icon(IconNames.SURPRISED)
    if rps == opponent_rps:
        result = 2
    elif rps == 0 and opponent_rps == 2:
        result = 1
    elif rps == 1 and opponent_rps == 0:
        result = 1
    elif rps == 2 and opponent_rps == 1:
        result = 1
    else:
        result = 0
    if result == 1:
        basic.show_icon(IconNames.HAPPY)
    elif result == 2:
        basic.show_icon(IconNames.STICK_FIGURE)
    else:
        basic.show_icon(IconNames.SAD)

def on_button_pressed_ab():
    global protocol_state
    if protocol_state >= 2 and protocol_state < 5:
        radio.send_string("play" + " " + convert_to_text(sender) + " " + convert_to_text(my_id) + " " + convert_to_text(rps))
        if protocol_state == 4:
            basic.show_icon(IconNames.SQUARE)
            check_play()
            protocol_state = 5
        elif protocol_state < 5:
            basic.show_icon(IconNames.SMALL_SQUARE)
            protocol_state = 3
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_received_string(receivedString):
    global sender, protocol_state, age, opponent_rps
    if receivedString.includes("request"):
        if protocol_state == 0:
            sender = parse_float(receivedString.split(" ")[1])
            if sender != my_id:
                protocol_state = 1
                age = 0
                basic.show_icon(IconNames.EIGTH_NOTE)
                radio.send_string("response" + " " + convert_to_text(sender) + " " + convert_to_text(my_id))
    elif receivedString.includes("response"):
        if protocol_state == 0 and parse_float(receivedString.split(" ")[1]) == my_id:
            sender = parse_float(receivedString.split(" ")[2])
            if sender != my_id:
                protocol_state = 2
                age = 0
                basic.show_icon(IconNames.HEART)
                radio.send_string("acknowledge" + " " + convert_to_text(sender) + " " + convert_to_text(my_id))
    elif receivedString.includes("acknowledge"):
        basic.show_icon(IconNames.GHOST)
        if protocol_state == 1 and parse_float(receivedString.split(" ")[1]) == my_id and parse_float(receivedString.split(" ")[2]) == sender:
            protocol_state = 2
            age = 0
    elif receivedString.includes("play"):
        if protocol_state >= 2 and protocol_state < 5 and parse_float(receivedString.split(" ")[1]) == my_id and parse_float(receivedString.split(" ")[2]) == sender:
            basic.show_icon(IconNames.SWORD)
            opponent_rps = parse_float(receivedString.split(" ")[3])
            if protocol_state == 3:
                basic.show_icon(IconNames.SQUARE)
                check_play()
                protocol_state = 5
            else:
                basic.show_icon(IconNames.SMALL_SQUARE)
                protocol_state = 4
radio.on_received_string(on_received_string)

def on_button_pressed_b():
    global rps
    rps = (rps + 1) % 3
    if rps == 0:
        basic.show_icon(IconNames.SMALL_HEART)
    elif rps == 1:
        basic.show_icon(IconNames.CHESSBOARD)
    else:
        basic.show_icon(IconNames.SCISSORS)
input.on_button_pressed(Button.B, on_button_pressed_b)

def reset():
    global protocol_state, sender, rps, opponent_rps, result, age
    protocol_state = 0
    sender = 0
    rps = 0
    opponent_rps = 0
    result = 0
    age = 0
    basic.show_icon(IconNames.DIAMOND)
    basic.show_number(my_id)
age = 0
sender = 0
protocol_state = 0
result = 0
opponent_rps = 0
rps = 0
my_id = 0
radio.set_group(1)
my_id = 0
reset()

def on_forever():
    global age
    if protocol_state == 0:
        radio.send_string("request" + " " + convert_to_text(my_id))
    basic.pause(1000)
    if protocol_state <= 1:
        age = age + 1
        if age > 10:
            reset()
basic.forever(on_forever)
