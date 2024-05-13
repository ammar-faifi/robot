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
arduino = serial.Serial(port="/dev/ttyACM1", baudrate=9600, timeout=1)
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
                Button("Motor 1 CW", id="M1_CW"),
                Button("Motor 2 CW", id="M2_CW"),
                Button("Motor 3 CW", id="M3_CW"),
                Button("Motor 4 CW", id="M4_CW"),
                Button("Motor 5 CW", id="M5_CW"),
                Button("Motor 6 CW", id="M6_CW"),
                Button("Close gripper", id="M7_C"),
            ),
            VerticalScroll(
                Button("Motor 1 CCW", id="M1_CCW"),
                Button("Motor 2 CCW", id="M2_CCW"),
                Button("Motor 3 CCW", id="M3_CCW"),
                Button("Motor 4 CCW", id="M4_CCW"),
                Button("Motor 5 CCW", id="M5_CCW"),
                Button("Motor 6 CCW", id="M6_CCW"),
                Button("Open gripper", id="M7_O"),
            ),
            VerticalScroll(
                Button("Stop All Motors", id="stop_all", variant="error"),
                TextDisplay("Console..."),
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = str(event.button.id)
        text_display = self.query_one(TextDisplay)

        if button_id == "stop_all":
            text_display.update("Stopping all motors")
            for i in range(1, 7):
                send_command(f"M{i}STOP")

        elif button_id.startswith('M7_'):
            text_display.update("Gripper...")
            send_command(button_id.replace('_', ''))

        else:
            motor, dir = button_id.split("_")
            text_display.update(f"Rotating {motor} clockwise")
            if dir == 'CW':
                send_command(f"{motor},1000")
            else:
                send_command(f"{motor},-1000")


if __name__ == "__main__":
    app = MotorControl()
    app.run()
