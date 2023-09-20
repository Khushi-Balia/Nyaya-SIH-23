#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d ".env" ]; then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
. .env/bin/activate
export ENV=development
export MONGODB_HOST='mongodb+srv://raghavagarwal3050:6gsAAeoeoSAOp6yA@cluster0.dtrh2f9.mongodb.net/?retryWrites=true&w=majority'
fuser -n tcp -k 5000
python3 app.py 
deactivate
