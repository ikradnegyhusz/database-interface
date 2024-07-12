from base import *
app = create_app()
with app.app_context():
    add_admin()
    add_egyen(50)
    add_tipus("csalad",50)
    add_tipus("statusz",50)
    add_tipus("besorolas",50)
    egyenek = db.session.query(models.Egyen)
    for egyen in egyenek:
        add_adat(egyen.id,30)
    input("done.")