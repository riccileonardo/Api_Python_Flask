-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Cursos
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Cursos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Cursos` DEFAULT CHARACTER SET utf8 ;
USE `Cursos` ;

-- -----------------------------------------------------
-- Table `Cursos`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cursos`.`User` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Cursos`.`Trilhas_apredizado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cursos`.`Trilhas_apredizado` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(255) NOT NULL,
  `descricao` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Cursos`.`Cursos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cursos`.`Cursos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(255) NOT NULL,
  `descricao` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Cursos`.`Aulas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cursos`.`Aulas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(255) NOT NULL,
  `descricao` VARCHAR(255) NOT NULL,
  `duracao` INT NOT NULL,
  `id_curso` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Aulas_Cursos1_idx` (`id_curso` ASC) VISIBLE,
  CONSTRAINT `fk_Aulas_Cursos1`
    FOREIGN KEY (`id_curso`)
    REFERENCES `Cursos`.`Cursos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Cursos`.`Comentarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cursos`.`Comentarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `descricao` VARCHAR(255) NOT NULL,
  `id_user` INT NOT NULL,
  `id_curso` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Comentarios_User1_idx` (`id_user` ASC) VISIBLE,
  INDEX `fk_Comentarios_Cursos1_idx` (`id_curso` ASC) VISIBLE,
  CONSTRAINT `fk_Comentarios_User1`
    FOREIGN KEY (`id_user`)
    REFERENCES `Cursos`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Comentarios_Cursos1`
    FOREIGN KEY (`id_curso`)
    REFERENCES `Cursos`.`Cursos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Cursos`.`Avaliacoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cursos`.`Avaliacoes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `avaliacao` INT NOT NULL,
  `comentario` VARCHAR(255) NULL,
  `id_user` INT NOT NULL,
  `id_curso` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Avaliacoes_User1_idx` (`id_user` ASC) VISIBLE,
  INDEX `fk_Avaliacoes_Cursos1_idx` (`id_curso` ASC) VISIBLE,
  CONSTRAINT `fk_Avaliacoes_User1`
    FOREIGN KEY (`id_user`)
    REFERENCES `Cursos`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Avaliacoes_Cursos1`
    FOREIGN KEY (`id_curso`)
    REFERENCES `Cursos`.`Cursos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Cursos`.`Curso_Trilha`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cursos`.`Curso_Trilha` (
  `Cursos_id` INT NOT NULL,
  `Trilha_apredizado_id` INT NOT NULL,
  INDEX `fk_Curso_Trilha_Cursos1_idx` (`Cursos_id` ASC) VISIBLE,
  INDEX `fk_Curso_Trilha_Trilha_apredizado1_idx` (`Trilha_apredizado_id` ASC) VISIBLE,
  CONSTRAINT `fk_Curso_Trilha_Cursos1`
    FOREIGN KEY (`Cursos_id`)
    REFERENCES `Cursos`.`Cursos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Curso_Trilha_Trilha_apredizado1`
    FOREIGN KEY (`Trilha_apredizado_id`)
    REFERENCES `Cursos`.`Trilhas_apredizado` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
