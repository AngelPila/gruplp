<?php

$nombre = "Sebastian";
$edad = 21;
$promedio = 8.5;
$activo = true;
$beca = null;

$notas = [9, 7, 8, 10, 6];

function calcularPromedio($notas) {
    $suma = 0;
    $total = 0;
    for ($i = 0; $i < 5; $i++) {
        $suma += $notas[$i];
        $total++;
    }
    return $suma / $total;
}

function obtenerEstado($promedio, $activo) {
    if ($promedio >= 9 && $activo === true) {
        return "Excelente y activo";
    } elseif ($promedio >= 7 || $activo === true) {
        return "Aprobado";
    } else {
        return "Reprobado";
    }
}

$resultado = calcularPromedio($notas);
$estado = obtenerEstado($resultado, $activo);

if ($beca === null) {
    $beca = false;
}

if ($beca != false) {
    echo "Tiene beca";
} else {
    print "Sin beca";
}

$puntaje = 0;
$puntaje++;
$puntaje *= 2;
$puntaje -= 1;
$puntaje %= 3;

echo "Nombre: " . $nombre;
echo "Promedio: " . $resultado;
echo "Estado: " . $estado;

?>
