
# music_streaming_app_using_flask_and_vue.js
=======
run python server

create environment
python3 -m venv nameofenvironment

activate environment
source nameofenvironment/bin/activate

install packages
pip install -r requirements.txt

activate python server
python app.py

celery jobs
celery -A app.celery worker -l info

celery periodic jobs 
celery -A app.celery beat -l info

mailhog 
mailhog is present in usually present in go/bin folder
cd $HOME/go/bin
type ./MailHog

running frontend server
npm install -g @vue/cli - for creating the vue folder
vue create my-vue-app  # Replace 'my-vue-app' with your project name
cd my-vue-app

if you are using templates in the repository then you have to 
add the packages of the vue cli by the command
npm install
(this instruction is for others who deleted their node modules 
add node modules using 
npm install
i have'nt uploaded the node modules along with the folder ,above command reads the package.json to install the necessary packages if you need it.)

install vue-star-rating used in rating the shows by entering below command
npm install vue-star-ratings --save

run server using 
npm run serve

>>>>>>> origin/main
