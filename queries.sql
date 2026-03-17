CREATE DATABASE IF NOT EXISTS mental_health_tracker;
USE mental_health_tracker;

CREATE TABLE habits(
	user_id INT NOT NULL,
	habit_id INT AUTO_INCREMENT PRIMARY KEY,
	habit_name VARCHAR(100) NOT NULL,
    entry_date DATE NOT NULL DEFAULT (CURDATE()),
    notes VARCHAR(255) NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    );



create table users(
	user_id int auto_increment primary key,
    user_name VARCHAR(255) not null,
    user_email VARCHAR(255)
    );
    
describe daily_entries;
insert into users values (1, 'test_name', 'test_email@test.com');
select * from users;
CREATE TABLE habit_logs(
	user_id INT NOT NULL,
	habit_log_id INT AUTO_INCREMENT PRIMARY KEY, 
    habit_id INT NOT NULL,
    entry_date DATE NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (habit_id, entry_date),
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    );


CREATE TABLE IF NOT EXISTS daily_entries (
	user_id INT NOT NULL,
    entry_date DATE NOT NULL PRIMARY KEY DEFAULT (CURDATE()),
    hours_slept INT NOT NULL,
    mood_level INT NOT NULL,
    stress_level INT NOT NULL,
    energy_level INT NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT user_entry UNIQUE (user_id,entry_date),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS alerts(
	user_id INT NOT NULL,
    entry_date DATE DEFAULT (CURDATE()),
    alert_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    alert_type VARCHAR(100) NOT NULL,
    alert_message VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


create or replace view habit_date_completion as
select h.user_id, h.habit_id, h.habit_name, hl.entry_date, hl.completed
from habits h  join habit_logs hl
where h.habit_id = hl.habit_id and hl.completed = true
order by hl.entry_date asc

delimiter //
create function get_highest_streak(p_habit_id int, p_user_id int)
        returns int
        deterministic
        begin
    	declare
            max_streak int default 0;
            select coalesce(max(streak_length), 0)
            into max_streak
            from (select count(*) as streak_length
                  from (select entry_date, date_sub(entry_date, interval row_number() over (order by entry_date) day) as grp
                        from habit_date_completion
                        where habit_id = p_habit_id and user_id = p_user_id
                          and completed = true) as grouped_days
                  group by grp) as streaks;
            return max_streak;
        end  //
delimiter ;

delimiter //
create procedure get_habit_logs_for_habit(in p_habit_id int)
begin
	select h.habit_name, hl.entry_date, hl.completed
    from habits h
    join habit_logs hl on hl.habit_id = h.habit_id
    where hl.habit_id = p_habit_id
    order by entry_date;
end //
delimiter ;


DELIMITER //

CREATE PROCEDURE summary (IN p_days INT, IN p_user_id INT)
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
    WHERE entry_date >= CURDATE() - INTERVAL p_days DAY AND user_id = p_user_id
) AS total_habits_logged
FROM daily_entries
WHERE entry_date >= CURDATE() - INTERVAL p_days DAY AND user_id = p_user_id;
END //
DELIMITER ;

delimiter //
create function get_low_sleep_streak(p_entry_date DATE, p_user_id INT)
    returns int
    deterministic
    begin
        declare streak int default 0;

        with recursive streak_dates as (
            select entry_date
            from daily_entries
            where entry_date = p_entry_date and user_id = p_user_id
              and hours_slept <= 6

            union all

            select d.entry_date
            from daily_entries d
            join streak_dates sd
              on d.entry_date = date_sub(sd.entry_date, interval 1 day)
            where d.hours_slept <= 6  and user_id = p_user_id
        )
        select count(*)
        into streak
        from streak_dates;

        return streak;
    end //
delimiter ;



delimiter //
create trigger low_sleep_alert
    after insert on daily_entries
    for each row
    begin
	declare consecutive_days int default 0;
	if new.hours_slept <= 6 then
		set consecutive_days = get_low_sleep_streak(new.entry_date, new.user_id);
		if consecutive_days >= 3 then
			insert into alerts(user_id, entry_date, alert_type, alert_message)
            values(new.user_id, new.entry_date, "Low sleep streak", concat(consecutive_days, " days with low sleep"));
		end if;
	end if;
    end //
delimiter ;

DELIMITER //
    CREATE FUNCTION avg_hours_of_sleep(p_user_id int)
    RETURNS DECIMAL (3,1)
    DETERMINISTIC
    BEGIN
    DECLARE avg_hours DECIMAL(3,1);
    SELECT ROUND(AVG(hours_slept), 1) into avg_hours
    FROM daily_entries
    WHERE user_id = p_user_id;
    RETURN avg_hours;
    END//
DELIMITER ;
    