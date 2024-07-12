from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

class Link(db.Model): #hajó és egyén link
    egyen_id = db.Column(db.Integer, db.ForeignKey('egyen.id'), primary_key = True)
    hajo_id = db.Column(db.Integer, db.ForeignKey('hajo.id'), primary_key = True)

class Egyen(db.Model, UserMixin):
    #1db egyénenként
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    jelszo = db.Column(db.String)
    nev = db.Column(db.String, unique=True)
    szuletes = db.Column(db.String)
    beleposzam = db.Column(db.Integer)
    lakcim = db.Column(db.String)
    telefon = db.Column(db.String)
    megjegyzes = db.Column(db.String)
    jogosultsag = db.Column(MutableList.as_mutable(db.PickleType), default=[])
    
    csalad_id = db.Column(db.Integer, db.ForeignKey('csalad.id'))
    statusz_id = db.Column(db.Integer, db.ForeignKey('statusz.id'))
    besorolas_id = db.Column(db.Integer, db.ForeignKey('besorolas.id'))
    
    #több darab egyénenként
    befizetesek = db.relationship('Befizetes',backref="egyen")
    hajok = db.relationship('Hajo', secondary = 'link')
    adatok = db.relationship('Adat', backref='egyen')

class Statusz(db.Model):  #státuszok. Egy státuszhoz több egyén rendelhető
    id = db.Column(db.Integer,primary_key=True)
    tipus = db.Column(db.String)
    tagok = db.relationship("Egyen", backref="statusz" , foreign_keys='Egyen.statusz_id')
    adatok = db.relationship("Adat", backref="statusz" , foreign_keys='Adat.statusz_id')

class Besorolas(db.Model): #besorolások. Egy besoroláshoz több egyén rendelhető
    id = db.Column(db.Integer,primary_key=True)
    tipus = db.Column(db.String)
    tagok = db.relationship("Egyen", backref="besorolas" , foreign_keys='Egyen.besorolas_id')
    adatok = db.relationship("Adat", backref="besorolas" , foreign_keys='Adat.besorolas_id')

class Csalad(db.Model):  #családok. Egy családhoz több egyén rendelhető
    id = db.Column(db.Integer,primary_key=True)
    tipus = db.Column(db.String)
    tagok = db.relationship("Egyen", backref="csalad" , foreign_keys='Egyen.csalad_id')
    adatok = db.relationship("Adat", backref="csalad" , foreign_keys='Adat.csalad_id')

class Cimke(db.Model): #címkék a befizetésekhez (egy címkéhez több befizetés rendelhető)
    id = db.Column(db.Integer, primary_key=True)
    tipus = db.Column(db.String)
    befizetes = db.relationship("Befizetes", backref="cimke", foreign_keys='Befizetes.cimke_id')

class Befizetes(db.Model): #egy befizetés egy egyénhez rendelve, egy címkéje van
    id = db.Column(db.Integer, primary_key=True)
    mennyiseg = db.Column(db.Integer)
    datum = db.Column(db.DateTime(timezone=True))
    mod = db.Column(db.String)
    egyen_id = db.Column(db.Integer, db.ForeignKey('egyen.id'))
    cimke_id = db.Column(db.Integer, db.ForeignKey('cimke.id'))

class Hajotipus(db.Model): #hajó típusok
    id = db.Column(db.Integer,primary_key=True)
    tipus = db.Column(db.String,unique=True)
    hajok = db.relationship('Hajo',backref="hajotipus")

class Hajo(db.Model): #konkrét létező hajók amit birtokolhat több egyén, és amiből egy egyén birtokolhat többet
    id = db.Column(db.Integer,primary_key=True)
    nev = db.Column(db.String)
    hely = db.Column(db.Integer)
    megjegyzes = db.Column(db.String)
    felelos = db.Column(db.Integer,db.ForeignKey('egyen.id'))
    tipus = db.Column(db.Integer,db.ForeignKey('hajotipus.id'))
    birtokosok = db.relationship("Egyen", secondary='link',overlaps="hajok")
    
class Adat(db.Model): #bővülő tábla, ami tartalmazza egy egyén befizetéseit, hajóit, családját, státuszát, besorolását
    id = db.Column(db.Integer,primary_key=True)
    egyen_id=db.Column(db.Integer,db.ForeignKey('egyen.id'))
    csalad_id=db.Column(db.Integer,db.ForeignKey('csalad.id'))
    statusz_id=db.Column(db.Integer,db.ForeignKey('statusz.id'))
    besorolas_id=db.Column(db.Integer,db.ForeignKey('besorolas.id'))
    hajok = db.Column(MutableList.as_mutable(db.PickleType), default=[])
    befizetesek = db.Column(MutableList.as_mutable(db.PickleType), default=[])
    megjegyzes = db.Column(db.String)
    datum = db.Column(db.DateTime(timezone=True))