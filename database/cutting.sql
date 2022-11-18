-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 01 avr. 2021 à 18:36
-- Version du serveur :  5.7.31
-- Version de PHP : 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `cutting`
--

-- --------------------------------------------------------

--
-- Structure de la table `conditionscoupe`
--

DROP TABLE IF EXISTS `conditionscoupe`;
CREATE TABLE IF NOT EXISTS `conditionscoupe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_lubrifiant` varchar(15) DEFAULT NULL,
  `vitesse_coupe` float DEFAULT NULL,
  `vitesse_avance` float DEFAULT NULL,
  `profondeur_passe` float DEFAULT NULL,
  `temps` float DEFAULT NULL,
  `id_experience` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_experience` (`id_experience`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `effortcoupe`
--

DROP TABLE IF EXISTS `effortcoupe`;
CREATE TABLE IF NOT EXISTS `effortcoupe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fx` float DEFAULT NULL,
  `fy` float DEFAULT NULL,
  `fz` float DEFAULT NULL,
  `id_conditions_coupe` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_conditions_coupe` (`id_conditions_coupe`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `experience`
--

DROP TABLE IF EXISTS `experience`;
CREATE TABLE IF NOT EXISTS `experience` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `outil`
--

DROP TABLE IF EXISTS `outil`;
CREATE TABLE IF NOT EXISTS `outil` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(15) DEFAULT NULL,
  `materiau` varchar(15) DEFAULT NULL,
  `geometrie` varchar(15) DEFAULT NULL,
  `duree_de_vie` float DEFAULT NULL,
  `temps` float DEFAULT NULL,
  `id_experience` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_experience` (`id_experience`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `piece`
--

DROP TABLE IF EXISTS `piece`;
CREATE TABLE IF NOT EXISTS `piece` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `materiau` varchar(15) DEFAULT NULL,
  `type_fabrication` varchar(15) DEFAULT NULL,
  `fatigue` float DEFAULT NULL,
  `durete` float DEFAULT NULL,
  `contraintes_residuelles` float DEFAULT NULL,
  `temps` float DEFAULT NULL,
  `id_experience` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_experience` (`id_experience`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `rugosite`
--

DROP TABLE IF EXISTS `rugosite`;
CREATE TABLE IF NOT EXISTS `rugosite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `valeur` float DEFAULT NULL,
  `id_piece` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_piece` (`id_piece`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `temperature`
--

DROP TABLE IF EXISTS `temperature`;
CREATE TABLE IF NOT EXISTS `temperature` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `valeur` float DEFAULT NULL,
  `id_conditions_coupe` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_conditions_coupe` (`id_conditions_coupe`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE USER 'admin'@'localhost' IDENTIFIED BY 'C9SaiK9pRkmoHuXvTV10';
GRANT ALL PRIVILEGES ON cutting.* TO 'admin'@'localhost';

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
