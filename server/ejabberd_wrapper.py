from django.conf import settings
from subprocess import call


class EjabberdWrapper(): 
    ejabberdHost = '127.0.0.1'
    
    def runCommand(self, argsString):
        status = call(['ejabberdctl '  + argsString + ' 2>&1'])
        print "status: ", status
        
        if(status == 0):
           return true
        else:
            return false
    
    def register (self, username, password):
        return self.runCommand("register " + username + " " + self.ejabberdHost + " " + password )   
    
    
    def unregister (self, username):
        return self.runCommand("unregister " + username + " " + self.ejabberdHost )
    
    
    def ban_account(self, userName, reason):
        return self.runCommand("ban_account " + userName + "@" + self.ejabberdHost + " " + reason )
    
    def change_password(self, userName, newPass):
        return self.runCommand("change_password " + userName + "@" . self.ejabberdHost + " " + newPass)
    
    def srg_create(self, groupName, groupDescription = ''):
        """
          srg_create group host name description display 
        """
        return self.runCommand("srg_create " + groupName + " " + self.ejabberdHost + " " + groupName + " " + groupDescription + " " + groupName )
    
    def srg_delete(self, groupName):
        
        return self.runCommand("srg_delete " + groupName + " " + ejabberdHost )
    
    def srg_user_add(self, userName, groupName):
        """
        srg_user_add user host group grouphost 
        Add the JID user@host to the Shared Roster Group 
        """
        return self.runCommand("srg_user_add " + userName + " " + self.ejabberdHost + " " + groupName + " " + self.ejabberdHost )
    
    def srg_user_del(self, userName, groupName):
        return self.runCommand("srg_user_del " + userName + " " + self.ejabberdHost + " " + groupName + " " + self.ejabberdHost )

    def create_room(self, roomName):
        return self.runCommand("create_room " + roomName + " conference." + self.ejabberdHost + " " + self.ejabberdHost)

    def destroy_room(self, roomName):
        return self.runCommand("destroy_room " + roomName + " conference." + self.ejabberdHost + " " + self.ejabberdHost )
    
    def get_room_occupants(self, roomName):
        return self.runCommand("get_room_occupants " + roomName + " conference." + self.ejabberdHost )

    def muc_online_rooms(self, host = 'global'):
        return self.runCommand("muc_online_rooms " + host)

    def send_direct_invitation(self, room, reason = '', users = []):
        #uString = ''
        #for (user in users): 
        #    uString = user + '@' + self.ejabberdHost + ' '
        return self.runCommand("send_direct_invitation " + room + '@conference.' + self.ejabberdHost + " '',  " + reason + " " + users)

    """
    * set_room_affiliation name service jid affiliation
    * allowed affiliations: array('Owner', 'Admin', 'Member', 'Outcast', 'None')
    """
    def set_room_affiliation(self, groupName, userName, affiliation):
        #if (!in_array(affiliation , array('Owner', 'Admin', 'Member', 'Outcast', 'None'))):
        #    return false
        return self.runCommand("set_room_affiliation " + groupName + ' ' + 'conference.' + selfejabberdHost + ' ' + affiliation)
