from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import UserModel
from flask_restful import Resource, request

class ClassName(Resource):


    @jwt_required
    def get(self):
        current_user=get_jwt_identity()
        user=UserModel.find_by_id(current_user)
        if user:
            classe=find_by_id(user.classe_id)
            if classe:
                return {"username":classe.nome}
            return {"message":"user has no class"}, 200
        return {"message":"user does not exist"}, 402

    @jwt_required
    def post(self):
        current_user=get_jwt_identity()
        user=UserModel.find_by_id(current_user)
        className=request.args.get("classe")
        if user:
            if user.admin==True:
                    classe = find_by_id(user.classe_id)
                    if classe:
                        classe.nome=className
                        classe.save_to_db()
                        return {"message":classe.nome}, 200
                    return "banana"
            return {"message":"user is not admin or is not in a class"}, 405
        return {"message":"user does not exist"}, 402
