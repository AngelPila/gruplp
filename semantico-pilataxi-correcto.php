<?php

$base = 10;
$divisor = 2;

// Sin errores: divisor es variable, no literal 0
$resultado = $base / $divisor;

function calcular($n) {
    return $n * 2;
}

// Sin errores: nombre de funcion diferente
function describir($texto) {
    return $texto;
}

$valor = calcular($base);
echo $valor;

?>
