# sweethearts facebook app

#DONE
- set up django project, database, vagrant box settings and other settings
- added database schema and migrations
- implemented login view
- implemented main page after login
- implemented logout/deactivation view, decode/validation part pending

#TODO
- finish up logout/deactivation view. I didn't deploy this project on server, thus I was not able to debug the deAuth
workflow. so I skipped the signature and payload part.
some references: https://developers.facebook.com/docs/games/gamesonfacebook/login#parsingsr
https://stackoverflow.com/a/6102526/2628463

# Potential optimizations
- use django RESTful framework
- add unittests
- move hard code parameters to config files, i.e. facebook api version.
- refactor the code to be more reusable, i.e to support multiple login source (i.e. facebook, twitter, etc).

# install virtualenv
`sudo apt-get install python3`
`sudo apt-get install python3-pip`
`sudo pip3 install virtualenv`

# enter virtualenv
`source sh-env/bin/activate`

# install requirements
`pip install -r requirements.txt`
