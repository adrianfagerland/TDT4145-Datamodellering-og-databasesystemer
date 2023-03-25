-- Stasjoner
INSERT OR IGNORE INTO Stasjon (Stasjonnavn, Moh) VALUES ('Bodø', 4.1);
INSERT OR IGNORE INTO Stasjon (Stasjonnavn, Moh) VALUES ('Fauske', 34);
INSERT OR IGNORE INTO Stasjon (Stasjonnavn, Moh) VALUES ('Mo i Rana', 3.5);
INSERT OR IGNORE INTO Stasjon (Stasjonnavn, Moh) VALUES ('Mosjøen', 6.8);
INSERT OR IGNORE INTO Stasjon (Stasjonnavn, Moh) VALUES ('Steinkjer', 3.6);
INSERT OR IGNORE INTO Stasjon (Stasjonnavn, Moh) VALUES ('Trondheim S', 5.1);

-- Delstrekninger
INSERT OR IGNORE INTO Delstrekning (DelstrekningID, Lengde, Sportype, Banestrekningnavn, Startstasjon, Sluttstasjon) VALUES ('TrondheimS_Steinkjer', 120, 'Dobbel', 'Nordlandsbanen', 'Trondheim S', 'Steinkjer');
INSERT OR IGNORE INTO Delstrekning (DelstrekningID, Lengde, Sportype, Banestrekningnavn, Startstasjon, Sluttstasjon) VALUES ('Steinkjer_Mosjøen', 280, 'Enkel', 'Nordlandsbanen', 'Steinkjer', 'Mosjøen');
INSERT OR IGNORE INTO Delstrekning (DelstrekningID, Lengde, Sportype, Banestrekningnavn, Startstasjon, Sluttstasjon) VALUES ('Mosjøen_MoiRana', 90, 'Enkel', 'Nordlandsbanen', 'Mosjøen', 'Mo i Rana');
INSERT OR IGNORE INTO Delstrekning (DelstrekningID, Lengde, Sportype, Banestrekningnavn, Startstasjon, Sluttstasjon) VALUES ('MoiRana_Fauske', 170, 'Enkel', 'Nordlandsbanen', 'Mo i Rana', 'Fauske');
INSERT OR IGNORE INTO Delstrekning (DelstrekningID, Lengde, Sportype, Banestrekningnavn, Startstasjon, Sluttstasjon) VALUES ('Fauske_Bodø', 60, 'Enkel', 'Nordlandsbanen', 'Fauske', 'Bodø');

-- Banestrekninger
INSERT OR IGNORE INTO Banestrekning (Banestrekningnavn, Fremdriftsenergi) VALUES ('Nordlandsbanen', 'Diesel');
