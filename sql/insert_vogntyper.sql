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

