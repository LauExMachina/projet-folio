#!/bin/bash


send_mail(){            #Attention la fonction prend 3 paramètres
   
    subject=$1
    text=$2
    fichierDestinataire=$3

    while IFS= read -r adress; do           # Lecture de chaque ligne dans le fichier .txt

        if [[ -n "$adress" ]]; then
            
            echo -e "To: $adress\nSubject:$subject\n\n$text" | msmtp --from=default -t  # Pour chaque ligne envoie un mail
         
        else
            echo "Aucune adresse disponible dans le fichier"

        fi

        

    done < "$fichierDestinataire"       # Fichier cible
}


#main

send_mail "Alert" "Alerte déclenchée" "mailAdress.txt"      # Appel de la fonction et ses arguments



