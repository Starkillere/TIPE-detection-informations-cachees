from add_data_to_db import *
from algorithme_de_dissimulation import *
from db_manager import *
from recole_des_donnees_limlite import *
import os

if [f for f in os.listdir("covers") if os.path.isfile(os.path.join("covers", f))] == []:
    db_local_db = create_database()
    hote_loader(db_local_db)
    hide_loader(db_local_db)
    creat_covers(db_local_db)
    data_collect(db_local_db)
    data_collect_without_transformation(db_local_db)