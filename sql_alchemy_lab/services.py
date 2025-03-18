from models import User, Order
from main import Session


data = [
    {'username': 'john_doe', 'email':'john.doe@example.com'},
    {'username': 'sarah_smith', 'email':'sarah.smith@gmail.com'},
    {'username': 'mike_jones', 'email':'mike.jones@company.com'},
    {'username': 'emma_wilson', 'email':'emma.wilson@domain.net'},
    {'username': 'david_brown', 'email':'david.brown@email.org'},

]

with Session() as session:
    for item in data:
        user = User(**item)
        session.add(user)
    session.commit()


with Session() as session:
    user_to_delete = session.query(User).filter_by(username='john_doe').first()

    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print("User deleted successfully")
    else:
        print("User does not found")

with Session() as session:
    try:
        session.query(User).delete()
        session.commit()
        print("All users deleted successfully")
    except Exception as e:
        session.rollback()
        print("An error occurred:", str(e))

    finally:
        session.close()
        
with Session() as session:
    orders = session.query(Order).order_by(Order.user_id.desc()).all()
    if not orders:
        print("No orders yet.")
    else:
        for order in orders:
            user = order.user
            print(f"Order number {order.id}, Is completed: {order.is_completed}, Username: {user.username}")

