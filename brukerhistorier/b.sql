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