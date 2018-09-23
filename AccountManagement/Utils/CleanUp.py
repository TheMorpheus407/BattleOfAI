from AccountManagement.Database.UserDTO import UserDTO
from AccountManagement.Database.db import db


def delete_trash_accounts():
    users = UserDTO.query.filter_by(email_verified=False).all()
    for i in users:
        if i.can_be_trashed():
            db.session.delete(i)
    db.session.commit()
