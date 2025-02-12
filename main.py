import mysql.connector
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="task_manager"
        )
        self.cursor = self.conn.cursor()
        self.create_table()
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                description TEXT NOT NULL,
                deadline DATE NOT NULL,
                status VARCHAR(20) NOT NULL
            )
        """)
        self.conn.commit()
    def add_task(self):
        description = input("Enter task description: ")
        while True:
            deadline = input("Enter task deadline (YYYY-MM-DD): ")
            try:
                datetime.strptime(deadline, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format! Please use YYYY-MM-DD format.")
        while True:
            status = input("Enter task status (pending/completed): ").lower()
            if status in ['pending', 'completed']:
                break
            print("Invalid status! Please enter either 'pending' or 'completed'.")
        
        try:
            query = "INSERT INTO tasks (description, deadline, status) VALUES (%s, %s, %s)"
            values = (description, deadline, status)
            
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Task added successfully!")
        except mysql.connector.Error as err:
            print(f"Error adding task: {err}")

    def view_all_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        
        if not tasks:
            print("No tasks found!")
            return
            
        for task in tasks:
            print(f"\nTask ID: {task[0]}")
            print(f"Description: {task[1]}")
            print(f"Deadline: {task[2]}")
            print(f"Status: {task[3]}")
            print("-" * 50)

    def update_task(self):
        task_id = input("Enter task ID to update: ")
        self.cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = self.cursor.fetchone()
        
        if not task:
            print("Task not found!")
            return
        print("\nWhat would you like to update?")
        print("1. Description")
        print("2. Deadline")
        print("3. Status")
        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            new_desc = input("Enter new description: ")
            query = "UPDATE tasks SET description = %s WHERE id = %s"
            values = (new_desc, task_id)
        elif choice == "2":
            while True:
                new_deadline = input("Enter new deadline (YYYY-MM-DD): ")
                try:
                    datetime.strptime(new_deadline, '%Y-%m-%d')
                    query = "UPDATE tasks SET deadline = %s WHERE id = %s"
                    values = (new_deadline, task_id)
                    break
                except ValueError:
                    print("Invalid date format! Please use YYYY-MM-DD format.")
        elif choice == "3":
            while True:
                new_status = input("Enter new status (pending/completed): ").lower()
                if new_status in ['pending', 'completed']:
                    query = "UPDATE tasks SET status = %s WHERE id = %s"
                    values = (new_status, task_id)
                    break
                print("Invalid status! Please enter either 'pending' or 'completed'.")
        else:
            print("Invalid choice!")
            return
        self.cursor.execute(query, values)
        self.conn.commit()
        print("Task updated successfully!")
    def delete_task(self):
        task_id = input("Enter task ID to delete: ")
        self.cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = self.cursor.fetchone()  
        if not task:
            print("Task not found!")
            return
        confirm = input("Are you sure you want to delete this task? (y/n): ")
        if confirm.lower() == 'y':
            self.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.conn.commit()
            print("Task deleted successfully!")
        else:
            print("Delete operation cancelled.")
    def view_pending_tasks(self):
        self.cursor.execute("SELECT * FROM tasks WHERE status = 'pending' ORDER BY deadline")
        tasks = self.cursor.fetchall()
        if not tasks:
            print("No pending tasks found!")
            return
        for task in tasks:
            print(f"\nTask ID: {task[0]}")
            print(f"Description: {task[1]}")
            print(f"Deadline: {task[2]}")
            print(f"Status: {task[3]}")
            print("-" * 50)
    def view_completed_tasks(self):
        self.cursor.execute("SELECT * FROM tasks WHERE status = 'completed' ORDER BY deadline")
        tasks = self.cursor.fetchall()
        if not tasks:
            print("No completed tasks found!")
            return
        for task in tasks:
            print(f"\nTask ID: {task[0]}")
            print(f"Description: {task[1]}")
            print(f"Deadline: {task[2]}")
            print(f"Status: {task[3]}")
            print("-" * 50)
def main():
    task_manager = TaskManager()    
    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. View Pending Tasks")
        print("6. View Completed Tasks")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ")
        if choice == "1":
            task_manager.add_task()
        elif choice == "2":
            task_manager.view_all_tasks()
        elif choice == "3":
            task_manager.update_task()
        elif choice == "4":
            task_manager.delete_task()
        elif choice == "5":
            task_manager.view_pending_tasks()
        elif choice == "6":
            task_manager.view_completed_tasks()
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()