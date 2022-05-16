from flask import Flask, request
from flask_restful import Api, Resource, reqparse,abort
import sqlite3

app = Flask(__name__)
api = Api(app)

post_cip_args = reqparse.RequestParser()
post_cip_args.add_argument("ids", action='append', help="List of ids is required for post request")
post_soc_args = reqparse.RequestParser()
post_soc_args.add_argument("ids", action='append', help="List of ids is required for post request")

connection = sqlite3.connect("cip_mapping.db", check_same_thread=False)
cursor = connection.cursor()

#-----Classes-----#
class Cip(Resource):
    def get(self,cip):
        objects = []
        for row in cursor.execute(f"SELECT soc_id, soc_name FROM cip_to_soc WHERE cip_id='{cip}'"):
            row_json = {"soc_id": row[0], "soc_name": row[1]}
            objects.append(row_json)
        return {cip:objects}

class CipPost(Resource):
    def get(self):
        cips = []
        for row in cursor.execute(f"SELECT cip_id, cip_name FROM cip_to_soc"):
            row_json = {"cip_id": row[0], "cip_name": row[1]}
            cips.append(row_json)
        return{"data": cips}

    def post(self):
        ids = post_cip_args.parse_args()
        id_list = ids['ids']
        id_objects = []
        for id in id_list:
            objects = []
            for row in cursor.execute(f"SELECT soc_id, soc_name FROM cip_to_soc WHERE cip_id='{id}'"):
                row_json = {"soc_id": row[0], "soc_name": row[1]}
                objects.append(row_json)
            id_objects.append({id:objects})
        return {"data": id_objects}


class Soc(Resource):
    def get(self,soc):
        objects = []
        for row in cursor.execute(f"SELECT cip_id, cip_name FROM cip_to_soc WHERE soc_id='{soc}'"):
            row_json = {"cip_id": row[0], "cip_name": row[1]}
            objects.append(row_json)
        return {soc:objects}

class SocPost(Resource):
    def get(self):
        socs = []
        for row in cursor.execute(f"SELECT soc_id, soc_name FROM cip_to_soc"):
            row_json = {"soc_id": row[0], "soc_name": row[1]}
            socs.append(row_json)
        return{"data": socs}

    def post(self):
        ids = post_soc_args.parse_args()
        id_list = ids['ids']
        id_objects = []
        for id in id_list:
            objects = []
            for row in cursor.execute(f"SELECT cip_id, cip_name FROM cip_to_soc WHERE soc_id='{id}'"):
                row_json = {"cip_id": row[0], "cip_name": row[1]}
                objects.append(row_json)
            id_objects.append({id:objects})
        return {"data": id_objects}

#-----Resources-----#
api.add_resource(Cip, "/cip/<string:cip>")
api.add_resource(CipPost, "/cip")
api.add_resource(Soc, "/soc/<string:soc>")
api.add_resource(SocPost,"/soc")


if __name__ == "__main__":
    app.run(debug=True)