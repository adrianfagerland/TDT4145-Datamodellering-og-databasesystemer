INSERT OR IGNORE INTO Operatør (Operatørnavn)
VALUES
('SJ');

INSERT OR IGNORE INTO VognType (VognTypenavn, Type)
VALUES
('SJ-sittevogn-1', 'Sitte'),
('SJ-sovevogn-1', 'Sove');

-- Insert data into OperatørEierVogntype table
INSERT INTO OperatørEierVogntype (Vogntypenavn, Operatør) VALUES
    ('SJ-sittevogn-1', 'SJ'),
    ('SJ-sovevogn-1', 'SJ'),

-- Insert data into Sete table
INSERT INTO Sete (Setenummer, Sittetypenavn, Radnummer) VALUES
    (1, 'Vogntype2', 1),
    (2, 'Vogntype2', 1),
    (3, 'Vogntype2', 2),
    (4, 'Vogntype2', 2);

-- Insert data into Seng table
INSERT INTO Seng (Sengenummer, Sovetypenavn, Kupenummer) VALUES
    (1, 'Vogntype1', 1),
    (2, 'Vogntype1', 1),
    (3, 'Vogntype1', 2),
    (4, 'Vogntype1', 2);

