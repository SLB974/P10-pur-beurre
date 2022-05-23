from decouple import config

SECRET_KEY = config("SECRET_KEY", default="vg6-5ml9g1y6usqj4cy_hgk-a2un=f335ay1*g9z!mgs5s!+l!")
DEBUG=config("DEBUG", default=False)
BDD_PASSW=config("BDD_PSW", default="jade")
