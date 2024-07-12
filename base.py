from website import models
from website import db
from website import create_app
from werkzeug.security import generate_password_hash
import datetime
import random

def add_admin():
    egyenek = db.session.query(models.Egyen)
    
    if egyenek.count()==0:
        admin = models.Egyen(email="admin@gmail.com",
                             nev="ADMIN",
                             jelszo=generate_password_hash("Hello", method='sha256'),
                             jogosultsag=[1])
        db.session.add(admin)
    
    db.session.commit()

def make_user(egyen):
    egyenek = db.session.query(models.Egyen)
    #add new user
    egyen.id = egyenek.count()+1
    db.session.add(egyen)
    egyen.jogosultsag = [egyen.id]
    
    #update admin rights
    egyenek[0].jogosultsag = egyenek[0].jogosultsag + [egyen.id]

def add_egyen(n):

    egyenek = db.session.query(models.Egyen)
    m=egyenek.count()
    for i in range(n):
        STR=str(i+m)
        email = "user"+STR+"@gmail.com"
        pw = generate_password_hash( "password"+STR,method="sha256" )
        nev = "user_"+STR
        x = models.Egyen(nev=nev,email=email,jelszo=pw)
        make_user(x)
    
    db.session.commit()

def add_tipus(model_name,n):

    model=0
    if model_name=="csalad": model=models.Csalad
    elif model_name=="statusz": model=models.Statusz
    elif model_name=="besorolas": model=models.Besorolas
    elif model_name=="cimke": model=models.Cimke
    elif model_name=="hajotipus": model=models.Hajotipus
   
    q = db.session.query(model)
    m = q.count()
    for i in range(n):
        STR=str(i+m)
        tipus = model_name+STR;
        x = model(tipus=tipus)
        db.session.add(x);
    
    db.session.commit()

def add_adat(egyen_id,n):
    egyenek = db.session.query(models.Egyen)
    csaladok = db.session.query(models.Csalad)
    besorolasok = db.session.query(models.Besorolas)
    statuszok = db.session.query(models.Statusz)
    
    for i in range(n):
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(days=10)
        random_date = start_date + (end_date - start_date) * random.random()
    
        adat = models.Adat()
        adat.egyen = egyenek[egyen_id-1]
        adat.datum = random_date
        adat.csalad = csaladok[random.randint(0,csaladok.count()-1)]
        adat.statusz = statuszok[random.randint(0,statuszok.count()-1)]
        adat.besorolas = besorolasok[random.randint(0,besorolasok.count()-1)]
        
        db.session.add(adat)
    
    db.session.commit()