import datetime
from urlparse import urlparse
import re
import smtplib

from tiktok.model.task import Task
from tiktok.model.project import Project
from tiktok.model.user import User
from tiktok.lib import resources, config, helpers
from tiktok.commands import task

class URL( object ):
    def __init__(self, url, *args, **kwargs ):
        
        url = urlparse( url )
        
        self.url = url
        # Select the correct Object to use as the ressource
        # The ressource handles all the system specific logic
        self.select_ressource( )
        self.init_ressource( )
        
    def clock( self, date, start_time, stop_time ):
        return False
        
    def live( self ):
        # Allows you to clock live in the taks IDed by the URL
        project_id = self.ressource.get_project_id( )
        project_cit = False
        answer = ''
        cit_task = False
        start = True

        args = {
            'keyword' : self.ressource.get_cit_id( )
        }

        search = Task.search(**args)

        if search:
            # ToDo : make sur this is correct. Don't know the JSON structure yet

            cit_task = int( re.search( '^#([0-9]*)', search[0]['label'] ).group(1) )

            cit_task = Task.get( cit_task )
            print( 'Found the task...' )
        else :
            print("No existing task...")
            print("Trying to figure out the project")

            if project_id:
                print( 'Project ID:' + project_id )
                print("Found a project ID...")
                p_list = Project.list( )

                for project in p_list: 
                    if project_id in project['name']:
                        project_cit = unicode(project['name'])

                        print( u'Found the project in CIT (ID ' + project_cit + u'), creating task...' )
                        # Mostly copied code from the command.task. Not DRY but it didn't work the 
                        # way I wanted it to. REMEMBER IT'S A POC

                        data = {
                            'name' : self.ressource.get_name( ),
                            'project': project_cit,
                            'duration': helpers.helpers.duration.parse('8:00'),
                            'start': True
                        }

                        # ---- Code logic for creating a taks -----

                        creator_id = User.find_id_by_username( config.configs['username'] )

                        #Transform project name into project id
                        found = Project.find_id_by_name( data.pop( 'project') )
                        if len( found ) == 0:
                            print "ERROR: project does not exist (project name not found)"
                            sys.exit( 1 )
                        elif len ( found ) > 1:
                            print "ERROR: more than one project with the same name (try putting in a longer project name for searching)"
                            sys.exit( 1 )

                        data['project_id'] = found[0]

                        #Transform usernames into user ids
                        user_ids = [ creator_id[0] ]

                        user_ids = list( set( user_ids ) )

                        data['user_ids'] = user_ids

                        cit_task = Task.create( **data )
                        # ---- End code logic for creating task -----

                        break

            if not project_cit:
                print("No CIT project found, do you want me to send an email to "+ config.configs['email_to'] + " asking for one?")
                
                while not re.match('y|n', answer):
                    answer = raw_input( "[y/N]: " ).strip().lower()
                    if answer == '':
                        answer = 'n'

                if 'y' in answer:
                    print( 'Sending an email' )

                    smtp = smtplib.SMTP()
                    smtp.set_debuglevel(0)
                    smtp.connect(config.configs['smtp_host'], config.configs['smtp_port'])
                    smtp.login(config.configs['smtp_user'], config.configs['smtp_pass'])

                    from_addr = config.configs['smtp_user']
                    to_addr = config.configs['email_to']

                    subj = "Besoin d'une tache CIT"

                    message_text = "Bonjour,\nJe cherche une tache pour clocker\n\n"+ self.ressource.get_cit_id( ) +"\n\nSVP Veuillez indiquer le # du projet sous sa forme P-00000-00 dans le nom du projet sur redmine ou dans le contenu du billet sur RT\n\nMerci pour votre Collaboration\n\nUn humble employer un peu perdu.\n\n" + self.url.geturl()

                    msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % ( from_addr, to_addr, subj, message_text )

                    smtp.sendmail(from_addr, to_addr, msg)
                    smtp.quit()
                    # ToDo
                else:
                    print( 'No email sent, you cannot clock your time at the moment, sry mate!')
        if cit_task:
            if start:
                cit_task.start()
                print( 'Now clocking on your task: ' )
                print(cit_task['name'])

        taskname = self.ressource.get_name( )

        return False
        
    def select_ressource( self ):
        '''
            Which ressrouce do you need. Probably could be a factory
            pattern.

            Single subdomain implied. Also implied is that this subdomain 
            identifies the Ressource to use
        '''
        system = self.url.hostname.split( '.' )[0]

        # Build the ressource name based on the system name
        self.selected_ressource =  vars( resources )[ system.capitalize() + 'Ressource' ]
    
    def init_ressource( self ):
        ID = False
        path = self.url.path.split( '/' )
        # Better to search for numbers then assume the position in the URL
        ID = re.search( '[0-9]+', self.url.path )
        if not ID:
            ID = re.search( '[0-9]+', self.url.query )

        if ID:
            ID = ID.group( 0 )

        self.ressource = self.selected_ressource( self.url.hostname, self.url.scheme, config.configs['username'], config.configs['password'], ID )



        