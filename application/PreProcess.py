from application.models import User, Roles, UserRoles, SpaceCraft
from application.database import db
from werkzeug.security import generate_password_hash

class PreProcess:
    def prepopulate_roles(self):
        roles = [
            {"name": "admin", "description": "Full Access"},
            {"name": "employee", "description": "Manages spacecraft and booking"},
            {"name": "customer", "description": "Books spacecraft"},
        ]
        existing_roles = {role.name for role in Roles.query.all()}
        for role in roles:
            if role["name"] not in existing_roles:
                new_role = Roles(name=role["name"], description=role["description"])
                db.session.add(new_role)
        db.session.commit()
    
    def create_admin(self):
        admin_role = Roles.query.filter_by(name="admin").one_or_none()
        if not admin_role:
            raise ValueError("Admin role missiing - call prepopulate roles")
        admin = User.query.filter_by(name="admin").one_or_none()
        if not admin:
            admin = User(
                name="admin",
                password_hash=generate_password_hash("admin")
            )
            db.session.add(admin)
            db.session.flush()

            admin_role_entry = UserRoles(user_id=admin.id, role_id=admin_role.id)
            db.session.add(admin_role_entry)
    
    def pre_populate_crafts(self):
        space_carfs = [
                {"name": "Applo", "type": "Lunar Shuttle", "capacity": 2},
                {"name": "Falcon", "type": "Orbital Carrier", "capacity": 4},
                {"name": "Starship", "type": "Deep Space", "capacity": 6}
        ]
        existing_name = {c.name for c in SpaceCraft.query.all()}
        for craft in space_carfs:
            if craft["name"] not in existing_name:
                new_craft = SpaceCraft(name = craft["name"],type = craft["type"],capacity = craft["capacity"])
                db.session.add(new_craft)
            db.session.commit()

    def __init__(self):
        self.prepopulate_roles()
        self.create_admin()
        self.pre_populate_crafts()
        db.session.commit()