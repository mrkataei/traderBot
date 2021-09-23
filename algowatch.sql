-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 23, 2021 at 10:50 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `algowatch`
--

-- --------------------------------------------------------

--
-- Table structure for table `analysis`
--

CREATE TABLE `analysis` (
  `id` int(11) NOT NULL,
  `name` char(20) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `analysis`
--

INSERT INTO `analysis` (`id`, `name`, `description`) VALUES
(1, 'emerald', 'this signal is work for all coins and have 75% accuracy.'),
(2, 'ruby', 'this signal works for all coins and have 75% accuracy.'),
(3, 'diamond', 'this signal works only on btcusdt-4h , etcusdt-4h , bchusdt-4h , adausdt-4h , ethusdt-4h and dogeusdst-30m.\r\naccuracy of signal is 99.9% ');

-- --------------------------------------------------------

--
-- Table structure for table `analysis_setting`
--

CREATE TABLE `analysis_setting` (
  `id` int(11) NOT NULL,
  `coin_id` int(11) NOT NULL,
  `timeframe_id` int(11) NOT NULL,
  `analysis_id` int(11) NOT NULL,
  `analysis_setting` text NOT NULL,
  `indicator_setting_id` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `analysis_setting`
--

INSERT INTO `analysis_setting` (`id`, `coin_id`, `timeframe_id`, `analysis_id`, `analysis_setting`, `indicator_setting_id`) VALUES
(1, 1, 1, 1, '', '1'),
(2, 1, 2, 1, '', '1'),
(3, 1, 3, 1, '', '1'),
(4, 1, 4, 1, '', '1'),
(5, 2, 1, 1, '', '1'),
(6, 2, 2, 1, '', '1'),
(7, 2, 3, 1, '', '1'),
(8, 2, 4, 1, '', '1'),
(9, 3, 1, 1, '', '1'),
(10, 3, 2, 1, '', '1'),
(11, 3, 3, 1, '', '1'),
(12, 3, 4, 1, '', '1'),
(13, 4, 1, 1, '', '1'),
(14, 4, 2, 1, '', '1'),
(15, 4, 3, 1, '', '1'),
(16, 4, 4, 1, '', '1'),
(17, 5, 1, 1, '', '1'),
(18, 5, 2, 1, '', '1'),
(19, 5, 3, 1, '', '1'),
(20, 5, 4, 1, '', '1'),
(21, 6, 1, 1, '', '1'),
(22, 6, 2, 1, '', '1'),
(23, 6, 3, 1, '', '1'),
(24, 6, 4, 1, '', '1'),
(26, 1, 3, 3, 'stoch_k_oversell:24,stoch_k_overbuy:75,stoch_rsi_k_overbuy:74,stoch_rsi_k_oversell:20,rsi_oversell:37,rsi_overbuy:64', '2,14,19,10'),
(27, 2, 3, 3, 'stoch_k_oversell:21,stoch_k_overbuy:83,stoch_rsi_k_overbuy:81,stoch_rsi_k_oversell:10,rsi_oversell:37,rsi_overbuy:80', '11,20,3,15'),
(28, 5, 3, 3, 'stoch_k_oversell:17,stoch_k_overbuy:93,stoch_rsi_k_overbuy:69,stoch_rsi_k_oversell:8,rsi_oversell:36,rsi_overbuy:85', '12,16,21,4'),
(29, 3, 3, 3, 'stoch_k_oversell:37,stoch_k_overbuy:91,stoch_rsi_k_overbuy:85,stoch_rsi_k_oversell:17,rsi_oversell:50,rsi_overbuy:58', '13,17,22,7'),
(30, 6, 3, 3, 'stoch_k_oversell:10,stoch_k_overbuy:91,stoch_rsi_k_overbuy:55,stoch_rsi_k_oversell:84,rsi_oversell:81,rsi_overbuy:88', '10,14,24,8'),
(31, 4, 1, 3, 'stoch_k_oversell:20,stoch_k_overbuy:92,stoch_rsi_k_overbuy:96,stoch_rsi_k_oversell:18,rsi_oversell:29,rsi_overbuy:62', '10,18,23,9');

-- --------------------------------------------------------

--
-- Table structure for table `bank`
--

CREATE TABLE `bank` (
  `user` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `amount` double NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `bank`
--

INSERT INTO `bank` (`user`, `amount`) VALUES
('arman', 10),
('kouroshataei', 220458.0064999999);

-- --------------------------------------------------------

--
-- Table structure for table `coins`
--

CREATE TABLE `coins` (
  `id` int(11) NOT NULL,
  `coin` varchar(30) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `coins`
--

INSERT INTO `coins` (`id`, `coin`) VALUES
(1, 'BTCUSDT'),
(2, 'ETHUSDT'),
(3, 'ADAUSDT'),
(4, 'DOGEUSDT'),
(5, 'BCHUSDT'),
(6, 'ETCUSDT');

-- --------------------------------------------------------

--
-- Table structure for table `indicators`
--

CREATE TABLE `indicators` (
  `id` int(10) NOT NULL,
  `name` char(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `indicators`
--

INSERT INTO `indicators` (`id`, `name`) VALUES
(1, 'MACD'),
(2, 'stoch'),
(3, 'RSI'),
(4, 'ichimoku'),
(5, 'stochrsi');

-- --------------------------------------------------------

--
-- Table structure for table `indicators_settings`
--

CREATE TABLE `indicators_settings` (
  `indicator_id` int(11) NOT NULL,
  `settings` text NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `indicators_settings`
--

INSERT INTO `indicators_settings` (`indicator_id`, `settings`, `id`) VALUES
(4, 'tenkan:9,kijun:26,senkou:52', 1),
(1, 'slow:23,sign:20,fast:5,source:close', 2),
(1, 'fast:6,slow:14,signal:20,source:hlc3', 3),
(1, 'fast:9,slow:15,signal:20,source:close', 4),
(1, 'fast:12,slow:18,signal:20,source:hlc3', 7),
(1, 'fast:11,slow:36,signal:20,source:close', 8),
(1, 'fast:13,slow:18,signal:20,source:ohlc4', 9),
(3, 'source:close,length:5', 10),
(3, 'source:close,length:4', 11),
(3, 'source:close,length:7', 12),
(3, 'source:close,length:3', 13),
(2, 'k:18,d:3,smooth:3', 14),
(2, 'k:10,d:3,smooth:2', 15),
(2, 'k:20,d:3,smooth:3', 16),
(2, 'k:22,d:3,smooth:3', 17),
(2, 'k:23,d:3,smooth:3', 18),
(5, 'rsi_length:24,length:15,k:3,d:3,source:close', 19),
(5, 'rsi_length:11,length:17,k:3,d:3,source:close', 20),
(5, 'rsi_length:6,length:21,k:4,d:3,source:hlc3', 21),
(5, 'rsi_length:14,length:14,k:4,d:2,source:ohlc4', 22),
(5, 'rsi_length:12,length:20,k:5,d:3,source:ohlc4', 23),
(5, 'rsi_length:16,length:23,k:3,d:3,source:high', 24);

-- --------------------------------------------------------

--
-- Table structure for table `recommendations`
--

CREATE TABLE `recommendations` (
  `coin_id` int(11) NOT NULL,
  `analysis_id` int(11) NOT NULL,
  `position` char(12) NOT NULL,
  `target_price` double NOT NULL,
  `current_price` double NOT NULL,
  `timeframe_id` int(11) NOT NULL,
  `cost_price` double NOT NULL,
  `risk` char(12) NOT NULL,
  `timestmp` timestamp NOT NULL DEFAULT current_timestamp(),
  `id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `score_analysis`
--

CREATE TABLE `score_analysis` (
  `recom_id` int(12) NOT NULL,
  `score` int(5) NOT NULL,
  `user` char(30) NOT NULL,
  `is_used` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `secrity_question`
--

CREATE TABLE `secrity_question` (
  `id` int(11) NOT NULL,
  `question` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `secrity_question`
--

INSERT INTO `secrity_question` (`id`, `question`) VALUES
(1, 'What is the name of your first teacher?'),
(2, 'Wich city did you born?');

-- --------------------------------------------------------

--
-- Table structure for table `timeframes`
--

CREATE TABLE `timeframes` (
  `id` int(11) NOT NULL,
  `timeframe` varchar(12) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `timeframes`
--

INSERT INTO `timeframes` (`id`, `timeframe`) VALUES
(1, '30min'),
(2, '1hour'),
(3, '4hour'),
(4, '1day');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(12) NOT NULL,
  `user` char(30) NOT NULL,
  `operation` char(10) NOT NULL,
  `amount` float NOT NULL,
  `detail` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` char(30) NOT NULL,
  `chat_id` char(12) NOT NULL,
  `password` char(255) NOT NULL,
  `salt` int(20) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `question_id` int(11) NOT NULL,
  `question_answer` varchar(254) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `chat_id`, `password`, `salt`, `role`, `question_id`, `question_answer`, `timestamp`) VALUES
('arman', '417318078', '6103082b2ee92c048eb1bed6e03366d1de0ee064f57982806861644270c97c59ec83fdf21853830d7fe4a110cd670d1dd15e0318814d25879e9d71a471e7a438', 12206, 'user', 2, 'zahedan', '2021-09-15 10:24:18'),
('Ava', '113564501', 'eed8e1dbac644dbc52e12da83fa59119f3d18153a108f80dc32ba035beb4d28e3717da40990379d50b5e43d16f100414ea74d5f397f398962469157ffee2e207', 73278, 'user', 2, 'Mshd', '2021-09-02 10:02:00'),
('Fr4ys', '69964482', 'ad08ed46a240e129d3f213f749b13b2ff356653b5290bd4d0b807a96244a3f5409470caf7d49c92a424a92e5f79a402e6fc41fcf67b7f887eae41e1efb24e060', 53538, 'user', 1, 'Mmd', '2021-09-07 11:24:44'),
('jickab', '366781788', 'd8fc58e751507d7e4789a4523750461bf5514159ad9e2edeafcd49153a403c53c070652eb97fdfcd4c52073a3a6c81d048c8a0e60836dd25feb3b7b9ef29d600', 13676, 'user', 2, 'Mashhad', '2021-08-22 05:21:05'),
('kami', '912323333', '0c57d3645ebdd09eee26773b3115f24db74d26d1e1d9f81be1f6481259ca6bed4de3c0df3fa9066a62a1e557dbba0b5100db1e40fb58d24d5bce6ddcab22126e', 45796, 'user', 2, 'mashhad', '2021-09-03 00:36:16'),
('kourosh', '1079329555', 'd008020c484be3d2f97a1b5af3a384cdb8f6ab9bd44f6f1b4028302019b88fd4757bef6ffcb2a9ca62f27c24fddb9c1e818488a4b165fa2f0735a02f012e1d4e', 66640, 'user', 2, 'mashhad', '2021-08-22 03:19:41'),
('kourosh2', '1349338275', 'dbb162b99efd6a857be21f6484f3d8ee56fb63805c21171ad9bcb73593d68b5131cd8269a9ea6761febcc897c787d440728acdc88f17eefee62605ae51a0f72a', 23490, 'user', 2, 'ferdos', '2021-08-23 05:55:50'),
('kourosh75', '1978824576', '6bf79110d8e1b6a7687ca1ce6eb863ce5e8279eff7fc4fb9374987f8e8c27414d7bf85a158162a7325383f404dd485aa138d64b2584e253c5cb785d50191a9fc', 89058, 'user', 2, 'mashhad', '2021-09-13 15:21:36'),
('kouroshataei', '1210507821', '93a898fa890e0a1d6370ce6715f241d08d83ffda7a7e4150feb91cff607683538d9ee7a45047a39354a21c9e9b1daf56b552d1966650062f23efa3a58a018a86', 89640, 'admin', 1, 'qoli', '2021-08-02 09:31:33'),
('Mhrohany', '102316762', 'bf12e257954da99f0d2a70350e643510acbb08c90613365d6e0e654b70e00fe04bdf016ce21265f474a4874e4a046b8d2dcf7d851b141898fee3d44aaa530011', 73278, 'user', 2, 'Mashhad', '2021-09-02 10:09:57'),
('shrm', '100724824', '2baf1170a54994e08d405ac1e15c794f06813bd5e00083565af990aa503238380746154b4226439bbb8725a130d7ed19ef82682bd8828c22ca3e763a4536a64a', 13676, 'user', 1, 'A', '2021-08-22 04:56:14');

-- --------------------------------------------------------

--
-- Table structure for table `user_analysis`
--

CREATE TABLE `user_analysis` (
  `id` int(12) NOT NULL,
  `user` char(30) NOT NULL,
  `analysis_id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_analysis`
--

INSERT INTO `user_analysis` (`id`, `user`, `analysis_id`) VALUES
(13, 'arman', 1),
(16, 'kouroshataei', 1);

-- --------------------------------------------------------

--
-- Table structure for table `user_timeframe`
--

CREATE TABLE `user_timeframe` (
  `id` int(12) NOT NULL,
  `user` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `timeframe_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `user_timeframe`
--

INSERT INTO `user_timeframe` (`id`, `user`, `timeframe_id`) VALUES
(1, 'kouroshataei', 1),
(2, 'arman', 1),
(3, 'kourosh', 3),
(4, 'shrm', 1),
(5, 'jickab', 3),
(6, 'kourosh2', 4),
(7, 'Ava', 3),
(8, 'Mhrohany', 1),
(9, 'kami', 4),
(10, 'Fr4ys', 1),
(11, 'kourosh75', 1);

-- --------------------------------------------------------

--
-- Table structure for table `watchlist`
--

CREATE TABLE `watchlist` (
  `user` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `coin_id` int(12) DEFAULT NULL,
  `name` char(40) COLLATE utf8_bin DEFAULT NULL,
  `id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `watchlist`
--

INSERT INTO `watchlist` (`user`, `coin_id`, `name`, `id`) VALUES
('kouroshataei', 1, 'kou', 50),
('kouroshataei', 2, 'kou', 51),
('kouroshataei', 3, 'kou', 52),
('kouroshataei', 6, 'kou', 53);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analysis`
--
ALTER TABLE `analysis`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `analysis_setting`
--
ALTER TABLE `analysis_setting`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `coin_id_2` (`coin_id`,`timeframe_id`,`analysis_id`),
  ADD KEY `coin_id_as` (`coin_id`),
  ADD KEY `timeframe_id_as` (`timeframe_id`),
  ADD KEY `analysis_id_as` (`analysis_id`);

--
-- Indexes for table `bank`
--
ALTER TABLE `bank`
  ADD PRIMARY KEY (`user`);

--
-- Indexes for table `coins`
--
ALTER TABLE `coins`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `indicators`
--
ALTER TABLE `indicators`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `indicators_settings`
--
ALTER TABLE `indicators_settings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `indicator_id_tb` (`indicator_id`);

--
-- Indexes for table `recommendations`
--
ALTER TABLE `recommendations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `coin_id_recom` (`coin_id`),
  ADD KEY `analysis_id_recom` (`analysis_id`),
  ADD KEY `timeframe_id_recom` (`timeframe_id`);

--
-- Indexes for table `score_analysis`
--
ALTER TABLE `score_analysis`
  ADD UNIQUE KEY `recom_id` (`recom_id`,`user`),
  ADD KEY `user_score` (`user`);

--
-- Indexes for table `secrity_question`
--
ALTER TABLE `secrity_question`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `timeframes`
--
ALTER TABLE `timeframes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `transaction_username` (`user`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`,`chat_id`),
  ADD UNIQUE KEY `chat_id` (`chat_id`),
  ADD KEY `users_ibfk_1` (`question_id`);

--
-- Indexes for table `user_analysis`
--
ALTER TABLE `user_analysis`
  ADD PRIMARY KEY (`id`),
  ADD KEY `analysis_username` (`user`),
  ADD KEY `analysis_id` (`analysis_id`);

--
-- Indexes for table `user_timeframe`
--
ALTER TABLE `user_timeframe`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_timeframe_username` (`user`),
  ADD KEY `user_timeframe_timeframe_id` (`timeframe_id`);

--
-- Indexes for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user` (`user`,`coin_id`),
  ADD KEY `username` (`user`),
  ADD KEY `coin_id` (`coin_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `analysis`
--
ALTER TABLE `analysis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `analysis_setting`
--
ALTER TABLE `analysis_setting`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `coins`
--
ALTER TABLE `coins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `indicators`
--
ALTER TABLE `indicators`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `indicators_settings`
--
ALTER TABLE `indicators_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `recommendations`
--
ALTER TABLE `recommendations`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `timeframes`
--
ALTER TABLE `timeframes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user_analysis`
--
ALTER TABLE `user_analysis`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `user_timeframe`
--
ALTER TABLE `user_timeframe`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `watchlist`
--
ALTER TABLE `watchlist`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `analysis_setting`
--
ALTER TABLE `analysis_setting`
  ADD CONSTRAINT `analysis_id_as` FOREIGN KEY (`analysis_id`) REFERENCES `analysis` (`id`),
  ADD CONSTRAINT `coin_id_as` FOREIGN KEY (`coin_id`) REFERENCES `coins` (`id`),
  ADD CONSTRAINT `timeframe_id_as` FOREIGN KEY (`timeframe_id`) REFERENCES `timeframes` (`id`);

--
-- Constraints for table `bank`
--
ALTER TABLE `bank`
  ADD CONSTRAINT `username_bank` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

--
-- Constraints for table `indicators_settings`
--
ALTER TABLE `indicators_settings`
  ADD CONSTRAINT `indicator_id_tb` FOREIGN KEY (`indicator_id`) REFERENCES `indicators` (`id`);

--
-- Constraints for table `recommendations`
--
ALTER TABLE `recommendations`
  ADD CONSTRAINT `analysis_id_recom` FOREIGN KEY (`analysis_id`) REFERENCES `analysis` (`id`),
  ADD CONSTRAINT `coin_id_recom` FOREIGN KEY (`coin_id`) REFERENCES `coins` (`id`),
  ADD CONSTRAINT `timeframe_id_recom` FOREIGN KEY (`timeframe_id`) REFERENCES `timeframes` (`id`);

--
-- Constraints for table `score_analysis`
--
ALTER TABLE `score_analysis`
  ADD CONSTRAINT `recom_id_score` FOREIGN KEY (`recom_id`) REFERENCES `recommendations` (`id`),
  ADD CONSTRAINT `user_score` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transaction_username` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `secrity_question` (`id`);

--
-- Constraints for table `user_analysis`
--
ALTER TABLE `user_analysis`
  ADD CONSTRAINT `analysis_id` FOREIGN KEY (`analysis_id`) REFERENCES `analysis` (`id`),
  ADD CONSTRAINT `analysis_username` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

--
-- Constraints for table `user_timeframe`
--
ALTER TABLE `user_timeframe`
  ADD CONSTRAINT `user_timeframe_timeframe_id` FOREIGN KEY (`timeframe_id`) REFERENCES `timeframes` (`id`),
  ADD CONSTRAINT `user_timeframe_username` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

--
-- Constraints for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD CONSTRAINT `coin_id` FOREIGN KEY (`coin_id`) REFERENCES `coins` (`id`),
  ADD CONSTRAINT `username` FOREIGN KEY (`user`) REFERENCES `users` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;