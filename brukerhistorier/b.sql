INSERT OR IGNORE INTO Operatør (Operatørnavn)
VALUES
('SJ');

INSERT OR IGNORE INTO VognType (VognTypenavn, Type)
VALUES
('SJ-sittevogn-1', 'Sitte'),
('SJ-sovevogn-1', 'Sove');

-- Insert data into OperatørEierVogntype table
INSERT OR IGNORE INTO OperatørEierVogntype (Vogntypenavn, Operatør) VALUES
    ('SJ-sittevogn-1', 'SJ'),
    ('SJ-sovevogn-1', 'SJ');

-- Insert data into Sete table
INSERT OR IGNORE INTO Sete (Setenummer, Sittetypenavn, Radnummer) VALUES
    (1, 'SJ-sittevogn-1', 1),
    (2, 'SJ-sittevogn-1', 1),
    (3, 'SJ-sittevogn-1', 1),
    (4, 'SJ-sittevogn-1', 1),
    (5, 'SJ-sittevogn-1', 2),
    (6, 'SJ-sittevogn-1', 2),
    (7, 'SJ-sittevogn-1', 2),
    (8, 'SJ-sittevogn-1', 2),
    (9, 'SJ-sittevogn-1', 3),
    (10, 'SJ-sittevogn-1', 3),
    (11, 'SJ-sittevogn-1', 3),
    (12, 'SJ-sittevogn-1', 3);


-- Insert data into Seng table
INSERT OR IGNORE INTO Seng (Sengenummer, Sovetypenavn, Kupenummer) VALUES
    (1, 'SJ-sovevogn-1', 1),
    (2, 'SJ-sovevogn-1', 1),
    (3, 'SJ-sovevogn-1', 2),
    (4, 'SJ-sovevogn-1', 2),
    (5, 'SJ-sovevogn-1', 3),
    (6, 'SJ-sovevogn-1', 3),
    (7, 'SJ-sovevogn-1', 4),
    (8, 'SJ-sovevogn-1', 4);


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
VALUES ('TrondheimSBodøMorgen', 'SJ', 'ToSitte', TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE);

INSERT OR IGNORE INTO Togrutetabell (TogruteID, Stasjonnummer, Stasjon, Ankomst, Avgang)
VALUES
('TrondheimSBodøMorgen', 1, 'Trondheim S', '00:00', '07:49'),
('TrondheimSBodøMorgen', 2, 'Steinkjer', '09:51', '09:51'),
('TrondheimSBodøMorgen', 3, 'Mosjøen', '13:20', '13:20'),
('TrondheimSBodøMorgen', 4, 'Mo i Rana', '14:31', '14:31'),
('TrondheimSBodøMorgen', 5, 'Fauske', '16:49', '16:49'),
('TrondheimSBodøMorgen', 6, 'Bodø', '17:34', '00:00');

-- Togrute 2
INSERT OR IGNORE INTO Togrute (TogruteID, Operatør, Togoppsett, Mandag, Tirsdag, Onsdag, Torsdag, Fredag, Lørdag, Søndag)
VALUES ('TrondheimSBodøNatt', 'SJ', 'EnSitteEnSove', TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);

INSERT OR IGNORE INTO Togrutetabell (TogruteID, Stasjonnummer, Stasjon, Ankomst, Avgang)
VALUES
('TrondheimSBodøNatt', 1, 'Trondheim S', '00:00', '23:05'),
('TrondheimSBodøNatt', 2, 'Steinkjer', '00:57+1', '00:57+1'),
('TrondheimSBodøNatt', 3, 'Mosjøen', '04:41+1', '04:41+1'),
('TrondheimSBodøNatt', 4, 'Mo i Rana', '05:55+1', '05:55+1'),
('TrondheimSBodøNatt', 5, 'Fauske', '08:19+1', '08:19+1'),
('TrondheimSBodøNatt', 6, 'Bodø', '09:05+1', '00:00');

-- Togrute 3
INSERT OR IGNORE INTO Togrute (TogruteID, Operatør, Togoppsett, Mandag, Tirsdag, Onsdag, Torsdag, Fredag, Lørdag, Søndag)
VALUES ('MoiRanaTrondheimSMorgen', 'SJ', 'EnSitte', TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE);

INSERT OR IGNORE INTO Togrutetabell (TogruteID, Stasjonnummer, Stasjon, Ankomst, Avgang)
VALUES
('MoiRanaTrondheimSMorgen', 1, 'Mo i Rana', '00:00', '08:11'),
('MoiRanaTrondheimSMorgen', 2, 'Mosjøen', '09:14', '09:14'),
('MoiRanaTrondheimSMorgen', 3, 'Steinkjer', '12:31', '12:31'),
('MoiRanaTrondheimSMorgen', 4, 'Trondheim S', '14:13', '00:00');