INSERT OR IGNORE INTO Kunde(Kundenummer, Kundenavn, Epostadresse, Mobilnummer)
VALUES 
(1, 'Kunde1', 'a@a.com', 12345678),
(2, 'Kunde2', 'b@b.com', 87654321);

INSERT OR IGNORE INTO Kundeordre(Kundeordrenummer, Kunde, Rute, Reisedato, Kjøpsdato, Kjøpstidspunkt)
VALUES
(1, 1, 'TrondheimSBodøMorgen', '2023-04-03', '2021-04-03', '12:00:00'),
(2, 1, 'TrondheimSBodøMorgen', '2023-04-04', '2021-04-03', '12:00:00'),
(3, 1, 'TrondheimSBodøNatt', '2023-04-03', '2021-04-03', '12:00:00'),
(4, 2, 'TrondheimSBodøNatt', '2023-04-03', '2021-04-03', '12:00:00'),
(5, 2, 'MoiRanaTrondheimSMorgen', '2023-04-03', '2021-04-03', '12:00:00');

INSERT OR IGNORE INTO Billett(BillettID, Påstigning, Avstigning, Ordrenummer, Vogn, Togoppsett)
VALUES
(1, 'Trondheim S', 'Bodø', 1, 1, 'ToSitte'),
(2, 'Trondheim S', 'Bodø', 2, 2, 'ToSitte'),
(3, 'Trondheim S', 'Bodø', 2, 3, 'EnSitteEnSove'),
(4, 'Trondheim S', 'Bodø', 2, 4, 'EnSitteEnSove'),
(5, 'Mo i Rana', 'Trondheim S', 3, 1, 'ToSitte'),
(6, 'Mo i Rana', 'Trondheim S', 4, 1, 'ToSitte'),
(7, 'Trondheim S', 'Bodø', 5, 1, 'ToSitte');

INSERT OR IGNORE INTO Setebillett(BillettID, Setenummer, Vogntypenavn)
VALUES
(1, 1, 'ToSitte'),
(2, 2, 'ToSitte'),
(5, 1, 'ToSitte'),
(6, 2, 'ToSitte'),
(7, 1, 'ToSitte');

INSERT OR IGNORE INTO Sengebillett(BillettID, Sengenummer, Vogntypenavn)
VALUES
(3, 1, 'EnSitteEnSove'),
(4, 2, 'EnSitteEnSove');