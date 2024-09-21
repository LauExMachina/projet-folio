import RPi.GPIO as GPIO
import time



def led():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)

    try:
        count = 0
       
        while count < 5:
            
            
            GPIO.output(17, GPIO.HIGH)     # Led alimentée
            time.sleep(1)                  #Système en pause 1s
            GPIO.output(17, GPIO.LOW)      # Led non alimentée
            time.sleep(1)

            count += 1                     # Incrémentation du tour de boucle
        
    except Exception as e:
        print("Erreur rencontrée : {e}")

    finally:
        
        GPIO.cleanup()                     # Nettoyage du GPIO en sortie
