-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-10-2024 a las 17:40:26
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `documentosbasedates`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciclo`
--

CREATE TABLE `ciclo` (
  `ID_CICLO` int(11) NOT NULL,
  `NRO_CICLO` enum('I','II','III','IV','V','VI') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ciclo`
--

INSERT INTO `ciclo` (`ID_CICLO`, `NRO_CICLO`) VALUES
(1, 'I'),
(2, 'II'),
(3, 'III'),
(4, 'IV'),
(5, 'V'),
(6, 'VI');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `curso`
--

CREATE TABLE `curso` (
  `ID_CURSO` int(11) NOT NULL,
  `NOMBRE_CURSO` varchar(100) NOT NULL,
  `DESCRIPCION_DEL_CURSO` text DEFAULT NULL,
  `ID_CICLO` int(11) DEFAULT NULL,
  `DIA` varchar(20) DEFAULT NULL,
  `HORA_INICIO` time DEFAULT NULL,
  `HORA_FIN` time DEFAULT NULL,
  `ID_PROFESOR` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `curso`
--

INSERT INTO `curso` (`ID_CURSO`, `NOMBRE_CURSO`, `DESCRIPCION_DEL_CURSO`, `ID_CICLO`, `DIA`, `HORA_INICIO`, `HORA_FIN`, `ID_PROFESOR`) VALUES
(1, 'Comprensión y redacción en Inglés', 'Curso para mejorar la comprensión y redacción en inglés', 4, 'Lunes', '14:15:00', '16:30:00', 7),
(2, 'Seguridad Informática', 'Curso sobre medidas de seguridad informática', 4, 'Lunes', '16:30:00', '18:00:00', 3),
(3, 'Taller de Software', 'Curso práctico sobre desarrollo de software', 4, 'Lunes', '18:20:00', '19:50:00', 4),
(4, 'Experiencias Formativas', 'Curso para la formación en diversas áreas profesionales', 4, 'Martes', '14:15:00', '15:45:00', 1),
(5, 'Taller de Software', 'Curso práctico sobre desarrollo de software', 4, 'Martes', '15:45:00', '17:15:00', 4),
(6, 'Diseño Gráfico', 'Curso sobre técnicas de diseño gráfico', 4, 'Martes', '17:15:00', '18:00:00', 2),
(7, 'Seguridad Informática', 'Curso sobre medidas de seguridad informática', 4, 'Miércoles', '14:15:00', '17:15:00', 3),
(8, 'Cultura Ambiental', 'Curso sobre concientización ambiental', 4, 'Miércoles', '17:15:00', '19:50:00', 4),
(9, 'Taller de Base de Datos', 'Curso sobre el manejo de bases de datos', 4, 'Jueves', '15:00:00', '17:15:00', 5),
(10, 'Diseño Gráfico', 'Curso sobre técnicas de diseño gráfico', 4, 'Jueves', '17:15:00', '19:50:00', 2),
(11, 'Taller de Base de Datos', 'Curso sobre el manejo de bases de datos', 4, 'Viernes', '15:00:00', '17:15:00', 5),
(12, 'Taller de Software', 'Curso práctico sobre desarrollo de software', 4, 'Viernes', '17:15:00', '19:05:00', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes_del_dsi`
--

CREATE TABLE `estudiantes_del_dsi` (
  `ID_ESTUDIANTE` int(11) NOT NULL,
  `DNI` varchar(20) NOT NULL,
  `NOMBRE` varchar(50) NOT NULL,
  `APELLIDO_P` varchar(50) NOT NULL,
  `APELLIDO_M` varchar(50) NOT NULL,
  `CORREO` varchar(100) NOT NULL,
  `NUMERO_TELEFONO` varchar(20) DEFAULT NULL,
  `DIRECCION` text DEFAULT NULL,
  `ID_CICLO` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes_del_dsi`
--

INSERT INTO `estudiantes_del_dsi` (`ID_ESTUDIANTE`, `DNI`, `NOMBRE`, `APELLIDO_P`, `APELLIDO_M`, `CORREO`, `NUMERO_TELEFONO`, `DIRECCION`, `ID_CICLO`) VALUES
(1, '61039983', 'Adrian Arturo', 'Astete', 'Hassinger', 'adrian.hassinger17@gmail.com', '937652611', NULL, 2),
(2, '43686347', 'Alex Bijhay', 'Bazan', 'Rojas', 'alexbijhay1981@gmail.com', '915948317', NULL, 2),
(3, '77648746', 'Leonardo', 'Cahuana', 'Tello', 'cahuanatelloleonardo@gmail.com', '929608252', NULL, 2),
(4, '77876500', 'Vianca Alexandra', 'Campos', 'Da Silva', 'alecamposds29@gmail.com', '963410206', NULL, 2),
(5, '60963473', 'Emiliano Sebastian', 'Culqui', 'Moncada', 'emilianoculqui203@gmail.com', '978955810', NULL, 2),
(6, '73897884', 'Carlos Andres', 'Duque', 'Balabarca', 'duquecarlos716@gmail.com', '994279939', NULL, 2),
(7, '74853143', 'Jack Elias', 'Fachin', 'Delgado', 'fachindelgadoj@gmail.com', '968946763', NULL, 2),
(8, '74861005', 'Leonardo Ivan', 'Flores', 'Taricuarima', 'liftper2005@gmail.com', '947355256', NULL, 2),
(9, '76803746', 'Rowling Anthony', 'Garcia', 'Cordova', 'rowlinganthonygarciacordova@gmail.com', '922375282', NULL, 2),
(10, '75990313', 'Ruth Abigail', 'Gonzales', 'Macedo', 'ruthabigailgonzalesmacedo@gmail.com', '929642387', NULL, 2),
(11, '63415624', 'Wagner Adelson', 'Gonzales', 'Vargas', 'gonzalesvargaswagnerdel son@gmail.com', '925305851', NULL, 2),
(12, '61077615', 'Franklin Daniel', 'Isuiza', 'Herrera', 'franklin18daniel2007@gmail.com', '921678758', NULL, 2),
(13, '61006046', 'Fresia Esther Alexandra', 'Lozano', 'Fripp', 'fresialozanofripp@gmail.com', '961163848', NULL, 2),
(14, '76779608', 'Elsa Bris', 'Mallma', 'Champi', 'mallmaelsa743@gmail.com', '949735936', NULL, 2),
(15, '75273160', 'Wilson', 'Marin', 'Flores', 'wmflores1@gmail.com', '919184892', NULL, 2),
(16, '47359082', 'Sandro Wichi', 'Marquez', 'Sanchez', 'marquezsanchezsandro10@gmail.com', '948161786', NULL, 2),
(17, '75423275', 'Cledy Beria', 'Maynas', 'Inuma', 'cledymaynas@gmail.com', '928393309', NULL, 2),
(18, '62779851', 'Analy Dariana', 'Medina', 'Maiz', 'Analydarianamedinamaiz@gmail.com', '982320630', NULL, 2),
(19, '45179057', 'Giancarlo', 'Mera', 'Flores', 'giangreymevas@gmail.com', '902035363', NULL, 2),
(20, '75766147', 'Luis Fernando', 'Mori', 'Orbe', 'fernandomori123456789@gmail.com', '995297568', NULL, 2),
(21, '77698560', 'Isai Fortunato', 'Palomino', 'Porras', 'palominoporrasisai2006@gmail.com', '935854682', NULL, 2),
(22, '73885601', 'Carlos Alexis', 'Perea', 'Saldaña', 'caps6954@gmailcom', '967349054', NULL, 2),
(23, '60956899', 'Erick Alexander', 'Perez', 'Shuña', 'erickperezshuña@gmail.com', '980094709', NULL, 2),
(24, '61133509', 'Francisco David', 'Pezo', 'Torres', 'pezotorresfranciscodavid2@gmail.com', '982049224', NULL, 2),
(25, '72720844', 'Luis Enrique', 'Ruiz', 'Salas', 'luisruizsalas01@gmail.com', '983850017', NULL, 2),
(26, '74624805', 'Albert Jhon', 'Saldaña', 'Quispe', 'albertsal650@gmail.com', '922304287', NULL, 2),
(27, '61040459', 'Sergio Adrian', 'Serruche', 'Panduro', 'irispanduroaguilar12@gmail.com', '982900882', NULL, 2),
(28, '60996693', 'Dan Jhonatan', 'Silva', 'Asipali', 'victorhugosilvacuricimba@gmail.com', '919651787', NULL, 2),
(29, '61584811', 'Weslin Andilo', 'Urquia', 'Rios', 'urquiariosweslinandilo@gmail.com', '951248933', NULL, 2),
(30, '76233162', 'Dayana Brillith', 'Ushiñahua', 'Pinedo', 'dayamaushinahua@gmail.com', '970327247', NULL, 2),
(31, '76780397', 'Paris Hilton Rahul', 'Velasquez', 'Perez', 'parisvelasquez456@gmail.com', '929520306', NULL, 2),
(32, '62828314', 'Jhonny David', 'Viena', 'Guevara', 'zinedineviena@gmail.com', '951158317', NULL, 2),
(33, '76814977', 'Ever Daniel', 'Ahuanari', 'Ipushima', 'ever200299@gmail.com', '928100678', NULL, 4),
(34, '76979586', 'Hugo Alfredo', 'Bastos', 'salazar', 'bastoshugo01@gmail.com', '939063464', NULL, 4),
(35, '74856145', 'Juan Carlos', 'Campana', 'Sangama', 'jotoccampanasangama@gmail.com', '969639899', NULL, 4),
(36, '76851312', 'Gerald Alexander', 'Castro', 'Fuentes', 'fuentesgloria064@gmail.com', '922369539', NULL, 4),
(37, '75485672', 'Antony Americo', 'Figueredo', 'Calampa', 'americofc06@gmail.com', '970896336', NULL, 4),
(38, '77801638', 'Anthony Aroldo', 'Garcia', 'Prada', 'ag275528@gmail.com', '944406672', NULL, 4),
(39, '75614641', 'Erix Angel Eduardo', 'Hubner', 'Salas', 'xire667@gmail.com', '961266281', NULL, 4),
(40, '77274216', 'Eder Angelo', 'Inga', 'Bautista', 'ederangeloingabautista@gmail.com', '915913802', NULL, 4),
(41, '46827064', 'Yeli Solange', 'Lagomarcino', 'Rojas', 'yeyelagomarcinorojas@gmail.com', '919757743', NULL, 4),
(42, '63349761', 'Miquias', 'Linares', 'Moreno', 'miquiaslinaresmoreno@gmail.com', '961599647', NULL, 4),
(43, '71721109', 'Nixon Miller', 'Mancilla', 'Leon', 'mancillanixon7@gmail.com', '925075598', NULL, 4),
(44, '76267844', 'Michell', 'Manihuari', 'Flores', 'setiembreforever@gmail.com', '933609735', NULL, 4),
(45, '73579001', 'Antonich Lloyd', 'Marin', 'Alejo', 'damasyajedrez1020@gmail.com', '921076170', NULL, 4),
(46, '72975292', 'Marco Erick', 'Martinez', 'Rodriguez', 'marcoerick642@gmail.com', '967603871', NULL, 4),
(47, '76591294', 'Joseph', 'Padilla', 'Alvan', 'jpadillalvan02@gmail.com', '929310114', NULL, 4),
(48, '74879133', 'Jim Kevin', 'Paredes', 'Huansi', 'jimparedesh12@gmail.com', '948190643', NULL, 4),
(49, '48817886', 'Wenceslao', 'Paredes', 'Rodriguez', 'jessiaguelle@gmail.com', '945645643', NULL, 4),
(50, '72450489', 'Bruno Martin', 'Perez', 'Rodriguez', 'brumapero17@gmail.com', '950861689', NULL, 4),
(51, '75971659', 'Victor Joseph', 'Ramirez', 'Manihuari', 'victorariesr@gmail.com', '955121008', NULL, 4),
(52, '63112277', 'Noelia Corali', 'Saavedra', 'Garcia', 'coralisaavedra243@gmail.com', '930615736', NULL, 4),
(53, '73006764', 'Carlos Manuel', 'Saavedra', 'Lopez', 'saavedrakatty09@gmail.com', '989692739', NULL, 4),
(54, '60682182', 'Estefani Xiomara', 'Segundo', 'Pereyra', 'xiomarapereyra98@gmail.com', '916297163', NULL, 4),
(55, '60185321', 'Leonardo Junior', 'Silva', 'Saboya', 'leojuniorss.8lj@gmail.com', '978744623', NULL, 4),
(56, '77579386', 'Jhoandri Josep', 'Solsol', 'Perez', 'jhoandrisolsolperez@gmail.com', '943017391', NULL, 4),
(57, '72659206', 'Cesar Arnold', 'Soria', 'Paima', 'soriapaimacesar@gmail.com', '967996672', NULL, 4),
(58, '75219857', 'Romer Alejandro', 'Ursua', 'Cahuaza', 'ursuaalejandro5@gmail.com', '928109685', NULL, 4),
(59, '71439589', 'Edinson Enrique', 'Vargas', 'Castillon', 'edinsonenrique300@gmail.com', '975522337', NULL, 4),
(60, '74893312', 'Olmes Emyl', 'Villacorta', 'Pacaya', 'olmesemylvillacortapacaya@gmail.com', '928904548', NULL, 4),
(61, '76810059', 'Victor Joel', 'Yaicate', 'Cahuaza', 'victoryaicate12@gmail.com', '970147084', NULL, 4),
(62, '77222112', 'Mauro', 'Cabanilla', 'Diaz', 'cabanillasmauro7@gmil.com', '947637636', NULL, 6),
(63, '72848961', 'Frank Patrick', 'Cahuachi', 'Chu', 'frankpatrickcahuachichu@gmail.com', '929328042', NULL, 6),
(64, '76117521', 'Milton', 'Cerron', 'Saboya', 'miltoncerronsaboya@gmail.com', '970084673', NULL, 6),
(65, '72166080', 'Willy Joseph', 'Chavez', 'Prada', 'wjosephch@gmail.com', '982984429', NULL, 6),
(66, '77217344', 'Marcos Alberto', 'Chino', 'Ruiz', 'marcosalberto17chino@gmail.com', '945528106', NULL, 6),
(67, '75244140', 'Carmen Lucia', 'Galindo', 'Bardales', 'galindovcarmen55@gmail.com', '970092392', NULL, 6),
(68, '42983234', 'Jhimmy Alan', 'Garcia', 'Vargas', 'ws.parkg@gmail.com', '920316994', NULL, 6),
(69, '75887985', 'Jeremy', 'Gomez', 'Sanchez', 'jeremygomezsanchez58@gmail.com', '945710720', NULL, 6),
(70, '61245880', 'Ramiro', 'Gonzales', 'Vela', '4m1r0228@gmail.com', '945439512', NULL, 6),
(71, '76726026', 'Charles Jonathan', 'Leon', 'Tafur', 'charlesleontafur@gmail.com', '924723889', NULL, 6),
(72, '72838449', 'Jefferson', 'Lopez', 'Ramirez', 'jlr080914@gmail.com', '923021799', NULL, 6),
(73, '61006533', 'Cristofer Joan', 'Panduro', 'Torres', 'cristofertorres2004j@gmail.com', '922580560', NULL, 6),
(74, '73515743', 'Yhordy Alfredo', 'Peralta', 'Quispe', 'halfredo987@gmail.com', '953152027', NULL, 6),
(75, '62828507', 'Daniel Andrey', 'Piña', 'Reategui', 'andrepidaniel@gmail.com', '951089852', NULL, 6),
(76, '74405540', 'Aaron', 'Rengifo', 'Choy Sanchez', 'choysad123@gmail.com', '983533662', NULL, 6),
(77, '70981870', 'Fidel Martin', 'Saavedra', 'Andres', 'sfidelandres@gmail.com', '923018247', NULL, 6),
(78, '72688606', 'Claudio Junniors', 'Saldarriaga', 'Torrejon', '', NULL, NULL, 6),
(79, '72178780', 'Fernando Elidor', 'Samame', 'Rodriguez', 'samamefernando21@gmail.com', '965822549', NULL, 6),
(80, '46729931', 'Armando Martin', 'Soria', 'Lopez', 'armando-21-7@hotmail.com', '921660284', NULL, 6),
(81, '72479304', 'Amy Nayely', 'Soriano', 'Tuanama', 'sorianotuanamaamy@gmail.com', '939372935', NULL, 6),
(82, '72260176', 'Joisy Fernanda', 'Torres', 'Marquez', 'jofertm05@gmail.com', '979531466', NULL, 6),
(83, '75579634', 'Abraham', 'Vasquez', 'Arevalo', 'abraham.24vasquez@gmail.com', '988618983', NULL, 6),
(84, '75755093', 'Farid Caleb', 'Zamora', 'Echevarria', 'calebespinozapkmz@gmail.com', '921585983', NULL, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

CREATE TABLE `profesores` (
  `ID_PROFESOR` int(11) NOT NULL,
  `NOMBRE_PROFESOR` varchar(100) NOT NULL,
  `APELLIDOS_PROFESOR` varchar(100) NOT NULL,
  `CORREO_PROFESOR` varchar(150) NOT NULL,
  `NUMERO_PROFESOR` varchar(15) DEFAULT NULL,
  `FECHA_REGISTRO` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profesores`
--

INSERT INTO `profesores` (`ID_PROFESOR`, `NOMBRE_PROFESOR`, `APELLIDOS_PROFESOR`, `CORREO_PROFESOR`, `NUMERO_PROFESOR`, `FECHA_REGISTRO`) VALUES
(1, 'Gil', 'Torres Arévalo', 'giltorresarevalo@gmail.com', '976681426', '2024-10-18 14:22:29'),
(2, 'Ruber', 'Torres Arévalo', 'rutoar2015@gmail.com', '982574167', '2024-10-18 14:22:29'),
(3, 'Christian Dustin', 'Puyo Torres', 'christianpuyotorres@gmail.com', '918282361', '2024-10-18 14:22:29'),
(4, 'John', 'Saboya Fulca', 'afheryita@gmail.com', '988452394', '2024-10-18 14:22:29'),
(5, 'Juan Carlos', 'Ríos Arriaga', 'virgojuank@hotmail.com', '942652485', '2024-10-18 14:22:29'),
(6, 'Lisnairi', 'Tuanama Seberiano', 'lisnairit@gmail.com', '960717265', '2024-10-18 14:22:29'),
(7, 'Diana Carolina', 'Hidalgo Gonzales', '', '@gmail.com', '0000-00-00 00:00:00');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ciclo`
--
ALTER TABLE `ciclo`
  ADD PRIMARY KEY (`ID_CICLO`);

--
-- Indices de la tabla `curso`
--
ALTER TABLE `curso`
  ADD PRIMARY KEY (`ID_CURSO`),
  ADD KEY `ID_CICLO` (`ID_CICLO`),
  ADD KEY `FK_ID_PROFESOR` (`ID_PROFESOR`);

--
-- Indices de la tabla `estudiantes_del_dsi`
--
ALTER TABLE `estudiantes_del_dsi`
  ADD PRIMARY KEY (`ID_ESTUDIANTE`),
  ADD UNIQUE KEY `DNI` (`DNI`),
  ADD UNIQUE KEY `CORREO` (`CORREO`),
  ADD KEY `ID_CICLO` (`ID_CICLO`);

--
-- Indices de la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`ID_PROFESOR`),
  ADD UNIQUE KEY `CORREO_PROFESOR` (`CORREO_PROFESOR`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `ciclo`
--
ALTER TABLE `ciclo`
  MODIFY `ID_CICLO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `curso`
--
ALTER TABLE `curso`
  MODIFY `ID_CURSO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `estudiantes_del_dsi`
--
ALTER TABLE `estudiantes_del_dsi`
  MODIFY `ID_ESTUDIANTE` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT de la tabla `profesores`
--
ALTER TABLE `profesores`
  MODIFY `ID_PROFESOR` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `curso`
--
ALTER TABLE `curso`
  ADD CONSTRAINT `FK_ID_PROFESOR` FOREIGN KEY (`ID_PROFESOR`) REFERENCES `profesores` (`ID_PROFESOR`),
  ADD CONSTRAINT `curso_ibfk_1` FOREIGN KEY (`ID_CICLO`) REFERENCES `ciclo` (`ID_CICLO`);

--
-- Filtros para la tabla `estudiantes_del_dsi`
--
ALTER TABLE `estudiantes_del_dsi`
  ADD CONSTRAINT `estudiantes_del_dsi_ibfk_1` FOREIGN KEY (`ID_CICLO`) REFERENCES `ciclo` (`ID_CICLO`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
