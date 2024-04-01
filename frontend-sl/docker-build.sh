#!/bin/bash
PROJECT=thienenkapp-mkpasswd-001

echo "Build and push a new image"
CURRENT_VERSION=$(gcloud run services describe mkpasswd --region europe-west1 --project ${PROJECT} --format json | jq '.spec.template.spec.containers[0].image' | sed 's/.*app_name:v\([^:][0-9]*\).*/\1/')
NEW_VERSION=$((CURRENT_VERSION + 1))
echo "Found version ${CURRENT_VERSION}"
echo "New version ${NEW_VERSION}"

# Function to validate user input
function validate_input() {
  local input="$1"
  if [[ "$input" =~ ^(yes|no|abort)$ ]]; then
    return 0  # Valid input
  else
    return 1  # Invalid input
  fi
}

# Main loop for user input
while true; do
  read -p "Do you want to continue (yes/no/abort)? " user_input

  # Validate user input
  if validate_input "$user_input"; then
    break  # Exit loop on valid input
  else
    echo "Invalid input. Please enter yes, no, or abort."
  fi
done

# Handle user choice
case "$user_input" in
  yes)
    echo "Continuing..."
    # Add your code for actions if user enters "yes"
    docker build -t europe-west1-docker.pkg.dev/${PROJECT}/mkpasswd-frontend/app_name:v${NEW_VERSION} .
    docker push     europe-west1-docker.pkg.dev/${PROJECT}/mkpasswd-frontend/app_name:v${NEW_VERSION}

    gcloud run services update mkpasswd --image=europe-west1-docker.pkg.dev/${PROJECT}/mkpasswd-frontend/app_name:v${NEW_VERSION}  --region europe-west1 --project thienenkapp-mkpasswd-001
    ;;
  no)
    echo "Exiting..."
    # Add your code for actions if user enters "no"
    exit 0  # Exit script with success code
    ;;
  abort)
    echo "Aborting..."
    # Add your code for actions if user enters "abort"
    exit 1  # Exit script with error code
    ;;
esac

exit 0

gcloud run services describe mkpasswd --region europe-west1 --project thienenkapp-mkpasswd-001 --format json | jq '.spec.template.spec.containers[0].image'
gcloud run services describe mkpasswd --region europe-west1 --project ${PROJECT}
