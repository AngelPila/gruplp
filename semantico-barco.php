<?php

$nombre = "Sebastian";
$edad = 20;
$activo = true;
$promedio = 8.5;

function calcularBono($sueldo, $anios) {
    $bono = $sueldo * $anios;
    return $bono;
}

function clasificar($valor) {
    if ($valor >= 9) {
        return "alto";
    }
    return "bajo";
}

$sueldo = 1000;
$bonoFinal = calcularBono($sueldo, $edad);
$categoria = clasificar($promedio);

echo $nombre;
echo $bonoFinal;
echo $categoria;

echo $apellido;

echo $telefono;

$total = $sueldo + $descuento;

$mensaje = despedir($nombre);

$reporte = generarReporte($edad, $activo);

?>
