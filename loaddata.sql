-- Create Users table
CREATE TABLE IF NOT EXISTS "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit,
  "is_staff" INTEGER DEFAULT 0
);

-- Promote the first user to admin
UPDATE Users SET is_staff = 1 WHERE id = 1;

-- Create DemotionQueue table
CREATE TABLE IF NOT EXISTS "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);

-- Create Subscriptions table
CREATE TABLE IF NOT EXISTS "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

-- Create Posts table
CREATE TABLE IF NOT EXISTS "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  -- approved: -1 = rejected, 0 = pending, 1 = approved
  "approved" INTEGER DEFAULT 0,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

-- Create Comments table
CREATE TABLE IF NOT EXISTS "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  "created_on" date,
  "subject" TEXT,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

-- Create Reactions table
CREATE TABLE IF NOT EXISTS "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

-- Create PostReactions table
CREATE TABLE IF NOT EXISTS "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

-- Create Tags table
CREATE TABLE IF NOT EXISTS "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

-- Create PostTags table
CREATE TABLE IF NOT EXISTS "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

-- Create Categories table
CREATE TABLE IF NOT EXISTS "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

-- Seed starter data
INSERT INTO Categories ("label") VALUES ('News');
INSERT INTO Tags ("label") VALUES ('JavaScript');
INSERT INTO Reactions ("label", "image_url") VALUES
  ('like', 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f44d.png'),
  ('laugh', 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f602.png'),
  ('fire', 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f525.png'),
  ('wow', 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f62e.png');

INSERT INTO Reactions (label, image_url) VALUES
  ('like', '/images/+1.png'),
  ('laugh', '/images/rolling_on_the_floor_laughing.png'),
  ('fire', '/images/fire.png'),
  ('wow', '/images/open_mouth.png');

INSERT INTO Reactions (label, image_url) VALUES
  ('like', '/images/thumbs_up.png'),
  ('laugh', '/images/rolling_on_the_floor_laughing.png'),
  ('fire', '/images/fire.png'),
  ('wow', '/images/open_mouth.png');

TRUNCATE TABLE Reactions;

DELETE FROM Reactions
WHERE label = 'wow';

INSERT INTO Users (
  "first_name", "last_name", "email", "bio", "username", "password", "profile_image_url", "created_on", "active"
) VALUES (
  'John', 'Doe', 'john.doe@email.com', 'Sample bio', 'johndoe', 'password123', 'http://example.com/image.jpg', '2025-06-16', 1
);

-- Add more categories
INSERT INTO Categories ("label") VALUES
  ('Science'),
  ('Technology'),
  ('Art'),
  ('Sports'),
  ('Philosophy'),
  ('Economics'),
  ('Health'),
  ('Travel'),
  ('Food'),
  ('Education'),
  ('History'),
  ('Literature'),
  ('Music'),
  ('Politics'),
  ('Environment'),
  ('Business'),
  ('Fashion'),
  ('Movies'),
  ('Gaming'),
  ('DIY');


ALTER TABLE Users RENAME COLUMN isStaff TO is_staff;

ALTER TABLE Users ADD COLUMN is_staff INTEGER;

UPDATE Users SET is_staff = 1;

ALTER TABLE Users ALTER COLUMN is_staff SET DEFAULT 1;


UPDATE Posts
SET approved = 1;