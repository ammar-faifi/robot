import pygame
import serial
import time

# Initialize Pygame and the joystick
pygame.init()
pygame.joystick.init()
print(f"number of joysticks connected: {pygame.joystick.get_count()}")
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Setup Serial connection to Arduino (update port and baudrate according to your setup)
arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
time.sleep(0.5)  # Wait for the connection to establish


def send_command(command):
    arduino.write(f"{command}\n".encode())
    print(f"Sent: {command}")


def read_serial():
    pass
    # if arduino.in_waiting > 0:
    #     line = arduino.readline()  # Read a line from the serial port
    #     if line.decode('utf-8').strip():  # If there is data
    #         print("arduino", line.decode('utf-8').strip())


def main():
    running = True
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

    while running:
        for event in pygame.event.get():
            read_serial()
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYHATMOTION:
                # Check for motor selection buttons
                for button, (motor, btn_id) in motor_commands.items():
                    if joystick.get_button(btn_id):
                        # if button == "r2"
                        # dpad = joystick.get_hat(0)
                        # if dpad == (0, 1):
                        #     send_command("M7O")
                        #     # print("M7O")
                        # elif dpad == (0, -1):
                        #     send_command("M7C")
                        # print("M7C")
                        if (
                            joystick.get_hat(0) == (1, 0) or joystick.get_axis(0) > 0.5
                        ):  # Right
                            if motor == "M7":
                                send_command("M7C")
                            else:
                                send_command(f"{motor}CW")
                            # print(f"{motor}CW")
                        elif (
                            joystick.get_hat(0) == (-1, 0)
                            or joystick.get_axis(0) < -0.5
                        ):  # Left
                            if motor == "M7":
                                send_command("M7O")
                            else:
                                send_command(f"{motor}CCW")
                            # print(f"{motor}CCW")

                # Check if L2 is pressed to stop all motors
                if joystick.get_button(6):
                    send_command("M7S")
                    for i in range(1, 7):
                        send_command(f"M{i}STOP")

            if event.type == pygame.JOYBUTTONUP:
                # If any button is released, send a stop command to all motors
                for _, btn_id in motor_commands.values():
                    if event.button == (btn_id):
                        send_command("M7S")
                        for i in range(1, 7):
                            send_command(
                                f"M{i}STOP"
                            )  # Assumes Arduino code can handle "MxSTOP" to stop motors

            # time.sleep(0.1)  # Slight delay to prevent sending too many commands


if __name__ == "__main__":
    main()
