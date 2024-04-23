from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Horizontal, VerticalScroll

import serial
import time

motor_commands = {
    "x": ("M1", 0),
    "circle": ("M2", 1),
    "square": ("M3", 2),
    "triangle": ("M4", 3),
    "r2": ("M6", None),
    "l1": ("M7", 4),
    "r1": ("M5", 5),
    "l2": (None, 6),
}
# Setup Serial connection to Arduino (update port and baudrate according to your setup)
arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
time.sleep(0.5)  # Wait for the connection to establish


def send_command(command):
    arduino.write(f"{command}\n".encode())
    with open("logs.txt", "a") as file:
        file.write(f"{command}\n")


class TextDisplay(Static):
    """A widget to display text."""


class MotorControl(App):
    # CSS_PATH = "motor_control.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+c", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            VerticalScroll(
                Button("Motor 1 CW", id="motor1_cw", variant="primary"),
                Button("Motor 2 CW", id="motor2_cw", variant="primary"),
                Button("Motor 3 CW", id="motor3_cw", variant="primary"),
                Button("Motor 4 CW", id="motor4_cw", variant="primary"),
                Button("Motor 5 CW", id="motor5_cw", variant="primary"),
                Button("Motor 6 CW", id="motor6_cw", variant="primary"),
                Button("Close gripper", id="motor7_cw", variant="primary"),
            ),
            VerticalScroll(
                Button("Motor 1 CCW", id="motor1_ccw", variant="primary"),
                Button("Motor 2 CCW", id="motor2_ccw", variant="primary"),
                Button("Motor 3 CCW", id="motor3_ccw", variant="primary"),
                Button("Motor 4 CCW", id="motor4_ccw", variant="primary"),
                Button("Motor 5 CCW", id="motor5_ccw", variant="primary"),
                Button("Motor 6 CCW", id="motor6_ccw", variant="primary"),
                Button("Open gripper", id="motor7_ccw", variant="primary"),
            ),
            VerticalScroll(
                Button("Stop All Motors", id="stop_all", variant="error"),
                TextDisplay("Console..."),
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        text_display = self.query_one(TextDisplay)

        if button_id == "motor1_cw":
            text_display.update("Rotating Motor 1 clockwise")
            send_command("M1CW")
        elif button_id == "motor1_ccw":
            text_display.update("Rotating Motor 1 counterclockwise")
            send_command("M1CCW")
        elif button_id == "motor2_cw":
            text_display.update("Rotating Motor 2 clockwise")
            send_command("M2CW")
        elif button_id == "motor2_ccw":
            text_display.update("Rotating Motor 2 counterclockwise")
            send_command("M2CCW")
        elif button_id == "motor3_cw":
            text_display.update("Rotating Motor 3 clockwise")
            send_command("M3CW")
        elif button_id == "motor3_ccw":
            text_display.update("Rotating Motor 3 counterclockwise")
            send_command("M3CCW")
        elif button_id == "motor4_cw":
            text_display.update("Rotating Motor 4 clockwise")
            send_command("M4CW")
        elif button_id == "motor4_ccw":
            text_display.update("Rotating Motor 4 counterclockwise")
            send_command("M4CCW")
        elif button_id == "motor5_cw":
            text_display.update("Rotating Motor 5 clockwise")
            send_command("M5CW")
        elif button_id == "motor5_ccw":
            text_display.update("Rotating Motor 5 counterclockwise")
            send_command("M5CCW")
        elif button_id == "motor6_cw":
            text_display.update("Rotating Motor 6 clockwise")
            send_command("M6CW")
        elif button_id == "motor6_ccw":
            text_display.update("Rotating Motor 6 counterclockwise")
            send_command("M6CCW")
        elif button_id == "motor7_cw":
            text_display.update("Rotating Motor 7 clockwise")
            send_command("M7C")
        elif button_id == "motor7_ccw":
            text_display.update("Rotating Motor 7 counterclockwise")
            send_command("M7O")
        elif button_id == "stop_all":
            text_display.update("Stopping all motors")
            for i in range(1, 7):
                send_command(f"M{i}STOP")


if __name__ == "__main__":
    app = MotorControl()
    app.run()
