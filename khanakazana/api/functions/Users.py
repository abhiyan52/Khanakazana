from khanakazana.api.functions.Models import Users
from khanakazana.api.functions.Database import Database
from khanakazana.api.functions.Response import Response


class UserAPI(Database):
    def __init__(self):
        super(UserAPI, self).__init__()
    
    def list_all_owners(self):
        owners = self.session.query(Users).filter(Users.user_type == 1)
        return owners

    def list_all_users(self):
        users = self.session.query(Users).filter(Users.user_type==0)
        return users
    
    def change_previledges(self, user_id, new_user_type):
        user = self.session.query(Users).filter(id == user_id).first()
        user.user_type = new_user_type
        self.session.commit()
        return 'OK'
    
    def delete_user(self, user_id):
        user = self.session.query(Users).filter(id == user_id).first()
        self.session.delete(user)
        self.session.commit()
    
    def update_user(self, user_id, update_field):
        user = self.session.query(Users).filter(id == user_id).first()
        if user is not None:
            update_field = update_fields.to_dict(flat=True)
            for key, value in update_fields.items():
                setattr(user, key, value)
            self.session.commit()
    
    
