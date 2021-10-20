#!/usr/bin/env python
from sqlobject import *

#sqlhub.processConnection = connectionForURI('postgres://localhost:5432/luke')
sqlhub.processConnection = connectionForURI('postgres://')

class Microcontroller(SQLObject):
    class sqlmeta: fromDatabase = True
    
'''
class P_Address_block(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Architecture(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Enumeration(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Enumeration_element(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Field(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Interrupt(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Market_state(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Package(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Peripheral(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Peripheral_instance(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Register(SQLObject):
    class sqlmeta: fromDatabase = True

class P_User(SQLObject):
    class sqlmeta: fromDatabase = True

class P_Vendor(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_address_block(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_architecture(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_enumeration(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_enumeration_element(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_field(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_interrupt(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_market_state(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_package(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_peripheral_instance(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_register(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_register_cluster(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_user(SQLObject):
    class sqlmeta: fromDatabase = True

class Pl_vendor(SQLObject):
    class sqlmeta: fromDatabase = True
'''


if __name__ == '__main__':
    for mc in Microcontroller.select():
        print(mc)
        #print(dir(mc))
        #print(vars(mc))
        for name in dir(mc):
            print('  ', name, ' <-> ', getattr(mc, name, None))
        print()
        print(dir(mc.sqlmeta))
        for name in dir(mc.sqlmeta):
            print('  ', name, ' <-> ', getattr(mc.sqlmeta, name, None))
            
        break
