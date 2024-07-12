from flask import Blueprint, render_template, request, redirect, flash, jsonify,url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import Egyen, Adat, Csalad, Statusz, Besorolas
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import json

#hozzáad egy egyént, az admin jogosultságait bővítve
def make_user(egyen):
    egyenek = db.session.query(Egyen)
    #+egyen
    #egyen.id = egyenek.count()+1
    db.session.add(egyen)
    egyen.jogosultsag = [egyen.id]
    
    #+admin jogok
    egyenek[0].jogosultsag = egyenek[0].jogosultsag + [egyen.id]

#kitöröl egy egyént, az admin jogosultságait változtatva
def remove_user(egyen):
    egyenek = db.session.query(Egyen)
    #-admin jogok
    egyenek[0].jogosultsag.remove(egyen.id)
    #egyén kitörlése
    db.session.query(Egyen).filter(
            Egyen.id == egyen.id
        ).delete()


#a LIST I-X indexen lévő értékét adja vissza, ha az I =/= None. Ha I==None akkor üres szöveget ad vissza.
def indexof(LIST,I,X):
    if I==None:
        return ''
    return LIST[I-X]



views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #egyenek = db.session.query(Egyen)
    #csaladok = db.session.query(Csalad)
    isadmin=False
    
    #család típusok lekérdezése
    csalad_tipusok = [r.tipus for r in db.session.query(Csalad.tipus) ]
    statusz_tipusok = [r.tipus for r in db.session.query(Statusz.tipus) ]
    besorolas_tipusok = [r.tipus for r in db.session.query(Besorolas.tipus) ]
    
    #egyének kiválasztása akikhez van jogosultsága a felhasználónak
    ID =  [r.id for r in db.session.query(Egyen.id).filter(Egyen.id.in_(current_user.jogosultsag))]
    email =  [str(r.email) for r in db.session.query(Egyen.email).filter(Egyen.id.in_(current_user.jogosultsag))]
    nev =  [str(r.nev) for r in db.session.query(Egyen.nev).filter(Egyen.id.in_(current_user.jogosultsag))]
    telefon =  [str(r.telefon) for r in db.session.query(Egyen.telefon).filter(Egyen.id.in_(current_user.jogosultsag))]
    szuletes =  [str(r.szuletes) for r in db.session.query(Egyen.szuletes).filter(Egyen.id.in_(current_user.jogosultsag))]
    beleposzam =  [str(r.beleposzam) for r in db.session.query(Egyen.beleposzam).filter(Egyen.id.in_(current_user.jogosultsag))]
    lakcim =  [str(r.lakcim) for r in db.session.query(Egyen.lakcim).filter(Egyen.id.in_(current_user.jogosultsag))]
    csalad_nev =  [indexof(csalad_tipusok,r.csalad_id,-1) for r in db.session.query(Egyen.csalad_id).filter(Egyen.id.in_(current_user.jogosultsag))]
    statusz_nev =  [indexof(statusz_tipusok,r.statusz_id,-1) for r in db.session.query(Egyen.statusz_id).filter(Egyen.id.in_(current_user.jogosultsag))]
    besorolas_nev =  [indexof(besorolas_tipusok,r.besorolas_id,-1) for r in db.session.query(Egyen.besorolas_id).filter(Egyen.id.in_(current_user.jogosultsag))]

    elerheto_egyenek=[email,nev,telefon,szuletes,beleposzam,lakcim,
                      csalad_nev,statusz_nev,besorolas_nev,ID] #ID lista mindig utolsó
    
    #adatok kiválasztása amikhez van jogosultsága a felhasználónak
    datum =  [str(r.datum) for r in db.session.query(Adat.datum).filter(Adat.egyen_id.in_(current_user.jogosultsag))]
    csalad_id =  [ r.csalad_id for r in db.session.query(Adat.csalad_id).filter(Adat.egyen_id.in_(current_user.jogosultsag)) ]
    statusz_id =  [r.statusz_id for r in db.session.query(Adat.statusz_id).filter(Adat.egyen_id.in_(current_user.jogosultsag))]
    besorolas_id =  [r.besorolas_id for r in db.session.query(Adat.besorolas_id).filter(Adat.egyen_id.in_(current_user.jogosultsag))]
    egyen_id =  [r.egyen_id for r in db.session.query(Adat.egyen_id).filter(Adat.egyen_id.in_(current_user.jogosultsag))]
    adat_id = [r.id for r in db.session.query(Adat.id).filter(Adat.egyen_id.in_(current_user.jogosultsag))]
    
    elerheto_adatok=[datum,csalad_id,statusz_id,besorolas_id,egyen_id,adat_id]
    
    #admin-e a jelenlegi felhasználó
    if current_user.id==1:
        isadmin=True
    
    return render_template("home.html",
                            user=current_user,
                            allowed_users=elerheto_egyenek,
                            allowed_users_data=elerheto_adatok,
                            family_types=csalad_tipusok,
                            status_types=statusz_tipusok,
                            class_types=besorolas_tipusok,
                            isadmin=isadmin)

@views.route('/mod-user', methods=['GET', 'POST'])
@login_required
def mod_user():
    data = json.loads(request.data)
    egyen = Egyen.query.get(data['userId'])
    if egyen:
        egyen.email=data['data'][0]
        egyen.nev=data['data'][1]
        egyen.telefon=data['data'][2]
        egyen.szuletes=data['data'][3]
        egyen.beleposzam=data['data'][4]
        egyen.lakcim=data['data'][5]
    else:
        e=Egyen(email=data['data'][0],
                nev=data['data'][1],
                telefon=data['data'][2],
                szuletes=data['data'][3],
                beleposzam=data['data'][4],
                lakcim=data['data'][5]
            )
        e.id=data['userId'];
        make_user(e)
        
    db.session.commit()
    
    return jsonify({})

@views.route('/del-user', methods=['GET', 'POST'])
@login_required
def del_user():
    data = json.loads(request.data)
    egyen = Egyen.query.get(data['userId'])
    print(data['userId'])
    remove_user(egyen)
    
    db.session.commit()
    
    return jsonify({})
