INSERT OR IGNORE INTO Togoppsett (Togoppsettnavn)
VALUES
('ToSitte'),
('EnSitteEnSove'),
('EnSitte');

INSERT OR IGNORE INTO Vogn (Vognnummer, Togoppsett, AvType)
VALUES
(1, 'ToSitte', 'SJ-sittevogn-1'),
(2, 'ToSitte', 'SJ-sittevogn-1'),
(1, 'EnSitteEnSove', 'SJ-sittevogn-1'),
(2, 'EnSitteEnSove', 'SJ-sovevogn-1'),
(1, 'EnSitte', 'SJ-sittevogn-1');

-- Togrute 1
INSERT OR IGNORE INTO Togrute (TogruteID, Operatør, Togoppsett, Mandag, Tirsdag, Onsdag, Torsdag, Fredag, Lørdag, Søndag)
VALUES ('Togrute1', 'SJ', 'ToSitte', TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE);

INSERT OR IGNORE INTO Togrutetabell (TogruteID, Stasjonnummer, Stasjon, Ankomst, Avgang)
VALUES
('Togrute1', 1, 'Trondheim S', '00:00', '07:49'),
('Togrute1', 2, 'Steinkjer', '09:51', '09:51'),
('Togrute1', 3, 'Mosjøen', '13:20', '13:20'),
('Togrute1', 4, 'Mo i Rana', '14:31', '14:31'),
('Togrute1', 5, 'Fauske', '16:49', '16:49'),
('Togrute1', 6, 'Bodø', '17:34', '00:00');

-- Togrute 2
INSERT OR IGNORE INTO Togrute (TogruteID, Operatør, Togoppsett, Mandag, Tirsdag, Onsdag, Torsdag, Fredag, Lørdag, Søndag)
VALUES ('Togrute2', 'SJ', 'EnSitteEnSove', TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);

INSERT OR IGNORE INTO Togrutetabell (TogruteID, Stasjonnummer, Stasjon, Ankomst, Avgang)
VALUES
('Togrute2', 1, 'Trondheim S', '00:00', '23:05'),
('Togrute2', 2, 'Steinkjer', '00:57', '00:57'),
('Togrute2', 3, 'Mosjøen', '04:41', '04:41'),
('Togrute2', 4, 'Mo i Rana', '05:55', '05:55'),
('Togrute2', 5, 'Fauske', '08:19', '08:19'),
('Togrute2', 6, 'Bodø', '09:05', '00:00');

-- Togrute 3
INSERT OR IGNORE INTO Togrute (TogruteID, Operatør, Togoppsett, Mandag, Tirsdag, Onsdag, Torsdag, Fredag, Lørdag, Søndag)
VALUES ('Togrute3', 'SJ', 'EnSitte', TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE);

INSERT OR IGNORE INTO Togrutetabell (TogruteID, Stasjonnummer, Stasjon, Ankomst, Avgang)
VALUES
('Togrute3', 1, 'Mo i Rana', '00:00', '08:11'),
('Togrute3', 2, 'Mosjøen', '09:14', '09:14'),
('Togrute3', 3, 'Steinkjer', '12:31', '12:31'),
('Togrute3', 4, 'Trondheim S', '14:13', '00:00');