
CREATE TABLE `Entry` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`  TEXT NOT NULL,
	`entry` TEXT NOT NULL,
	`date` DATE NOT NULL,
	`mood_id` INTEGER NOT NULL,
	FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Mood` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label`  TEXT NOT NULL
);

INSERT INTO `Mood` VALUES (null, 'Happy');
INSERT INTO `Mood` VALUES (null, 'Sad');
INSERT INTO `Mood` VALUES (null, 'Mad');
INSERT INTO `Mood` VALUES (null, 'Frustrated');

INSERT INTO `Entry` VALUES (null, 'API', 'Such a wonderful time learning apis', '2021-01-28', 1);
INSERT INTO `Entry` VALUES (null, 'JSON', 'Such a horrible time understanding json', '2021-02-14', 2);
INSERT INTO `Entry` VALUES (null, 'SQL', 'Such a horrible time learning SQL queries', '2021-03-12', 2);
INSERT INTO `Entry` VALUES (null, 'React', 'I love react', '2021-03-20', 1);
SELECT *
FROM entry
WHERE entry LIKE '%horr%'

CREATE TABLE `Tag` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`  TEXT NOT NULL
);

CREATE TABLE `Entry_tag` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`entry_id`  INTEGER NOT NULL,
	`tag_id`  INTEGER NOT NULL,
	FOREIGN KEY(`entry_id`) REFERENCES `Entry`(`id`),
	FOREIGN KEY(`tag_id`) REFERENCES `Tag`(`id`)
);

INSERT INTO `Tag` VALUES (null, 'SQL');
INSERT INTO `Tag` VALUES (null, 'Json');
INSERT INTO `Tag` VALUES (null, 'api');
INSERT INTO `Tag` VALUES (null, 'javascript');
INSERT INTO `Tag` VALUES (null, 'react');
SELECT 
e.id,
e.tag_id,
e.entry_id,
t.name
FROM Entry_tag e
JOIN tag t ON t.id = e.tag_id
WHERE e.entry_id = 11
            