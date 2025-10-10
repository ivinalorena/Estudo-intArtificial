/*EXERCICIOS BASICOS DE SQL
1. diferente em sql é <> ou !=
2. basicos de sql: SELECT, FROM, WHERE, AND, OR, NOT, IN, BETWEEN, LIKE, IS NULL
3. deletar tabela: DROP TABLE table_name;
4. deletar dados: DELETE FROM table_name WHERE condition;
*/
--Find the available seats on the bus by filtering the bus_seats table 
--where available is not equal to 0. Only show the type and price columns.
SELECT type, price
FROM bus_seats
WHERE available <> 0;
--Help a customer see the train 
--seats from train_seats table where type is not equal to Middle.
SELECT *
from train_seats
WHERE type <> 'Middle';
--Help a customer see a cheaper phone from device_offer table, 
--by selecting only those with a price of less than $10000.
SELECT *
from device_offer
where price <10000;
--In a game, a player having 50 EXP (experience) points has to compete with a player with 
--experience points up to 50. Filter the player_stats table to get entries with exp less than or equal to 50.
select * from player_stats 
where exp<=50;
--ind out the players who played more than 50 matches in their lifetime by filtering the cricket_stats table where 
--matches_played is greater than 50. Only select the name column.
select name from cricket_stats
where matches_played > 50;
--Four friends made a last-minute trip plan. Help them find a bus from buses table where seats_available is greater 
--than or equal to 4. Only show name and type.
SELECT name,type
FROM buses
WHERE seats_available >= 4;
--Give the column receipt_number an alias of number.
select receipt_number AS number
from receipts;
--Give the column out_of_stock an alias of empty.
SELECT out_of_stock as empty
FROM ingredients
WHERE out_of_stock = 'yes';
--Give the column employee_number an alias of ID.
SELECT employee_number as ID
FROM employees;
-- Give the column patient_name an alias of name and age an alias of age.
SELECT patient_name AS name, age AS age
FROM appointments;
--Select the column worked_overtime and give an alias of overtime.
SELECT hours_worked AS hours, worked_overtime as overtime
FROM timecards;
--uso do DISTINCT
--Find the different types of vehicles available in the vehicles table.
SELECT DISTINCT type
FROM vehicles;
--Find out a student's best subjects by ordering the result table by 
--the marks column.
select * from result
order by marks;
--Find out the highest number of views for a vlogger by arranging the vlogger table 
--in descending order according to the views column. Display the views column only, with no repetition.
select DISTINCT views
FROM vlogger
order by views DESC;
--A student wants to go for a movie on Friday, their off-day. Filter the movies table for movies 
--where day equals Friday.
SELECT *
FROM movies
WHERE day = 'Friday';
--A customer wants to know the price and condition of available iOS devices. Filter the device_offer 
--table where os equals iOS. Select the price and condition only.
select price, condition
from device_offer
where os ='iOS';