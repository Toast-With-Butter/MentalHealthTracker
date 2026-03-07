CREATE DATABASE IF NOT EXISTS mental_health_tracker;
USE mental_health_tracker;

CREATE TABLE habits(
	habit_id INT AUTO_INCREMENT PRIMARY KEY,
	habit_name VARCHAR(100) NOT NULL,
    entry_date DATE NOT NULL DEFAULT (CURDATE()),
    notes VARCHAR(255) NULL
    );

CREATE TABLE habit_logs(
	habit_log_id INT AUTO_INCREMENT PRIMARY KEY, 
    habit_id INT NOT NULL,
    entry_date DATE NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (habit_id, entry_date),
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
    );


insert into habits (habit_name, entry_date, notes)
value
("2 km run", "2026-03-01", "A run in the forest"),
("Crochet", "2026-03-01", "Making a sweater"),
("Reading", "2026-03-02", "Just one more chapter!");

insert into habit_logs(habit_id, entry_date, completed)
values
(1, "2026-03-01", true),
(1, "2026-03-02", true),
(1, "2026-03-03", true),
(1, "2026-03-04", true),
(1, "2026-03-05", true),
(1, "2026-03-06", true),
(1, "2026-03-07", true),
(1, "2026-03-08", true),
(2, "2026-03-03", true),
(2, "2026-03-04", true),
(2, "2026-03-05", true),
(2, "2026-03-07", true),
(3, "2026-03-01", true),
(3, "2026-03-04", true),
(3, "2026-03-05", true),
(3, "2026-03-08", true);

create or replace view habit_date_completion as 
select h.habit_id, h.habit_name, hl.entry_date, hl.completed
from habits h 
join habit_logs hl
where h.habit_id = hl.habit_id and hl.completed = true
order by hl.entry_date asc;

delimiter //
create function get_highest_streak(p_habit_id int)
returns int 
deterministic 
begin
	declare max_streak int default 0;
    select coalesce(max(streak_length), 0)  into max_streak
    from (
		select count(*) as streak_length
        from(
			select entry_date, date_sub(entry_date,	interval row_number() over (order by entry_date) day) as grp
			from habit_date_completion
			where habit_id = p_habit_id	and completed = true) as grouped_days
		group by grp
	) as streaks;
    return max_streak;
end //
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

create or replace view average_moods as
SELECT 
	entry_date,
    AVG(hours_slept) AS avg_sleep,
    AVG(mood_level) AS avg_mood,
    AVG(stress_level) AS avg_stress,
    AVG(energy_level) AS avg_energy
FROM daily_entries
group by entry_date;


DELIMITER //

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

END //

DELIMITER ;