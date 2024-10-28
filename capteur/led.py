from gpiozero import LED
from time import sleep


def led():

    led = LED(23)

    count = 0

    try:
        while count < 5:
            led.on()
            sleep(1)
            led.off()
            sleep(1)

            count += 1

    except Exception as e : 
        print(f"Erreur : {e}")


if __name__ == "__main__":
    led()
