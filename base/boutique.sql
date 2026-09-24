-- =====================================================================
--  Base de données « boutique » utilisée par tous les exercices.
--  Elle est recréée à neuf à chaque vérification : impossible de la casser !
-- =====================================================================

CREATE TABLE clients (
    id               INTEGER PRIMARY KEY,
    prenom           TEXT NOT NULL,
    nom              TEXT NOT NULL,
    ville            TEXT,
    age              INTEGER,
    email            TEXT,
    date_inscription TEXT
);

CREATE TABLE produits (
    id        INTEGER PRIMARY KEY,
    nom       TEXT NOT NULL,
    categorie TEXT NOT NULL,
    prix      REAL NOT NULL,
    stock     INTEGER NOT NULL
);

CREATE TABLE commandes (
    id            INTEGER PRIMARY KEY,
    client_id     INTEGER NOT NULL REFERENCES clients(id),
    date_commande TEXT NOT NULL,
    statut        TEXT NOT NULL
);

CREATE TABLE lignes_commande (
    id          INTEGER PRIMARY KEY,
    commande_id INTEGER NOT NULL REFERENCES commandes(id),
    produit_id  INTEGER NOT NULL REFERENCES produits(id),
    quantite    INTEGER NOT NULL
);

INSERT INTO clients (id, prenom, nom, ville, age, email, date_inscription) VALUES
    (1,  'Alice',   'Martin',   'Paris',     28, 'alice.martin@mail.fr',   '2023-01-15'),
    (2,  'Bruno',   'Durand',   'Lyon',      35, 'bruno.durand@mail.fr',   '2023-02-03'),
    (3,  'Chloé',   'Bernard',  'Marseille', 22, NULL,                     '2023-03-22'),
    (4,  'David',   'Petit',    'Paris',     41, 'david.petit@mail.fr',    '2023-04-10'),
    (5,  'Emma',    'Robert',   'Toulouse',  19, 'emma.robert@mail.fr',    '2023-05-05'),
    (6,  'Fatima',  'Richard',  'Lyon',      30, 'fatima.richard@mail.fr', '2023-06-18'),
    (7,  'Gabriel', 'Moreau',   'Nantes',    55, NULL,                     '2023-07-01'),
    (8,  'Hugo',    'Laurent',  'Paris',     26, 'hugo.laurent@mail.fr',   '2023-08-12'),
    (9,  'Inès',    'Simon',    'Bordeaux',  33, 'ines.simon@mail.fr',     '2023-09-09'),
    (10, 'Jules',   'Michel',   'Lille',     47, 'jules.michel@mail.fr',   '2023-10-30'),
    (11, 'Karim',   'Lefebvre', 'Marseille', 38, NULL,                     '2024-01-07'),
    (12, 'Léa',     'Leroy',    'Paris',     24, 'lea.leroy@mail.fr',      '2024-02-14'),
    (13, 'Mathis',  'Roux',     NULL,        31, 'mathis.roux@mail.fr',    '2024-03-03'),
    (14, 'Nina',    'David',    'Nantes',    29, 'nina.david@mail.fr',     '2024-04-21'),
    (15, 'Oscar',   'Bertrand', 'Lyon',      62, 'oscar.bertrand@mail.fr', '2024-05-30');

INSERT INTO produits (id, nom, categorie, prix, stock) VALUES
    (1,  'Clavier mécanique',   'Informatique', 79.90,  25),
    (2,  'Souris sans fil',     'Informatique', 24.99,  60),
    (3,  'Écran 27 pouces',     'Informatique', 249.00, 8),
    (4,  'Casque audio',        'Informatique', 59.90,  0),
    (5,  'Le Petit Prince',     'Livres',       7.50,   120),
    (6,  'Apprendre le SQL',    'Livres',       34.00,  15),
    (7,  'Harry Potter tome 1', 'Livres',       8.90,   80),
    (8,  'Lampe de bureau',     'Maison',       32.50,  40),
    (9,  'Cafetière',           'Maison',       45.00,  12),
    (10, 'Plaid polaire',       'Maison',       19.90,  0),
    (11, 'Ballon de football',  'Sport',        22.00,  35),
    (12, 'Tapis de yoga',       'Sport',        29.90,  18),
    (13, 'Haltères 5 kg',       'Sport',        39.00,  5),
    (14, 'Jeu d''échecs',       'Jeux',         25.00,  10),
    (15, 'Puzzle 1000 pièces',  'Jeux',         14.90,  22),
    (16, 'Monopoly',            'Jeux',         29.99,  7);

INSERT INTO commandes (id, client_id, date_commande, statut) VALUES
    (1,  1,  '2024-01-10', 'livrée'),
    (2,  2,  '2024-01-15', 'livrée'),
    (3,  1,  '2024-02-02', 'livrée'),
    (4,  3,  '2024-02-20', 'annulée'),
    (5,  4,  '2024-03-05', 'livrée'),
    (6,  5,  '2024-03-18', 'livrée'),
    (7,  2,  '2024-04-01', 'livrée'),
    (8,  6,  '2024-04-12', 'annulée'),
    (9,  8,  '2024-05-07', 'livrée'),
    (10, 9,  '2024-05-25', 'livrée'),
    (11, 1,  '2024-06-14', 'livrée'),
    (12, 10, '2024-07-03', 'livrée'),
    (13, 12, '2024-08-19', 'livrée'),
    (14, 4,  '2024-09-09', 'en cours'),
    (15, 14, '2024-10-02', 'livrée'),
    (16, 8,  '2024-11-11', 'en cours'),
    (17, 2,  '2024-12-05', 'en cours'),
    (18, 15, '2024-12-20', 'en cours');

INSERT INTO lignes_commande (id, commande_id, produit_id, quantite) VALUES
    (1,  1,  1,  1),
    (2,  1,  2,  1),
    (3,  2,  5,  2),
    (4,  2,  7,  1),
    (5,  3,  6,  1),
    (6,  4,  3,  1),
    (7,  5,  3,  2),
    (8,  5,  8,  1),
    (9,  6,  11, 3),
    (10, 6,  12, 1),
    (11, 7,  9,  1),
    (12, 8,  14, 1),
    (13, 9,  4,  1),
    (14, 9,  2,  2),
    (15, 10, 15, 2),
    (16, 10, 16, 1),
    (17, 11, 5,  3),
    (18, 12, 1,  1),
    (19, 12, 3,  1),
    (20, 13, 7,  2),
    (21, 13, 12, 1),
    (22, 14, 9,  1),
    (23, 14, 8,  2),
    (24, 15, 14, 1),
    (25, 15, 15, 1),
    (26, 16, 11, 1),
    (27, 17, 6,  2),
    (28, 18, 16, 1),
    (29, 18, 2,  1);
