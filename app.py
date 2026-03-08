from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import mysql.connector
import seed_mental_health_tracker

app = Flask(__name__)

DB_NAME = "mental_health_tracker"


def clear():
    os.system('cls||clear')

def enter_health_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT entry_date, mood_level, stress_level, energy_level, hours_slept, notes"
                " FROM daily_entries"
                " WHERE entry_date = (CURDATE())")
    rows = cur.fetchall()
    if len(rows) > 0:
        print("Daily entry already recorded")
        input("Press enter to continue.")
        cur.close()
        return
    try:
        sleep = int(input("How many hours did you sleep?\n->"))
        mood = int(input("How is your mood level on a scale from 1-10?\n->"))
        stress = int(input("How is your stress level on a scale from 1-10?\n->"))
        energy = int(input("How is your energy level on a scale from 1-10?\n->"))
        notes = str(input("Any notes:\n->"))

        sql = "INSERT IGNORE INTO daily_entries (hours_slept, mood_level, stress_level, energy_level, notes)" \
        "VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql,(sleep, mood, stress, energy, notes))
        conn.commit()

        print("Data entered successfully!")
        input("Press enter to continue.")
    except ValueError:
        print("You must enter a number.")
        input("Press enter to continue.")
    finally:
        cur.close()

def view_all_health_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT entry_date, mood_level, stress_level, energy_level, hours_slept, notes FROM daily_entries")
    rows = cur.fetchall()
    cur.close()
    print(f"{'Date':<12} {'Mood':<6} {'Stress':<8} {'Energy':<8} {'Sleep':<6} {'Notes'}")
    print("-" * 60)
    for entry_date, mood_level, stress_level, energy_level, hours_slept, notes in rows:
        print(f"{str(entry_date):<12} {mood_level:<6} {stress_level:<8} {energy_level:<8} {hours_slept:<6} {notes}")
    input("Press enter to continue.")

def enter_new_habit(conn):
    cur = conn.cursor()
    try:
        h_name = str(input("What is your habit called?\n->"))
        notes = str(input("Any notes:\n->"))

        sql = "INSERT IGNORE INTO habits (habit_name, notes)" \
        "VALUES (%s, %s)"
        cur.execute(sql,(h_name, notes))
        conn.commit()

        print("New habit has been entered successfully!")
        input("Press enter to continue.")
    except ValueError:
        print("Wrong input data. Please try again.")
        input("Press enter to continue.")
    finally:
        cur.close()

def list_all_habits(conn):
    cur = conn.cursor()
    cur.execute("SELECT habit_name, entry_date, notes FROM habits")
    rows = cur.fetchall()
    cur.close()
    print(f"{'Date created':<12} {'Habit name':<30} {'Notes'}")
    print("-" * 60)
    for habit_name, entry_date, notes in rows:
        print(f" {str(entry_date):<12} {habit_name:<30} {notes}")
    input("Press enter to continue.")

def log_habit(conn):
    cur = conn.cursor()
    cur.execute("SELECT habit_id, habit_name FROM habits")
    rows = cur.fetchall()
    cur.close()
    print("Choose the habit you would like to log:")
    for habit_id, habit_name in rows:
        print(f" {habit_id}. {habit_name} ")

    try:
        h_id = int(input("--> "))
        cur = conn.cursor()
        cur.execute("SELECT * FROM habits WHERE habit_id = %s", (h_id,))
        rows = cur.fetchall()
        if len(rows) == 0:
            print("Habit not found.")
            input("Press enter to continue.")
            cur.close()
            return
        cur.close()
        cur = conn.cursor()
        cur.execute(
            "SELECT habit_id, entry_date FROM habit_logs WHERE habit_id = %s AND entry_date = CURDATE()",
            (h_id,)
        )
        rows = cur.fetchall()
        if len(rows) > 0:
            print("You have already logged this habit today.")
            input("Press enter to continue.")
            cur.close()
            return

        sql = "INSERT IGNORE INTO habit_logs (habit_id, completed)" \
              "VALUES (%s, %s)"
        cur.execute(sql, (h_id, 1))
        conn.commit()

        print("Good job on completing your habit. Keep it up!")
        print("Habit logged successfully.")
        input("Press enter to continue.")
    except ValueError:
        print("You must enter a number.")
        input("Press enter to continue.")
    finally:
        cur.close()

def view_habit_logs(conn):
    cur = conn.cursor()
    cur.execute("SELECT entry_date, habit_name FROM habit_date_completion")
    rows = cur.fetchall()
    cur.close()
    print(f"{'Date logged':<12} {'Habit name':<30} ")
    print("-" * 60)
    for entry_date, habit_name in rows:
        print(f" {str(entry_date):<12} {habit_name:<30}")
    input("Press enter to continue.")

def view_alerts(conn):
    cur = conn.cursor()
    cur.execute("select entry_date, alert_type, alert_message from alerts")
    rows = cur.fetchall()
    cur.close()
    print(f"{'Date triggered':<16} {'Alert type':<40} {'Alert message':<40}")
    print("-" * 60)
    for entry_date, alert_type, alert_message in rows:
        print(f" {str(entry_date):<16} {alert_type:<40} {alert_message}")
    input("Press enter to continue.")

def get_connection(db = None):
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=db,
    )

def main():
   # mode = input("Run mode (web / console): ").strip().lower()
   # if mode == "web":
   #     run_web()
   # elif mode == "console":
        run_console()


def run_web():
    load_dotenv()
    conn = setup_database()
    app.run(debug=True, use_reloader=False)
    conn.close()

def run_console():
    load_dotenv()
    conn = setup_database()
    is_running = True
    while is_running:
        clear()
        Main_Menu()
        choice = input("--> ")
        clear()
        is_running = handle_main_menu_input(choice, conn)
    conn.close()


def handle_main_menu_input(choice, conn):
    if choice == "1":
        enter_health_data(conn)
        return True
    elif choice == "2":
        view_all_health_data(conn)
        return True
    elif choice == "3":
        enter_new_habit(conn)
        return True
    elif choice == "4":
        list_all_habits(conn)
        return True
    elif choice == "5":
        log_habit(conn)
        return True
    elif choice == "6":
        view_habit_logs(conn)
        return True
    elif choice == "7":
        Statistics_Menu()
        subchoice = input("--> ")
        handle_statistics_menu_input(subchoice)
        return True
    elif choice == "8":
        view_alerts(conn)
        return True
    elif choice in "qQ":
        return False
    else:
        return True

def handle_statistics_menu_input(choice):
    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice in "qQ":
        pass


def Main_Menu():
    print("Main Menu:\n",
          "1. Enter daily health data\n",
          "2. View all health data\n",
          "3. Create new habit\n",
          "4. List all habits\n",
          "5. Log daily habit\n",
          "6. View habits log\n",
          "7. View statistics\n",
          "8. View alerts\n",
          "Q. Quit\n")
    
def Statistics_Menu():
    print("Statistics:\n",
          "1. Your health summary\n",
          "2. Your average sleep /night\n",
          "3. Your sleep impact")
    print("Habits:\n",
          "4. Your high streaks")
    print("Q. Go Back!\n")


def init_db(conn, db_name: str) -> None:
    cur = conn.cursor()
    cur.execute(
        f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    cur.execute(f"USE `{db_name}`")
    cur.close()
    print("Created database")

def init_schema(conn, db_name: str) -> None:
    cur = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS habits (
        habit_id   INT AUTO_INCREMENT PRIMARY KEY,
        habit_name VARCHAR(100) NOT NULL,
        entry_date DATE         NOT NULL DEFAULT (CURDATE()),
        notes      VARCHAR(255)
    )
    """
    cur.execute(query)

    query = """
    CREATE TABLE IF NOT EXISTS habit_logs(
	habit_log_id INT AUTO_INCREMENT PRIMARY KEY, 
    habit_id INT NOT NULL,
    entry_date DATE NOT NULL DEFAULT (CURDATE()),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (habit_id, entry_date),
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
    )
    """
    cur.execute(query)

    query = """
    CREATE TABLE IF NOT EXISTS daily_entries(
    entry_date DATE NOT NULL PRIMARY KEY DEFAULT (CURDATE()),
    hours_slept INT NOT NULL,
    mood_level INT NOT NULL,
    stress_level INT NOT NULL,
    energy_level INT NOT NULL,
    notes VARCHAR(255)
    )
    """
    cur.execute(query)

    query = """
    CREATE TABLE IF NOT EXISTS alerts(
    entry_date DATE DEFAULT (CURDATE()),
    alert_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    alert_type VARCHAR(100) NOT NULL,
    alert_message VARCHAR(255) NOT NULL
    )
    """
    cur.execute(query)
    cur.close()
    print("Created tables")

def populate_tables(conn):
    seed_mental_health_tracker.insert_habits(conn)
    seed_mental_health_tracker.insert_daily_entries(conn)
    seed_mental_health_tracker.insert_habit_logs(conn)
    seed_mental_health_tracker.insert_alerts(conn)
    print("Populated tables")

def create_views(conn):
    cur = conn.cursor()

    query = """
    create or replace view habit_date_completion as
    select h.habit_id, h.habit_name, hl.entry_date
    from habits h  join habit_logs hl
    where h.habit_id = hl.habit_id and hl.completed = true
    order by hl.entry_date asc
    """
    cur.execute(query)
    cur.close()

def create_procedures(conn):
    cur = conn.cursor()
    cur.execute("drop procedure if exists get_habit_logs_for_habit")
    conn.commit()
    query = """
    create procedure get_habit_logs_for_habit(in p_habit_id int)
    begin
	select h.habit_name, hl.entry_date, hl.completed
    from habits h
    join habit_logs hl on hl.habit_id = h.habit_id
    where hl.habit_id = p_habit_id
    order by entry_date;
    end 
    """
    cur.execute(query)
    conn.commit()

    cur.execute("drop procedure if exists summary")
    conn.commit()
    query = """
    CREATE PROCEDURE summary (IN p_days INT)
    BEGIN
    SELECT
    COUNT(*) AS nr_of_entries,
    ROUND(AVG(hours_slept), 1) AS avg_sleep,
    ROUND(AVG(mood_level), 1) AS avg_mood,
    ROUND(AVG(stress_level), 1) AS avg_stress,
    ROUND(AVG(energy_level), 1) AS avg_energy,
    (
        SELECT COUNT(*)
        FROM habit_date_completion
        WHERE entry_date >= CURDATE() - INTERVAL p_days DAY
    ) AS total_habits_logged
    FROM daily_entries
    WHERE entry_date >= CURDATE() - INTERVAL p_days DAY;
    END
    """
    cur.execute(query)
    conn.commit()
    cur.close()

    print("Created procedures")

def create_functions(conn):
    cur = conn.cursor()
    cur.execute("drop function if exists get_highest_streak")
    query = """
            create function get_highest_streak(p_habit_id int)
                returns int
                deterministic
            begin
    	declare \
            max_streak int default 0;
            select coalesce(max(streak_length), 0) \
            into max_streak
            from (select count(*) as streak_length \
                  from (select entry_date, date_sub(entry_date, interval row_number() over (order by entry_date) day) as grp \
                        from habit_date_completion \
                        where habit_id = p_habit_id \
                          and completed = true) as grouped_days \
                  group by grp) as streaks;
            return max_streak;
            end \
            """
    cur.execute(query)
    conn.commit()

    cur.execute("drop function if exists avg_hours_of_sleep")
    query = """
    CREATE FUNCTION avg_hours_of_sleep()
    RETURNS DECIMAL (3,1)
    DETERMINISTIC 
    BEGIN 
    DECLARE avg_hours DECIMAL(3,1);
    SELECT ROUND(AVG(hours_slept), 1) into avg_hours
    FROM daily_entries;        
    RETURN avg_hours;
    END
    """
    cur.execute(query)

    cur.execute("drop function if exists get_low_sleep_streak")
    query = """
    create function get_low_sleep_streak(p_entry_date DATE)
    returns int
    deterministic
    begin
        declare streak int default 0;
    
        with recursive streak_dates as (
            select entry_date
            from daily_entries
            where entry_date = p_entry_date
              and hours_slept < 6
    
            union all
    
            select d.entry_date
            from daily_entries d
            join streak_dates sd
              on d.entry_date = date_sub(sd.entry_date, interval 1 day)
            where d.hours_slept < 6
        )
        select count(*)
        into streak
        from streak_dates;
    
        return streak;
    end
    """
    cur.execute(query)
    conn.commit()

    print("Created functions")

def create_triggers(conn):
    cur = conn.cursor()
    cur.execute("drop trigger if exists low_sleep_alert")
    query = """
    create trigger low_sleep_alert
    after update on daily_entries
    for each row
    begin
	declare consecutive_days int default 0;
	if new.hours_slept < 6 then
		set consecutive_days = get_low_sleep_streak(new.entry_date);
		if consecutive_days >= 3 then 
			insert into alerts(entry_date, alert_type, alert_message)
            values(new.entry_date, "Low sleep streak", concat(consecutive_days, " days with low sleep"));
		end if;
	end if;
    end
    """
    cur.execute(query)

    conn.commit()
    print("Created triggers")

def setup_database():
    conn = get_connection()
    init_db(conn, DB_NAME)
    init_schema(conn, DB_NAME)
    populate_tables(conn)
    create_views(conn)
    create_procedures(conn)
    create_functions(conn)
    create_triggers(conn)
    return conn



if __name__ == '__main__':
    main()

