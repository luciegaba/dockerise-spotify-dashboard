
#!/bin/bash


echo "WELCOME TO SPOTIFY DATA ANALYTICS LAUNCHER"
echo ""
echo "Let's check some config stuff"

#!/bin/bash
sudo yum install -y yum-utils
sudo yum-config-manager \
--add-repo \
https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl start docker

while [[ !  -f ".env" ]]; do
  echo "The .env file was not found in the current directory."
  read -p "Please add the .env file and press Enter to continue: "
done

echo "The .env file was found. Continuing with script execution."


if [[ -z "$CSV_OPTION" ]]; then
  read -p "Do you want to import CSV in case requesting too long or not possible (y/n)? " response

  if [[ "$response" = "y" ]]; then
    export CSV_OPTION="YES"
  else
    export CSV_OPTION="NO"
  fi

  echo "CSV_OPTION is set to $CSV_OPTION"

  # Append the exported variable to the .env file
  echo "CSV_OPTION=$CSV_OPTION" >> .env
fi

echo "Launching Docker-compose"

sudo docker compose -f "docker-compose.yml" up -d --build

echo "Done !"
echo ""
echo "Check docker ps to see if containers run"
echo "If there is problems, report logs "



