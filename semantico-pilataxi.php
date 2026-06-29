<?php

$base = 10;
$altura = 5;

// Error semantico 1: division por cero con literal
$resultado1 = $base / 0;

// Error semantico 2: modulo por cero con literal
$resultado2 = $altura % 0;

function calcular($n) {
    return $n * 2;
}

// Error semantico 3: funcion redeclarada con el mismo nombre
function calcular($m) {
    return $m + 1;
}

echo $resultado1;
echo $resultado2;

?>
