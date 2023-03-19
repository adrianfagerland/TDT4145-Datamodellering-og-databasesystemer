CREATE TABLE IF NOT EXISTS Stasjon (
    Stasjonnavn VARCHAR(50) NOT NULL,
    Moh INT NOT NULL,
    PRIMARY KEY (Stasjonnavn),
    CHECK (Moh >= 0)
);
CREATE TABLE IF NOT EXISTS Banestrekning (
    Banestrekningnavn VARCHAR(50) NOT NULL,
    Fremdriftsenergi VARCHAR(50) NOT NULL,
    PRIMARY KEY (Banestrekningnavn),
    CHECK (Fremdriftsenergi IN ('Elektrisk', 'Diesel'))
);
CREATE TABLE IF NOT EXISTS Delstrekning (
    DelstrekningID VARCHAR(50) NOT NULL,
    Lengde INT NOT NULL,
    Sportype VARCHAR(50) NOT NULL,
    Banestrekningnavn VARCHAR(50) NOT NULL,
    Startstasjon VARCHAR(50) NOT NULL,
    Sluttstasjon VARCHAR(50) NOT NULL,
    PRIMARY KEY (DelstrekningID),
    FOREIGN KEY (Banestrekningnavn) REFERENCES Banestrekning(Banestrekningnavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Startstasjon) REFERENCES Stasjon(Stasjonnavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Sluttstasjon) REFERENCES Stasjon(Stasjonnavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (Lengde >= 0),
    CHECK (Sportype IN ('Enkel', 'Dobbel'))
);
CREATE TABLE IF NOT EXISTS Operatør (
    Operatørnavn VARCHAR(50) NOT NULL,
    PRIMARY KEY (Operatørnavn)
);
CREATE TABLE IF NOT EXISTS Vogntype (
    Vogntypenavn VARCHAR(50) NOT NULL,
    Type VARCHAR(50) NOT NULL,
    PRIMARY KEY (Vogntypenavn),
    CHECK (Type IN ('Sitte', 'Sove'))
);
CREATE TABLE IF NOT EXISTS Sete (
    Setenummer INT NOT NULL,
    Sittetypenavn VARCHAR(50) NOT NULL,
    Radnummer INT NOT NULL,
    PRIMARY KEY (Setenummer, Sittetypenavn),
    FOREIGN KEY (Sittetypenavn) REFERENCES Vogntype(Vogntypenavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (Radnummer >= 0),
    CHECK (Setenummer >= 0)
);
CREATE TABLE IF NOT EXISTS Seng (
    Sengenummer INT NOT NULL,
    Sovetypenavn VARCHAR(50) NOT NULL,
    Kupenummer INT NOT NULL,
    PRIMARY KEY (Sengenummer, Sovetypenavn),
    FOREIGN KEY (Sovetypenavn) REFERENCES Vogntype(Vogntypenavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (Kupenummer >= 0),
    CHECK (Sengenummer >= 0)
);
CREATE TABLE IF NOT EXISTS OperatørEierVogntype (
    Vogntypenavn VARCHAR(50) NOT NULL,
    Operatør VARCHAR(50) NOT NULL,
    PRIMARY KEY (Vogntypenavn, Operatør),
    FOREIGN KEY (Vogntypenavn) REFERENCES Vogntype(Vogntypenavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Operatør) REFERENCES Operatør(Operatørnavn) ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS Togoppsett (
    Togoppsettnavn VARCHAR(50) NOT NULL,
    PRIMARY KEY (Togoppsettnavn)
);
CREATE TABLE IF NOT EXISTS Vogn (
    Vognnummer INT NOT NULL,
    Togoppsett VARCHAR(50) NOT NULL,
    AvType VARCHAR(50) NOT NULL,
    PRIMARY KEY (Vognnummer, Togoppsett),
    FOREIGN KEY (Togoppsett) REFERENCES Togoppsett(Togoppsettnavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (AvType) REFERENCES Vogntype(Vogntypenavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (Vognnummer >= 0)
);
CREATE TABLE IF NOT EXISTS Togrute (
    TogruteID VARCHAR(50) NOT NULL,
    Operatør VARCHAR(50) NOT NULL,
    Togoppsett VARCHAR(50) NOT NULL,
    Mandag BOOLEAN NOT NULL,
    Tirsdag BOOLEAN NOT NULL,
    Onsdag BOOLEAN NOT NULL,
    Torsdag BOOLEAN NOT NULL,
    Fredag BOOLEAN NOT NULL,
    Lørdag BOOLEAN NOT NULL,
    Søndag BOOLEAN NOT NULL,
    PRIMARY KEY (TogruteID),
    FOREIGN KEY (Operatør) REFERENCES Operatør(Operatørnavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Togoppsett) REFERENCES Togoppsett(Togoppsettnavn) ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS Togrutetabell (
    TogruteID VARCHAR(50) NOT NULL,
    Stasjonnummer INT NOT NULL,
    Stasjon VARCHAR(50) NOT NULL,
    Ankomst VARCHAR(50) NOT NULL,
    Avgang VARCHAR(50) NOT NULL,
    PRIMARY KEY (TogruteID, Stasjonnummer),
    FOREIGN KEY (Stasjon) REFERENCES Stasjon(Stasjonnavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (Stasjonnummer >= 0)
);
CREATE TABLE IF NOT EXISTS Togruteforekomst (
    Rute VARCHAR(50) NOT NULL,
    Togruteforekomstdato DATE NOT NULL,
    PRIMARY KEY (Rute, Togruteforekomstdato),
    FOREIGN KEY (Rute) REFERENCES Togrutetabell(TogruteID) ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS Kunde (
    Kundenummer INT PRIMARY KEY,
    Kundenavn VARCHAR(50) NOT NULL,
    Epostadresse VARCHAR(100) UNIQUE,
    Mobilnummer VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS Kundeordre (
    Kundeordrenummer INT PRIMARY KEY,
    Kunde INT NOT NULL,
    Rute VARCHAR(50) NOT NULL,
    Reisedato DATE NOT NULL,
    Kjøpsdato DATE NOT NULL,
    Kjøpstidspunkt TIME NOT NULL,
    FOREIGN KEY (Kunde) REFERENCES Kunde(Kundenummer) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Rute, Reisedato) REFERENCES Togruteforekomst(Rute, Togruteforekomstdato) ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS Billett (
    BillettID VARCHAR(50) NOT NULL,
    Påstigning VARCHAR(50) NOT NULL,
    Avstigning VARCHAR(50) NOT NULL,
    Ordrenummer INT NOT NULL,
    Vogn INT NOT NULL,
    Togoppsett VARCHAR(50) NOT NULL,
    PRIMARY KEY (BillettID),
    FOREIGN KEY (Påstigning) REFERENCES Stasjon(Stasjonnavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Avstigning) REFERENCES Stasjon(Stasjonnavn) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Ordrenummer) REFERENCES Kundeordre(Kundeordrenummer) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Vogn, Togoppsett) REFERENCES Vogn(Vognnummer, Togoppsett) ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS Setebillett (
    BillettID VARCHAR(50) NOT NULL,
    Setenummer INT NOT NULL,
    Vogntypenavn VARCHAR(50) NOT NULL,
    PRIMARY KEY (BillettID),
    FOREIGN KEY (BillettID) REFERENCES Billett(BillettID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Setenummer, Vogntypenavn) REFERENCES Sete(Setenummer, Sittetypenavn) ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS Sengebillett (
    BillettID VARCHAR(50) NOT NULL,
    Sengenummer INT NOT NULL,
    Vogntypenavn VARCHAR(50) NOT NULL,
    PRIMARY KEY (BillettID),
    FOREIGN KEY (BillettID) REFERENCES Billett(BillettID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Sengenummer, Vogntypenavn) REFERENCES Seng(Sengenummer, Sovetypenavn) ON DELETE RESTRICT ON UPDATE CASCADE
);