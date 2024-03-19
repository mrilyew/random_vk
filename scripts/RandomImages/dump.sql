CREATE TABLE scripts_data.vk_posts (
	id BIGINT UNSIGNED auto_increment NOT NULL,
	content LONGTEXT NULL,
	virtual_id VARCHAR(300) NULL,
	attachments_count TINYINT(11) NULL,
	CONSTRAINT vk_posts_pk PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

CREATE TABLE scripts_data.vk_photos (
	id BIGINT UNSIGNED auto_increment NOT NULL,
	url MEDIUMTEXT NULL,
	`date` BIGINT UNSIGNED NULL,
	virtual_id varchar(200) NULL,
	CONSTRAINT vk_photos_pk PRIMARY KEY (id)
)

ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

ALTER TABLE scripts_data.vk_photos ADD post varchar(200) NULL;
