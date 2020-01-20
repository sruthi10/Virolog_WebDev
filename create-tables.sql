-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema blastoutput
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema blastoutput
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `blastoutput` DEFAULT CHARACTER SET utf8 ;
USE `blastoutput` ;

-- -----------------------------------------------------
-- Table `blastoutput`.`hits`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `blastoutput`.`hits` ;

CREATE TABLE IF NOT EXISTS `blastoutput`.`hits` (
  `num` INT(11) NOT NULL,
  `id` VARCHAR(100) NOT NULL,
  `def` TEXT(30000) NULL DEFAULT NULL,
  `accession` VARCHAR(45) NOT NULL,
  `len` INT(11) NULL DEFAULT NULL,
  INDEX `accession_index` (`accession` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `blastoutput`.`iteration`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `blastoutput`.`iteration` ;

CREATE TABLE IF NOT EXISTS `blastoutput`.`iteration` (
  `iter-num` INT(11) NOT NULL,
  `query-ID` VARCHAR(45) NOT NULL,
  `query-def` TEXT(30000) NULL DEFAULT NULL,
  `query-len` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`iter-num`),
  INDEX `iteration_index` (`query-ID` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `blastoutput`.`hsp`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `blastoutput`.`hsp` ;

CREATE TABLE IF NOT EXISTS `blastoutput`.`hsp` (
  `num` INT(11) NOT NULL,
  `bit-score` DOUBLE NULL DEFAULT NULL,
  `score` INT(11) NULL DEFAULT NULL,
  `evalue` DOUBLE NULL DEFAULT NULL,
  `query-from` INT(11) NULL DEFAULT NULL,
  `query-to` INT(11) NULL DEFAULT NULL,
  `hit-from` INT(11) NULL DEFAULT NULL,
  `hit-to` INT(11) NULL DEFAULT NULL,
  `query-frame` INT(11) NULL DEFAULT NULL,
  `hit-frame` INT(11) NULL DEFAULT NULL,
  `identity` INT(11) NULL DEFAULT NULL,
  `positive` INT(11) NULL DEFAULT NULL,
  `gaps` INT(11) NULL DEFAULT NULL,
  `align-len` INT(11) NULL DEFAULT NULL,
  `qseq` VARCHAR(1000) NULL DEFAULT NULL,
  `hseq` VARCHAR(1000) NULL DEFAULT NULL,
  `midline` VARCHAR(1000) NULL DEFAULT NULL,
  `hit_accession` VARCHAR(45) NULL DEFAULT NULL,
  `iteration_query-ID` VARCHAR(45) NULL DEFAULT NULL,
  `iteration_num` INT(11) NOT NULL,
  INDEX `hsp_index_hits` (`hit_accession` ASC),
  INDEX `hsp_index_iteration` (`iteration_query-ID` ASC),
  INDEX `hsp_index_iteration-num` (`iteration_num` ASC),
  CONSTRAINT `FK_hits`
    FOREIGN KEY (`hit_accession`)
    REFERENCES `blastoutput`.`hits` (`accession`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_iteration-query-id`
    FOREIGN KEY (`iteration_query-ID`)
    REFERENCES `blastoutput`.`iteration` (`query-ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_iteration-num`
    FOREIGN KEY (`iteration_num`)
    REFERENCES `blastoutput`.`iteration` (`iter-num`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `blastoutput`.`statistics`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `blastoutput`.`statistics` ;

CREATE TABLE IF NOT EXISTS `blastoutput`.`statistics` (
  `iteration_num-stat` INT(11) NOT NULL,
  `db-num` INT(11) NULL,
  `db-len` INT(11) NULL,
  `hsp-len` INT(11) NULL,
  `eff-space` INT(11) NULL,
  `kappa` DOUBLE NULL,
  `lambda` DOUBLE NULL,
  `entropy` DOUBLE NULL,
  CONSTRAINT `FK_iteration-num-stat`
    FOREIGN KEY (`iteration_num-stat`)
    REFERENCES `blastoutput`.`iteration` (`iter-num`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- replace my paths with the paths to your own files --

LOAD DATA LOCAL INFILE 'C:\\Users\\trevs\\OneDrive\\programming\\python\\undergrad_research\\undergrad-research\\create_iteration.csv'
INTO TABLE `blastoutput`.`iteration`;

LOAD DATA LOCAL INFILE 'C:\\Users\\trevs\\OneDrive\\programming\\python\\undergrad_research\\undergrad-research\\create_hits.csv'
INTO TABLE `blastoutput`.`hits`;

LOAD DATA LOCAL INFILE 'C:\\Users\\trevs\\OneDrive\\programming\\python\\undergrad_research\\undergrad-research\\create_statistics.csv'
INTO TABLE `blastoutput`.`statistics`;

LOAD DATA LOCAL INFILE 'C:\\Users\\trevs\\OneDrive\\programming\\python\\undergrad_research\\undergrad-research\\create_hsp.csv'
INTO TABLE `blastoutput`.`hsp`;
