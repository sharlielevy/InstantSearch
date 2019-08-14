
class Singleton:
    def __init__(self,decorated):
         self._decorated = decorated
    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance
    def __call__(self):
        raise TypeError("Singletone must be accessed thotough `Instance()`.")

    def __instancecheck__(self,inst):
        return isinstance(inst,self._decorated)


class Command:

    def __init__(attr_name,attr_val,attr_prev_val) :
        self.attribute_name = attr_name
        self.attribute_prev_value = attr_prev_val
        self.attribute_value = attr_val

    def execute(self):
        # write to UNDO's db
        # updates the APP _attr_val_list with self.attribute_value 
      
    def undo(self):
        # updates the APP _attr_val_list with elf.attribute_prev_value

class History:
    undos = []
    redos = []
    def execute(cmd):
        cmd.execute()
        undos.push(cmd)
        redos.clears()

    def undo:
        cmd = undos.pop()
        cmd.undo()
        redus.push(cmd)

    def redo:
        cmd = redos.pop()
        cmd.execute()
        undos.push()


@Singleton
class DBHandler:
    self.history = History()

    # Req - 
    """ SET – [http://_your-app-id_.appspot.com/set?name={variable_name}&value={variable_value}] 
    # Set the variable variable_name to the value variable_value, neither variable names nor values
    # will contain spaces. Print the variable name and value after the change."""
    def SetHandler(variable_name,variable_value):
        # 1.Removing the spaces from the attribute_name && attribute values strings
        variable_name.spilt()
        variable_value.split()

        # 2. Creating a new DB record with the name and value and call History.execute with the new object
        # 3. History write object to UNDO's Table
        # 4. History calls Command execute action is being called :
        #           - update the app attributes values)
        #           - prints out new varaible name and value to console
        # 5. History clears REDO's Table
        prev_val = 0
        is_exist = variable_name in self.app_data
        if is_exist == True:
            prev_val =self.app_data[variable_name]

        cmd = Command(variable_name,variable_value,prev_val)
        self.history.execute(cmd)

       

    # Req
    """GET – [http://_your-app-id_.appspot.com/get?name={variable_name} 
    Print out the value of the variable variable_name or “None” if the variable is not set."""    
    def GetHandler(variable_name):
        #1.Removing the spaces from the attribute_name
        #2.Rerieve last value of the same attribute_name from UNDO's DB
        #3.Printing new varaible name and value to console
        # 
        variable_name.split()
        ret_val = "None"
        is_exist = variable_name in self.app_data
        if is_exist == True:
            ret_val = self.app_data[variable_name]
        
        print("The value of the " + variable_name + " is " + ret_val)
        
      

    # Req 
    """UNSET – [http://_your-app-id_.appspot.com/unset?name={variable_name}]
    Unset the variable variable_name, making it just like the variable was never set."""
    def UnsetHandler(variable_name):
        variable_name.split()
        self.SetHandler(variable_name,"")

    # Req    
    """NUMEQUALTO – [http://_your-app-id_.appspot.com/numequalto?value={variable_value}]
    Print to the browser the number of variables that are currently set to variable_value. 
    If no variables equal that value, print 0."""
   def NumEqualToHandler(variable_value):
       #1.Removing the spaces from the attribute_name
        variable_value.split()
        count = 0
        for item in self.app_data:
            if self.app_data[item] == variable_value:
                count += 1
        print("The number of  " + variable_name + " is " + count)    
       #2.Querying  UNDO's DB for all records that their attribute value is "variable_value"
       #3.Printing number of records. if therre is none, Print 0


   
    # Req   
    """UNDO – [http://_your-app-id_.appspot.com/undo]
    Undo the most recent SET/UNSET command. If more than one consecutive UNDO command is issued,
     the original commands should be undone in the reverse order of their execution. 
     Print the name and value of the changed variable (after the undo) if successful, 
     or print NO COMMANDS if no commands may be undone.
    Example: If you set the variable name x to the value 13 via request, then you set the variable name x to
     the value 22 via request, the undo request will undo the assignment of the value 22 to the variable x and
      will revert it’s value to 13, if then another undo request will be issued it will unset the variable. """
    def UndoHandler:
        self.history.undo()
        #1. History calls undo function that :
            # - pops out the last record of the UNDO's table.
            # - creating a new command out of the record values(name,value,prev_val)
            # - calls command execute function
        #2. History writes  the command into the REDO's table


    # Req
    """REDO – [http://_your-app-id_.appspot.com/redo]
    Redo the most recent SET/UNSET command which was undone.  If more than one consecutive REDO command is issued,
     the original commands should be redone in the original order of their execution.
      If another command was issued after an UNDO, the REDO command should do nothing.
       Print the name and value of the changed variable (after the redo) if successful, 
       or print NO COMMANDS if no commands may be re-done."""
    def RedoHandler:
        #1. History calls redo function that :
            # - pops out the last record of the REDO's table.
            # - creating a new command out of the record values(name,value,prev_val)
            # - calls command redo function
        #2. History writes  the command into the UNDO's table
     self.history.redo()
   
   
    # Req
    """END – [http://_your-app-id_.appspot.com/end]
    Exit the program. Your program will always receive this as its last command. You need to remove all your data 
    from the application (clean all the Datastore entities). Print CLEANED when done."""
    def EndHandler:
        #1.History will go over all REDO'S/UNDO'S tables clean it
        #2.History will print out CLEANED to the console



def main():
    db_handler = DBHandler.Instance()
    db_handler.app_data = {}
    application = webapp2.WSGIApplication([
        	('/get',	db_handler.GetHandler),
      	    ('/set', 	db_handler.SetHandler),
            ('/unset', db_handler.UnsetHandler),
            ('/numequalto', db_handler.NumEqualToHandler),
            ('/undo', 	 db_handler.UndoHandler),
            ('/redo', 	 db_handler.RedoHandler),
            ('/end',    db_handler.EndHandler)    	
        ], debug=False)

main()