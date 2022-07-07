input.onButtonPressed(Button.A, function () {
    my_id += 1
    basic.showNumber(my_id)
})
function check_play () {
    basic.showIcon(IconNames.Surprised)
    if (rps == opponent_rps) {
        result = 2
    } else if (rps == 0 && opponent_rps == 2) {
        result = 1
    } else if (rps == 1 && opponent_rps == 0) {
        result = 1
    } else if (rps == 2 && opponent_rps == 1) {
        result = 1
    } else {
        result = 0
    }
    if (result == 1) {
        basic.showIcon(IconNames.Happy)
    } else if (result == 2) {
        basic.showIcon(IconNames.StickFigure)
    } else {
        basic.showIcon(IconNames.Sad)
    }
}
input.onButtonPressed(Button.AB, function () {
    if (protocol_state >= 2 && protocol_state < 5) {
        radio.sendString("play" + " " + convertToText(sender) + " " + convertToText(my_id) + " " + convertToText(rps))
        if (protocol_state == 4) {
            basic.showIcon(IconNames.Square)
            check_play()
            protocol_state = 5
        } else if (protocol_state < 5) {
            basic.showIcon(IconNames.SmallSquare)
            protocol_state = 3
        }
    }
})
radio.onReceivedString(function (receivedString) {
    if (receivedString.includes("request")) {
        if (protocol_state == 0) {
            sender = parseFloat(_py.py_string_split(receivedString, " ")[1])
            if (sender != my_id) {
                protocol_state = 1
                age = 0
                basic.showIcon(IconNames.EigthNote)
                radio.sendString("response" + " " + convertToText(sender) + " " + convertToText(my_id))
            }
        }
    } else if (receivedString.includes("response")) {
        if (protocol_state == 0 && parseFloat(_py.py_string_split(receivedString, " ")[1]) == my_id) {
            sender = parseFloat(_py.py_string_split(receivedString, " ")[2])
            if (sender != my_id) {
                protocol_state = 2
                age = 0
                basic.showIcon(IconNames.Heart)
                radio.sendString("acknowledge" + " " + convertToText(sender) + " " + convertToText(my_id))
            }
        }
    } else if (receivedString.includes("acknowledge")) {
        basic.showIcon(IconNames.Ghost)
        if (protocol_state == 1 && parseFloat(_py.py_string_split(receivedString, " ")[1]) == my_id && parseFloat(_py.py_string_split(receivedString, " ")[2]) == sender) {
            protocol_state = 2
            age = 0
        }
    } else if (receivedString.includes("play")) {
        if (protocol_state >= 2 && protocol_state < 5 && parseFloat(_py.py_string_split(receivedString, " ")[1]) == my_id && parseFloat(_py.py_string_split(receivedString, " ")[2]) == sender) {
            basic.showIcon(IconNames.Sword)
            opponent_rps = parseFloat(_py.py_string_split(receivedString, " ")[3])
            if (protocol_state == 3) {
                basic.showIcon(IconNames.Square)
                check_play()
                protocol_state = 5
            } else {
                basic.showIcon(IconNames.SmallSquare)
                protocol_state = 4
            }
        }
    }
})
input.onButtonPressed(Button.B, function () {
    rps = (rps + 1) % 3
    if (rps == 0) {
        basic.showIcon(IconNames.SmallHeart)
    } else if (rps == 1) {
        basic.showIcon(IconNames.Chessboard)
    } else {
        basic.showIcon(IconNames.Scissors)
    }
})
function reset () {
    protocol_state = 0
    sender = 0
    rps = 0
    opponent_rps = 0
    result = 0
    age = 0
    basic.showIcon(IconNames.Diamond)
    basic.showNumber(my_id)
}
let age = 0
let sender = 0
let protocol_state = 0
let result = 0
let opponent_rps = 0
let rps = 0
let my_id = 0
radio.setGroup(1)
my_id = 0
reset()
basic.forever(function () {
    if (protocol_state == 0) {
        radio.sendString("request" + " " + convertToText(my_id))
    }
    basic.pause(1000)
    if (protocol_state <= 1) {
        age = age + 1
        if (age > 10) {
            reset()
        }
    }
})
