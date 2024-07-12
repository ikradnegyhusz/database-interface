from base import *
import os

def print_menu(List):
    for i in range(len(List)):
        print(str(i)+" - "+List[i])

app = create_app()
with app.app_context():
    #menu
    options=["exit","+admin","+egyén","+család","+státusz","+besorolás","+fizetési címke","+hajótípus","+adat"]
    while(True):
        os.system('cls')
        print_menu(options)
        inp = input(">>> ")
        
        if inp == '0': exit()
        elif inp == '1': add_admin()
        elif inp == '2': add_egyen(int(input("n = ")))
        elif inp == '3': add_tipus("csalad",int(input("n = ")))
        elif inp == '4': add_tipus("statusz",int(input("n = ")))
        elif inp == '5': add_tipus("besorolas",int(input("n = ")))
        elif inp == '6': add_tipus("cimke",int(input("n = ")))
        elif inp == '7': add_tipus("hajotipus",int(input("n = ")))
        elif inp == '8': add_adat(int(input("egyen id = ")),int(input("n = ")))