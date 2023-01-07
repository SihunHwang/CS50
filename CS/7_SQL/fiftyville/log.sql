-- Keep a log of any SQL queries you execute as you solve the mystery.

--the crime scene description
SELECT * FROM crime_scene_reports WHERE day = 28 AND month = 7 AND street = 'Chamberlin Street';

--the interviews for the crime mentioning the courthouse
SELECT * FROM interviews WHERE day = 28 AND month = 7 AND transcript LIKE '%courthouse%';

--the license plates of the cars exiting that time
SELECT * FROM courthouse_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND minute >= 15 AND minute < 30 AND activity = 'exit';

--the account numbers and amount of money withdrawn
SELECT * FROM atm_transactions WHERE year = 2020 AND day = 28 AND month = 7 AND transaction_type = 'withdraw' AND atm_location = 'Fifer Street';

--the flights leaving tomorrow from fiftyville
SELECT * FROM flights WHERE year = 2020 AND day = 29 AND month = 7 AND origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') ORDER BY hour, minute LIMIT 1;

--the passport numbers of the passengers of the flight
SELECT * FROM passengers WHERE flight_id = 36;

--people with the passport numbers
SELECT * FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);

--people on the flight with a car present at the courthouse
SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND minute >= 15 AND minute < 30 AND activity = 'exit') AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);

--phone calls less than a min long, caller is in the list
SELECT * FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60 AND caller IN (SELECT phone_number FROM people WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND minute >= 15 AND minute < 30 AND activity = 'exit') AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36));

--account numbers of people in the list
SELECT * FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2020 AND day = 28 AND month = 7 AND transaction_type = 'withdraw' AND atm_location = 'Fifer Street') AND person_id IN (SELECT id FROM people WHERE name IN (SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE day = 28 AND month = 7 AND hour = 10 AND minute >= 15 AND minute < 30 AND activity = 'exit') AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)));

--the destination of the flight
SELECT * FROM airports WHERE id = 4;

--person with whom the theif called
SELECT * FROM people WHERE phone_number = '(375) 555-8161';